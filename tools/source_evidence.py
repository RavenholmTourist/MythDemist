"""Shared source extraction for quotation checks and retrieval; no network access."""
import re
from functools import lru_cache
import xml.etree.ElementTree as ET
from pathlib import Path


def normalize(text):
    return re.sub(r"\s+", " ", text).strip()


def _tag(node):
    return node.tag.rsplit("}", 1)[-1]


def _primary_text(node):
    parts = [node.text or ""]
    for child in node:
        if _tag(child) != "note":
            parts.append(_primary_text(child))
        parts.append(child.tail or "")
    return "".join(parts)


def _plain_ovid_segments(text, book_headings):
    """Separate Riley's verse from arguments, synopses, footnotes, and explanations."""
    roman = {
        "FIRST": "I", "SECOND": "II", "THIRD": "III", "FOURTH": "IV",
        "FIFTH": "V", "SIXTH": "VI", "SEVENTH": "VII", "EIGHTH": "VIII",
        "NINTH": "IX", "TENTH": "X", "ELEVENTH": "XI", "TWELFTH": "XII",
        "THIRTEENTH": "XIII", "FOURTEENTH": "XIV", "FIFTEENTH": "XV",
    }
    fable_heading = re.compile(
        r"^\s*FABLES?\s+(.+?)\s*(\[[IVXLCDM]+\.\d+(?:-\d+)?\])\s*$",
        re.I | re.M,
    )
    explanation_heading = re.compile(r"^\s*EXPLANATION\.\s*$", re.I | re.M)
    segments = []

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    def without_footnotes(value):
        kept = []
        skipping = False
        depth = 0
        for line in value.splitlines():
            if not skipping and re.match(r"^\s*\[Footnote \d+:", line, re.I):
                skipping = True
                depth = line.count("[") - line.count("]")
                continue
            if skipping:
                depth += line.count("[") - line.count("]")
                if depth <= 0:
                    skipping = False
                continue
            kept.append(line)
        return "\n".join(kept)

    for book_index, heading in enumerate(book_headings):
        book = roman[heading.group(1).upper()]
        end = book_headings[book_index + 1].start() if book_index + 1 < len(book_headings) else len(text)
        body = text[heading.end():end]
        book_locator = f"Book {book}"

        # Riley prints Ovid's four-line proem under this heading; other argument
        # and FABLE summaries are editorial synopses, not Ovid's verse.
        proem = re.search(r"^\s*THE ARGUMENT\.\s*\[I\.1-4\]\s*$", body, re.I | re.M) if book == "I" else None
        if proem:
            proem_end = re.search(r"^\s*\[Footnote \d+:", body[proem.end():], re.I | re.M)
            stop = proem.end() + proem_end.start() if proem_end else len(body)
            add(without_footnotes(body[proem.end():stop]), f"{book_locator} · Proem [I.1-4]", "source-text")

        headings = list(fable_heading.finditer(body))
        for index, fable in enumerate(headings):
            section_end = headings[index + 1].start() if index + 1 < len(headings) else len(body)
            section = body[fable.end():section_end]
            explanation = explanation_heading.search(section)
            verse_area = section[:explanation.start()] if explanation else section
            # In this edition each FABLE's two-space-indented synopsis precedes
            # the flush-left translated narrative.
            verse_start = next(
                (match.start() for match in re.finditer(r"(?m)^(?=\S)", verse_area) if verse_area[match.start():].strip()),
                -1,
            )
            label = fable.group(1).rstrip(". ")
            locator = f"{book_locator} · Fable {label} {fable.group(2)}"
            if verse_start >= 0:
                add(without_footnotes(verse_area[verse_start:]), locator, "source-text")
            if explanation:
                add(section[explanation.start():], f"{locator} · editorial explanation", "editorial-note")
            synopsis = section[:verse_start] if verse_start >= 0 else section
            add(synopsis, f"{locator} · editorial synopsis", "editorial-note")

    return segments


