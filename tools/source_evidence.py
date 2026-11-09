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


def _plain_mesopotamian_segments(path, text):
    """Keep tablet translations distinct from transliterations and scholarship."""
    segments = []
    columns = re.compile(
        r"^\s*(?:COL(?:UMN)?\.?\s+(I|II|III|IV|V|VI)\.?|REVERSE\s+(I|II|III|IV))\s*$",
        re.I | re.M,
    )
    lacuna = re.compile(r"^\s*\((?:About|Perhaps).*(?:missing|broken away).*\)\s*$", re.I | re.M)

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    def add_translated_column(value, locator):
        """Keep editorial lacuna notices out of the translated tablet text."""
        cursor = 0
        part = 0
        for gap in lacuna.finditer(value):
            add(value[cursor:gap.start()], f"{locator} · part {part + 1}", "source-text")
            add(gap.group(), f"{locator} · editorial lacuna notice", "editorial-note")
            cursor = gap.end()
            part += 1
        add(value[cursor:], f"{locator} · part {part + 1}" if part else locator, "source-text")

    def add_columns(verse, edition, prefix_is_column_one=False):
        found = list(columns.finditer(verse))
        seen = {}
        if found:
            prefix = verse[:found[0].start()]
            if prefix_is_column_one and prefix.strip():
                add_translated_column(prefix, f"{edition} · Column I")
            else:
                add(prefix, f"{edition} · editorial preface", "editorial-note")
        elif prefix_is_column_one:
            add_translated_column(verse, f"{edition} · Column I")
            return
        else:
            add(verse, f"{edition} · translation", "source-text")
            return
        for index, column in enumerate(found):
            stop = found[index + 1].start() if index + 1 < len(found) else len(verse)
            if column.group(1):
                name = f"Column {column.group(1).upper()}"
            else:
                name = f"Reverse {column.group(2).upper()}"
            seen[name] = seen.get(name, 0) + 1
            suffix = f" · fragment {seen[name]}" if seen[name] > 1 else ""
            add_translated_column(verse[column.end():stop], f"{edition} · {name}{suffix}")

    if path.name == "gilgamesh-clay-jastrow-11000.txt":
        editions = [
            ("Pennsylvania Tablet", "PENNSYLVANIA TABLET", "COMMENTARY ON THE PENNSYLVANIA TABLET"),
            ("Yale Tablet", "YALE TABLET.", "CORRECTIONS TO THE TEXT OF LANGDON"),
        ]
        translation_spans = []
        speech = re.search(r"Why, O Gish, does thou run about\?.*?Let the wife rejoice in thy bosom!", text, re.S)
        if speech:
            add(speech.group(), "Old Babylonian Tablet X fragment · Sabitum's speech quoted in the introduction", "source-text")
        for label, start_marker, end_marker in editions:
            start = re.search(r"^" + re.escape(start_marker) + r"\s*$", text, re.I | re.M)
            if not start:
                continue
            end = re.search(r"^" + re.escape(end_marker) + r".*$", text[start.end():], re.I | re.M)
            section_end = start.end() + end.start() if end else len(text)
            section = text[start.end():section_end]
            heading = re.search(r"^TRANSLATION\.?\s*$", section, re.I | re.M)
            if not heading:
                continue
            verse_start = start.end() + heading.end()
            translation_spans.append((start.start(), section_end))
            verse = text[verse_start:section_end]
            add_columns(verse, label)
        # All material outside the translated tablet passages is introduction,
        # transliteration, commentary, correction, or edition apparatus.
        cursor = 0
        notes = []
        for start, stop in translation_spans:
            notes.append(text[cursor:start])
            cursor = stop
        notes.append(text[cursor:])
        editorial = "\n".join(notes)
        if speech:
            editorial = editorial.replace(speech.group(), "")
        add(editorial, "Jastrow and Clay edition · editorial apparatus", "editorial-note")
    elif path.name == "gilgamish-langdon-18897.txt":
        heading = re.search(r"^TRANSLATION\.?\s*$", text, re.I | re.M)
        end = re.search(r"^INDEX TO PARTS 2 AND 3\s*$", text, re.I | re.M)
        if heading and end and end.start() > heading.end():
            verse = text[heading.end():end.start()]
            add_columns(verse, "Langdon edition", prefix_is_column_one=True)
            add(text[:heading.start()] + text[end.start():], "Langdon edition · introduction, notes, and apparatus", "editorial-note")

    return segments


def _plain_chinese_segments(path, text):
    """Keep modern Chinese mythology syntheses and tale collections section-scoped."""
    segments = []

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    if path.name == "myths-legends-china-werner-15250.txt":
        chapters = list(re.finditer(r"^\s*CHAPTER ([IVXLCDM]+)\s*$", text, re.I | re.M))
        notes = re.search(r"^\s*NOTES\s*$", text, re.I | re.M)
        for index, chapter in enumerate(chapters):
            start = chapter.start()
            stop = chapters[index + 1].start() if index + 1 < len(chapters) else len(text)
            if notes and notes.start() > start:
                stop = min(stop, notes.start())
            lines = text[chapter.end():stop].splitlines()
            title = next((line.strip() for line in lines if line.strip()), "Untitled")
            locator = f"Chapter {chapter.group(1).upper()} · {title}"
            add(text[start:stop], locator, "source-text")
        if chapters:
            add(text[:chapters[0].start()], "Werner edition · preface and contents", "editorial-note")
            if notes:
                add(text[notes.start():], "Werner edition · notes", "editorial-note")
    elif path.name == "chinese-folk-lore-tales-macgowan-26070.txt":
        headings = list(re.finditer(r"^\s*([A-Z][A-Z0-9 ,.'\"()-]{3,})\s*$", text, re.M))
        # The contents page uses numbered entries; only exact unnumbered headings
        # in the body are treated as tale boundaries.
        body_headings = [item for item in headings if not re.match(r"\s*(?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI)\.", item.group(1))]
        story_start = next((index for index, heading in enumerate(body_headings) if heading.group(1).strip() == "THE WIDOW HO"), None)
        if story_start is None:
            return []
        add(text[:body_headings[story_start].start()], "Macgowan edition · front matter and contents", "editorial-note")
        for index, heading in enumerate(body_headings[story_start:]):
            start = heading.start()
            next_index = story_start + index + 1
            stop = body_headings[next_index].start() if next_index < len(body_headings) else len(text)
            locator = heading.group(1).strip()
            add(text[start:stop], locator, "source-text")

    return segments


