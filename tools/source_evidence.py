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


def _plain_homer_segments(text, work_name):
    """Separate Homeric verse from prose book summaries and chapter headings."""
    segments = []
    headings = list(re.finditer(r"^BOOK ([IVXLCDM]+)\.?[ \t]*$", text, re.M))

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    def roman_number(value):
        units = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
        return sum(
            -units[c] if i + 1 < len(value) and units[c] < units[value[i + 1]] else units[c]
            for i, c in enumerate(value)
        )

    for index, heading in enumerate(headings):
        book = roman_number(heading.group(1).upper())
        stop = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        body = text[heading.end():stop]
        cursor = 0
        if work_name == "The Iliad":
            paragraph = re.search(r"\S[^\n]*(?:\n(?!\s*\n)[^\n]*)*", body)
            if paragraph and "—" in paragraph.group():
                add(paragraph.group(), f"Book {book} · editorial summary", "editorial-note")
                cursor = paragraph.end()
        else:
            lines = body.splitlines(keepends=True)
            offset = 0
            heading_start = None
            heading_end = None
            for line in lines:
                if not line.strip():
                    offset += len(line)
                    continue
                if heading_start is None and line.strip().isupper() and len(line.strip()) > 8:
                    heading_start = offset
                    heading_end = offset + len(line)
                    offset += len(line)
                    continue
                if heading_start is not None and line.strip().isupper():
                    heading_end = offset + len(line)
                    offset += len(line)
                    continue
                break
            if heading_start is not None:
                add(body[heading_start:heading_end], f"Book {book} · editorial heading", "editorial-note")
                cursor = heading_end
        add(body[cursor:], f"Book {book}", "source-text")
    if headings:
        add(text[:headings[0].start()], f"{work_name} · front matter and contents", "editorial-note")
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


def _plain_mesoamerican_segments(path, text):
    """Keep Lewis Spence's regional chapters distinct from his reference matter."""
    segments = []
    chapters = list(re.finditer(r"^\s*CHAPTER ([IVXLCDM]+)(?::\s*(.*))?\s*$", text, re.I | re.M))
    end = re.search(r"^\s*(?:BIBLIOGRAPHY|INDEX AND GLOSSARY)\s*$", text, re.I | re.M)

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    if not chapters:
        return segments
    for index, chapter in enumerate(chapters):
        start = chapter.start()
        stop = chapters[index + 1].start() if index + 1 < len(chapters) else (end.start() if end and end.start() > start else len(text))
        lines = text[chapter.end():stop].splitlines()
        title = chapter.group(2).strip() if chapter.group(2) else next((line.strip() for line in lines if line.strip()), "Untitled")
        add(text[start:stop], f"Chapter {chapter.group(1).upper()} · {title}", "source-text")
    add(text[:chapters[0].start()], "Spence edition · front matter and contents", "editorial-note")
    if end:
        add(text[end.start():], "Spence edition · bibliography and index", "editorial-note")
    return segments


def _plain_gold_coast_folktale_segments(text):
    """Keep Barker and Sinclair's named tale retellings separate from their introduction."""
    segments = []
    start = text.find("I. ANANSI, OR SPIDER, TALES", 20000)
    if start < 0:
        return segments
    headings = list(re.finditer(r"^\s*([IVXLCDM]+)\.\s+(.+?)\s*$", text[start:], re.M))
    stories = [
        item for item in headings
        if item.group(2).strip().upper() not in {"ANANSI, OR SPIDER, TALES", "MISCELLANEOUS TALES"}
    ]

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    add(text[:start], "Barker and Sinclair edition · introduction and contents", "editorial-note")
    for index, heading in enumerate(stories):
        section_start = start + heading.start()
        section_end = start + stories[index + 1].start() if index + 1 < len(stories) else len(text)
        locator = f"Story {heading.group(1).upper()} · {heading.group(2).strip()}"
        add(text[section_start:section_end], locator, "source-text")
    return segments


