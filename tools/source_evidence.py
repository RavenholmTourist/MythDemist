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


def source_segments(path):
    path = Path(path)
    if path.suffix.lower() != ".xml":
        text = path.read_text(encoding="utf-8")
        start = re.search(r"\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG.*?\*\*\*", text, re.I)
        end = re.search(r"\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG", text, re.I)
        text = text[start.end() if start else 0:end.start() if end else len(text)]
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