def _plain_indian_epic_segments(path, text):
    """Scope Dutt's English epic renderings to named books and sections."""
    segments = []

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    if path.name == "mahabharata-dutt-19630.txt":
        books = list(re.finditer(r"^\s*BOOK ([IVXLCDM]+)\s*$", text, re.I | re.M))
        epilogue = re.search(r"^\s*TRANSLATOR'S EPILOGUE\s*$", text, re.I | re.M)
        for index, book in enumerate(books):
            start = book.start()
            stop = books[index + 1].start() if index + 1 < len(books) else (epilogue.start() if epilogue else len(text))
            lines = text[book.end():stop].splitlines()
            title = next((line.strip() for line in lines if line.strip()), "Untitled")
            add(text[start:stop], f"Book {book.group(1).upper()} · {title}", "source-text")
        if books:
            add(text[:books[0].start()], "Dutt edition · preface and introduction", "editorial-note")
            if epilogue:
                add(text[epilogue.start():], "Dutt edition · translator's epilogue and back matter", "editorial-note")
    elif path.name == "ramayana-vol1-dutt-57265.txt":
        # The front matter repeats both kanda headings in its table of contents;
        # the final heading occurrence marks the actual translated text.
        kanda_headers = []
        for name in ("BALAKANDAM\\.", "AYODHYAKANDAM"):
            matches = list(re.finditer(r"^\s*" + name + r"\s*$", text, re.I | re.M))
            if matches:
                kanda_headers.append(matches[-1])
        kanda_headers.sort(key=lambda item: item.start())
        sections = list(re.finditer(r"^\s*SECTION ([IVXLCDM]+)\.?\s*$", text, re.I | re.M))
        starts = []
        kanda_index = 0
        for section in sections:
            while kanda_index + 1 < len(kanda_headers) and kanda_headers[kanda_index + 1].start() < section.start():
                kanda_index += 1
            if kanda_headers and section.start() > kanda_headers[0].start():
                kanda_name = "Balakandam" if "BALAKANDAM" in kanda_headers[kanda_index].group(0).upper() else "Ayodhyakandam"
                starts.append((section, kanda_name))
        for index, (section, kanda) in enumerate(starts):
            stop = starts[index + 1][0].start() if index + 1 < len(starts) else len(text)
            locator = f"{kanda} · Section {section.group(1).upper()}"
            add(text[section.start():stop], locator, "source-text")
        if starts:
            add(text[:starts[0][0].start()], "Dutt Ramayana edition · front matter and translator's preface", "editorial-note")
            end = re.search(r"^\s*\*\*\*\s*END OF THE PROJECT GUTENBERG", text, re.I | re.M)
            if end and end.start() > starts[-1][0].start():
                tail = text[end.start():]
                add(tail, "Dutt Ramayana edition · end matter", "editorial-note")

    return segments


def _plain_kalevala_segments(text):
    """Separate Lönnrot's numbered runos from the modern edition's front matter."""
    segments = []
    headings = list(re.finditer(r"^\s*RUNE ([IVXLCDM]+)\.?\s*$", text, re.I | re.M))
    if not headings:
        return segments
    first_actual = min(item.start() for item in headings)
    last_by_rune = {}
    for heading in headings:
        last_by_rune[heading.group(1).upper()] = heading
    ordered = sorted(last_by_rune.values(), key=lambda item: item.start())

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    toc = text[:first_actual]
    for index, heading in enumerate(ordered):
        stop = ordered[index + 1].start() if index + 1 < len(ordered) else len(text)
        roman = heading.group(1).upper()
        title_match = re.search(r"^\s*RUNE " + re.escape(roman) + r"\.\s+(.+?)\s*$", toc, re.I | re.M)
        title = title_match.group(1).strip() if title_match else "Untitled episode"
        add(text[heading.start():stop], f"Rune {roman} · {title}", "source-text")
    add(text[:first_actual], "Crawford edition · front matter and contents", "editorial-note")
    return segments


def source_segments(path):
    path = Path(path)
    if path.suffix.lower() != ".xml":
        text = path.read_text(encoding="utf-8")
        start = re.search(r"\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG.*?\*\*\*", text, re.I)
        end = re.search(r"\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG", text, re.I)
        text = text[start.end() if start else 0:end.start() if end else len(text)]
        if path.name in {"gilgamesh-clay-jastrow-11000.txt", "gilgamish-langdon-18897.txt"}:
            return _plain_mesopotamian_segments(path, text)
        if path.name in {"myths-legends-china-werner-15250.txt", "chinese-folk-lore-tales-macgowan-26070.txt"}:
            return _plain_chinese_segments(path, text)
        if path.name in {"mahabharata-dutt-19630.txt", "ramayana-vol1-dutt-57265.txt"}:
            return _plain_indian_epic_segments(path, text)
        if path.name in {"kalevala-crawford-5186.txt", "kalevala-vol1-crawford-5184.txt"}:
            return _plain_kalevala_segments(text)
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