def _plain_popol_vuh_spence_segments(text):
    """Separate Spence's K'iche' tale summaries from his comparative commentary."""
    segments = []
    headings = [
        (r"THE FIRST BOOK", "Spence summary · First Book", "source-text"),
        (r"THE MYTH OF VUKUB-CAKIX", "Spence summary · Vukub-Cakix", "source-text"),
        (r"THE SECOND BOOK", "Spence summary · Second Book", "source-text"),
        (r"THE THIRD BOOK", "Spence summary · Third Book", "source-text"),
        (r"THE FOURTH BOOK", "Spence summary · Fourth Book", "source-text"),
        (r"COSMOGONY OF THE [\"']POPOL VUH[\"']", "Spence commentary · Cosmogony", "editorial-note"),
        (r"THE PANTHEON OF THE [\"']POPOL VUH[\"']", "Spence commentary · Pantheon", "editorial-note"),
        (r"THE VUKUB-CAKIX MYTH", "Spence commentary · Vukub-Cakix", "editorial-note"),
        (r"THE HARRYING OF XIBALBA", "Spence commentary · Xibalba", "editorial-note"),
    ]
    matches = []
    for pattern, locator, kind in headings:
        match = re.search(r"^\s*" + pattern + r"\s*$", text, re.I | re.M)
        if match:
            matches.append((match.start(), match, locator, kind))
    matches.sort(key=lambda item: item[0])

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    if not matches:
        return segments
    add(text[:matches[0][0]], "Spence edition · preface and source history", "editorial-note")
    for index, (_, match, locator, kind) in enumerate(matches):
        stop = matches[index + 1][0] if index + 1 < len(matches) else len(text)
        add(text[match.end():stop], locator, kind)
    return segments


def _plain_gold_coast_folktale_segments(text):
    """Separate Dayrell's named story retellings from collection front matter."""
    segments = []
    heading_pattern = re.compile(r"^\s*([IVXLCDM]+)\.\s+(.+?)\s*$", re.M)
    body_start = text.find("I. ANANSI, OR SPIDER, TALES", 20000)
    if body_start < 0:
        return segments
    headings = [match for match in heading_pattern.finditer(text, body_start)]
    story_headings = [
        match for match in headings
        if match.group(2).strip().upper() not in {"ANANSI, OR SPIDER, TALES", "MISCELLANEOUS TALES"}
    ]

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    add(text[:body_start], "Barker and Sinclair edition · introduction and contents", "editorial-note")
    for index, heading in enumerate(story_headings):
        stop = story_headings[index + 1].start() if index + 1 < len(story_headings) else len(text)
        locator = f"Story {heading.group(1).upper()} · {heading.group(2).strip()}"
        add(text[heading.start():stop], locator, "source-text")
    return segments


def _plain_westervelt_maui_segments(text):
    """Segment Westervelt's numbered Maui chapters while retaining his regional labels."""
    segments = []
    headings = list(re.finditer(r"(?m)^\s*([IVXLCDM]+)\.\s*$", text))
    if not headings:
        return segments
    actual = []
    for heading in headings:
        following = text[heading.end():].splitlines()
        title = next((line.strip() for line in following if line.strip()), "Untitled")
        if title.isupper() and len(title) > 3:
            actual.append((heading, title))

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    # The contents page uses titles on the same line; only the body has a bare
    # Roman-numeral heading followed by its chapter title.
    for index, (heading, title) in enumerate(actual):
        stop = actual[index + 1][0].start() if index + 1 < len(actual) else len(text)
        locator = f"Chapter {heading.group(1).upper()} · {title}"
        add(text[heading.start():stop], locator, "source-text")
    add(text[:actual[0][0].start()], "Westervelt edition · front matter and contents", "editorial-note")
    return segments


def _plain_rasmussen_greenland_segments(text):
    """Split Rasmussen's Greenland collection into named story readings."""
    segments = []
    body_markers = list(re.finditer(r"^\s*ESKIMO FOLK-TALES\s*$", text, re.I | re.M))
    body_marker = body_markers[-1] if body_markers else None
    end = re.search(r"^\s*NOTES\s*$", text, re.I | re.M)
    if not body_marker:
        return segments
    body_start = body_marker.start()
    body_end = end.start() if end and end.start() > body_start else len(text)
    headings = []
    offset = body_start
    for line in text[body_start:body_end].splitlines(keepends=True):
        title = line.strip()
        if len(title) > 3 and title.isupper() and not re.fullmatch(r"[IVXLCDM]+", title):
            headings.append((offset, title))
        offset += len(line)
    headings = [(position, title) for position, title in headings if title != "ESKIMO FOLK-TALES"]

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    if not headings:
        return segments
    add(text[:body_start], "Rasmussen edition · introduction and contents", "editorial-note")
    for index, (position, title) in enumerate(headings):
        stop = headings[index + 1][0] if index + 1 < len(headings) else body_end
        add(text[position:stop], title.title(), "source-text")
    if end:
        add(text[end.start():], "Rasmussen edition · notes", "editorial-note")
    return segments