def source_segments(path):
    path = Path(path)
    if path.suffix.lower() != ".xml":
        text = path.read_text(encoding="utf-8")
        start = re.search(r"\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG.*?\*\*\*", text, re.I)
        end = re.search(r"\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG", text, re.I)
        text = text[start.end() if start else 0:end.start() if end else len(text)]
        # Riley's Ovid files include a contents page with Roman-numbered book
        # synopses before the actual "BOOK THE FIRST/SECOND..." text. Prefer
        # those actual headings and keep editorial apparatus out of primary
        # retrieval and quotation verification.
        ordinals = "FIRST SECOND THIRD FOURTH FIFTH SIXTH SEVENTH EIGHTH NINTH TENTH ELEVENTH TWELFTH THIRTEENTH FOURTEENTH FIFTEENTH"
        ovid_headings = list(re.finditer(r"^BOOK THE (" + "|".join(ordinals.split()) + r")\.?\s*$", text, re.M | re.I))
        if ovid_headings and path.name.startswith("ovid-metamorphoses-books-"):
            return _plain_ovid_segments(text, ovid_headings)
        headings = list(re.finditer(r'^BOOK ([IVXLC]+)\.?[ \t]*$', text, re.M))
        if headings:
            def roman(value):
                numbers = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
                return sum(-numbers[c] if i + 1 < len(value) and numbers[c] < numbers[value[i + 1]] else numbers[c] for i, c in enumerate(value))
            return [{'text': normalize(text[heading.end():headings[i + 1].start() if i + 1 < len(headings) else len(text)]), 'locator': f'Book {roman(heading[1])}', 'evidenceType': 'source-text'} for i, heading in enumerate(headings)]
        return [{"text": normalize(text), "locator": "local text", "evidenceType": "source-text"}]
    root = ET.parse(path).getroot()
    segments = []

    def visit(node, location):
        kind = node.get("subtype")
        if kind in {"book", "chapter", "section"}:
            location = [*location, f"{kind} {node.get('n', '?')}"]
        if kind == "section":
            locator = " · ".join(location)
            segments.append({"text": normalize(_primary_text(node)), "locator": locator, "evidenceType": "source-text"})
            # Translator notes must not inherit the authority of the ancient primary text.
            for index, note in enumerate(n for n in node.iter() if _tag(n) == "note"):
                segments.append({"text": normalize("".join(note.itertext())), "locator": f"{locator} · editorial note {index + 1}", "evidenceType": "editorial-note"})
            return
        for child in node:
            visit(child, location)

    visit(root, [])
    if not segments:
        body = next((node for node in root.iter() if _tag(node) == 'body'), root)
        segments.append({"text": normalize(_primary_text(body)), "locator": "local XML text", "evidenceType": "source-text"})
    return segments


@lru_cache(maxsize=128)
def source_text(path):
    return " ".join(item["text"] for item in source_segments(path) if item["evidenceType"] == "source-text")


def check_reference(ref, root):
    kind = ref.get("evidenceType")
    if kind not in {"quotation", "paraphrase"}:
        return ["evidenceType must explicitly distinguish quotation from paraphrase"]
    text = source_text(root / ref["localPath"])
    quote = ref["excerpt"] if kind == "quotation" else ref.get("evidenceQuote", "")
    if not quote or normalize(quote) not in text:
        return ["quotation/evidenceQuote is not verbatim in the primary source text"]
    anchor = re.search(r';\s*(.*?), normalized characters (\d+)-(\d+)$', ref['locator'])
    if anchor:
        segment = next((item for item in source_segments(root / ref['localPath']) if item['locator'] == anchor[1] and item['evidenceType'] == 'source-text'), None)
        if not segment or segment['text'][int(anchor[2]):int(anchor[3])] != normalize(quote):
            return ['local character locator does not select the quoted passage']
    lines = re.search(r'local text file lines (\d+)-(\d+)', ref['locator'])
    if lines:
        raw = (root / ref['localPath']).read_text(encoding='utf-8').splitlines()
        if normalize(quote) not in normalize(' '.join(raw[int(lines[1]) - 1:int(lines[2])])):
            return ['physical-file locator does not contain the quoted passage']
    return []
