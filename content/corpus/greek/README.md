# Local Greek-myth source corpus

This directory stores selected full-text source editions locally for personal study and future retrieval. The collection is deliberately small at first; it is not a single “official” canon.

## Layout

- `primary/`: Greek and Hellenistic literary sources in older English translations or TEI-XML.
- `reception/`: later Roman retellings, kept separate from Greek evidence.
- `scholarship/`: older secondary works that are reusable but must be treated as interpretation, not primary evidence.
- `manifest.json`: source IDs, edition/translator details, remote provenance, rights status, and locator notes.

The `.txt` files are unmodified Project Gutenberg plain-text downloads and retain their original headers, credits, and license notices. Do not remove those notices. Project Gutenberg identifies its specific eBooks as public domain in the United States, but that label alone does not establish UK status. The separate translator copyrights were checked against the UK standard literary-work term of 70 years after the end of the author’s death year. The Perseus XML files declare CC BY-SA 4.0 in their TEI headers and are kept unmodified; if they are edited, preserve attribution/share-alike terms and follow the source’s instruction to offer modifications to Perseus.

UK guidance permits limited fair-dealing copying for non-commercial research or private study, but says copying a whole work would not generally be considered fair dealing. “No distribution” is therefore not a blanket basis for copying an otherwise protected book. At the user’s explicit request after this warning, three Gilbert Murray Euripides translations have been restored as `personal-local-only` records. They must not be redistributed, and generated/exported lessons should prefer the UK-cleared Buckley or Coleridge translations while Murray’s status remains uncertain. See the [GOV.UK copyright exceptions guidance](https://www.gov.uk/guidance/exceptions-to-copyright) and the rights fields in `manifest.json`. This is a working provenance policy, not legal advice.

## What is included

- Hesiod, *Theogony* and *Works and Days*, the *Homeric Hymns*, and related Homerica in the Evelyn-White anthology.
- Homer, *Iliad* and *Odyssey*, translated by Samuel Butler.
- Pindar, *The Extant Odes*, translated by Ernest Myers.
- Apollonius Rhodius, *Argonautica*, translated by R. C. Seaton.
- Pseudo-Apollodorus, *Bibliotheca* and *Epitome*, translated by James George Frazer and stored as Perseus TEI-XML under CC BY-SA 4.0.
- Plutarch, *Lives of the Noble Grecians and Romans*, in the Dryden translation tradition revised by Arthur Hugh Clough.
- Aeschylus, *House of Atreus* (*Agamemnon*, *Libation Bearers*, *Furies*), translated by E. D. A. Morshead.
- Sophocles, *Oedipus the King*, *Oedipus at Colonus*, and *Antigone*, translated by Francis Storr.
- Euripides, *Medea* and *Bacchae*, translated by Theodore Alois Buckley; *Trojan Women*, translated by Edward P. Coleridge and stored as Perseus TEI-XML under CC BY-SA 4.0.
- Euripides, *Medea*, *Bacchae*, and *Trojan Women*, translated by Gilbert Murray, stored as **personal-local-only** comparison copies at the user’s request.
- Ovid, *Metamorphoses*, translated by Henry T. Riley, Books I–XV, classified as **Roman reception**.
- James George Frazer, *Studies in Greek Scenery, Legend and History*, classified as **dated scholarship** selected from his Pausanias commentary.

These translations are valuable for access and comparison, but are old English renderings, not contemporary translations. They can differ in style, terminology, and interpretive choices. Lessons must cite the ancient work and locator, name the translation used, and avoid treating a translation’s wording as the Greek text itself.

## Citation and retrieval

- Cite the ancient work using its conventional locator (for example, *Iliad* 16 or *Theogony* 453–491).
- TEI-XML records carry structured CTS/Perseus locators and should be preferred when precise section retrieval matters.
- Some Project Gutenberg texts may not preserve ancient line numbering consistently. Use a stable book/section locator; when a specific line-level claim matters, cross-check against a scholarly edition or a separately licensed aligned text.
- Retrieval chunks should retain the source ID, work, book/section, translator, and eBook ID as metadata. Never separate a passage from its provenance.
- Keep Ovid tagged as Roman reception even when a later lesson compares its story with Greek sources.
- Keep Frazer tagged as scholarship and dated interpretation; do not use it as direct evidence for what an ancient source says.
- Records marked `personal-local-only` are for private comparison and retrieval context only. They should not be copied into generated lesson text, exports, screenshots, or any distributable package while their UK status is uncertain.

## Not included yet

This is not yet a full local scholarly library. Recent academic books and many modern translations are copyrighted; free online access is not the same as permission to copy. For those works, the repository currently keeps references and original research notes. Openly licensed academic material can be added later with its license and attribution recorded per item.