def _plain_pyle_fairy_segments(text):
    """Separate Pyle's named tale retellings from the anthology apparatus."""
    stories = [
        "LITTLE SURYA BAI",
        "THE PRINCES AND THE FRIENDLY ANIMALS",
        "GRACIOSA AND PERCINET",
        "THE GIANT'S CLIFF",
        "THE STORY OF CONN-EDA",
        "THE BLUE BELT",
        "THE DUTIFUL DAUGHTER",
        "THE OAT CAKE",
        "THE DREAMER",
        "THE STORY OF HARKA",
        "SCHIPPEITARO",
        "EROS AND PSYCHE",
    ]
    headings = []
    for title in stories:
        matches = list(re.finditer(r"^\s*" + re.escape(title) + r"\.?\s*$", text, re.I | re.M))
        if matches:
            headings.append((matches[-1].start(), matches[-1], title))
    headings.sort(key=lambda item: item[0])
    segments = []

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    if not headings:
        return segments
    add(text[:headings[0][0]], "Pyle edition · front matter and contents", "editorial-note")
    for index, (start, heading, title) in enumerate(headings):
        stop = headings[index + 1][0] if index + 1 < len(headings) else len(text)
        add(text[start:stop], f"Pyle retelling · {title.title()}", "source-text")
    return segments


def _plain_webster_basque_segments(text):
    """Separate Webster's named collected tales from comparison and language essays."""
    start_match = re.search(r"^\s*I\.\-\-LEGENDS OF THE TARTARO\.\s*$", text, re.I | re.M)
    end = re.search(r"^\s*NOTES\s*$", text, re.I | re.M)
    if not start_match:
        return []
    body_end = end.start() if end and end.start() > start_match.start() else len(text)
    headings = [
        match for match in re.finditer(r"^\s*([A-Z][A-Z0-9 .,\'\"()\-;\[\]—–]+)\s*$", text[start_match.start():body_end], re.M)
        if len(match.group(1).strip()) > 3
    ]
    segments = []
    editorial_headings = {
        "I.--LEGENDS OF THE TARTARO.",
        "II--THE HEREN-SUGE.--THE SEVEN-HEADED SERPENT.",
        "III.--ANIMAL TALES.",
        "IV.--BASA-JAUN, BASA-ANDRE, AND LAMIÑAK.",
        "V.--WITCHCRAFT AND SORCERY.",
        "VI.--CONTES DES FÉES.",
        "VII.--RELIGIOUS TALES.",
        "AN ESSAY ON THE BASQUE LANGUAGE,",
        "BASQUE POETRY.",
        "SUGGESTED EXPLANATION OF THE ABOVE TALE (THE LADY-PIGEON AND HER COMB).",
        "NOTES",
    }

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    add(text[:start_match.start()], "Webster edition · introduction and contents", "editorial-note")
    offset = start_match.start()
    for index, heading in enumerate(headings):
        title = heading.group(1).strip()
        absolute_start = start_match.start() + heading.start()
        absolute_end = start_match.start() + (headings[index + 1].start() if index + 1 < len(headings) else body_end - start_match.start())
        kind = "editorial-note" if title in editorial_headings or title.startswith("VARIATION") else "source-text"
        add(text[absolute_start:absolute_end], title, kind)
    if end:
        add(text[end.start():], "Webster edition · notes and back matter", "editorial-note")
    return segments


def _plain_ellis_yoruba_segments(text):
    """Scope Ellis's 1894 Yoruba survey to its transcribed chapters.

    The contents page repeats every chapter heading (including chapters X-XII,
    which the archive did not transcribe), so a CHAPTER line only opens a
    segment when the next non-empty line is not another CHAPTER entry."""
    chapters = []
    # Body headings end with a period; contents-page entries do not.
    for match in re.finditer(r"(?m)^CHAPTER ([IVXLC]+)\. (.+?)\.\s*$", text):
        rest = text[match.end():]
        next_line = next((line.strip() for line in rest.splitlines() if line.strip()), "")
        if next_line.startswith("CHAPTER "):
            continue
        chapters.append((match.start(), match.group(1), match.group(2).rstrip(".").strip()))
    if not chapters:
        return []
    segments = []

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    add(text[:chapters[0][0]], "Ellis edition · title page and contents", "editorial-note")
    for index, (position, number, title) in enumerate(chapters):
        stop = chapters[index + 1][0] if index + 1 < len(chapters) else len(text)
        add(text[position:stop], f"Chapter {number} · {title}", "source-text")
    return segments


def _plain_yoruba_legends_segments(text):
    """Split Ogumefu's 1929 collection into its forty named legends.

    Body headings read "IX ORISA OKO"; the contents page writes the same titles
    as "IX.TITLE<page>" without a space, so it cannot open a false boundary.
    Ogumefu's own preface remains quotable source text, while the title page,
    contents, and the STORIES OF TORTOISE divider are editorial apparatus."""
    boundaries = [
        (match.start(), f"Legend {match.group(1)} · {match.group(2).strip()}", "source-text")
        for match in re.finditer(r"(?m)^([IVXLC]{1,7}) ([A-Z][A-Z0-9 .,'\"()\u2018\u2019\u201c\u201d\-!?]+)\s*$", text)
    ]
    divider = re.search(r"(?m)^STORIES OF TORTOISE\s*$", text)
    if divider:
        boundaries.append((divider.start(), "Section divider · STORIES OF TORTOISE", "editorial-note"))
    boundaries.sort()
    if not boundaries:
        return []
    segments = []

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    front = text[:boundaries[0][0]]
    preface = re.search(r"(?m)^PREFACE\s*$", front)
    contents = re.search(r"(?m)^CONTENTS\s*$", front)
    if preface and contents and preface.start() < contents.start():
        add(front[:preface.start()], "Ogumefu edition · title page", "editorial-note")
        add(front[preface.start():contents.start()], "Preface", "source-text")
        add(front[contents.start():], "Ogumefu edition · contents", "editorial-note")
    else:
        add(front, "Ogumefu edition · front matter", "editorial-note")
    for index, (position, locator, kind) in enumerate(boundaries):
        stop = boundaries[index + 1][0] if index + 1 < len(boundaries) else len(text)
        add(text[position:stop], locator, kind)
    return segments


def _plain_mooney_cherokee_segments(text):
    """Separate Mooney's numbered Cherokee narratives from his ethnographic apparatus."""
    starts = list(re.finditer(r"(?m)^\s*V--THE MYTHS\s*$", text, re.I))
    start = starts[-1] if starts else None
    if not start:
        return []
    end = re.search(r"(?m)^\s*VI--NOTES AND PARALLELS TO MYTHS\s*$", text[start.end():], re.I)
    body_end = start.end() + end.start() if end else len(text)
    headings = []
    offset = start.start()
    for line in text[start.start():body_end].splitlines(keepends=True):
        match = re.match(r"^\s*(\d{1,3})\.\s+(.+?)\s*$", line)
        title = match.group(2).strip() if match else ""
        if match and len(title) > 3 and title.isupper():
            headings.append((offset + match.start(), match.group(1), title))
        offset += len(line)
    segments = []

    def add(value, locator, evidence_type):
        value = normalize(value)
        if value:
            segments.append({"text": value, "locator": locator, "evidenceType": evidence_type})

    add(text[:start.start()], "Mooney edition · introduction, history, and contents", "editorial-note")
    for index, (position, number, title) in enumerate(headings):
        stop = headings[index + 1][0] if index + 1 < len(headings) else body_end
        add(text[position:stop], f"Myth {number} · {title}", "source-text")
    if end:
        add(text[body_end:], "Mooney edition · notes and parallels", "editorial-note")
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
        if path.name in {"myths-mexico-peru-spence-53080.txt", "mythologies-mexico-peru-spence-36386.txt"}:
            return _plain_mesoamerican_segments(path, text)
        if path.name == "west-african-folk-tales-66923.txt":
            return _plain_gold_coast_folktale_segments(text)
        if path.name == "legends-ma-ui-westervelt-32601.txt":
            return _plain_westervelt_maui_segments(text)
        if path.name == "eskimo-folk-tales-28932.txt":
            return _plain_rasmussen_greenland_segments(text)
        if path.name == "fairy-tales-far-near-66919.txt":
            return _plain_pyle_fairy_segments(text)
        if path.name == "basque-legends-webster-34902.txt":
            return _plain_webster_basque_segments(text)
        if path.name == "myths-cherokee-mooney-45634.txt":
            return _plain_mooney_cherokee_segments(text)
        if path.name == "yoruba-speaking-peoples-ellis-1894.txt":
            return _plain_ellis_yoruba_segments(text)
        if path.name == "yoruba-legends-ogumefu-1929.txt":
            return _plain_yoruba_legends_segments(text)
        if path.name == "popol-vuh-56550.txt":
            return _plain_popol_vuh_spence_segments(text)
        if path.name == "west-african-folk-tales-66923.txt":
            return _plain_gold_coast_folktale_segments(text)
        if path.name == "homer-iliad-2199.txt":
            return _plain_homer_segments(text, "The Iliad")
        if path.name == "homer-odyssey-1727.txt":
            return _plain_homer_segments(text, "The Odyssey")
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
