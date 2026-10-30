# How this repository was made (Panama)

This file is written by the build on 2026-10-30, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Asamblea Nacional de Panamá, Constitución Política y Reglamento Orgánico del Régimen Interno (Edición 2024) | <https://asamblea.gob.pa/Uploads/GestorFiles/Reglamento_Organico_del_Regimen_Interno.pdf> | 2026-10-29 | No licence stated on the site |
| Procuraduría General de la Nación (Ministerio Público), Texto Único del Código Penal de la República de Panamá | <https://ministeriopublico.gob.pa/wp-content/uploads/2016/09/CODIGO-PENAL-2019-FINAL-1.pdf> | 2026-10-30 | No licence stated on the site. |
| Órgano Judicial de Panamá: Ley 63 de 2008, Código Procesal Penal (Legispan copy of Gaceta Oficial 26114) | <https://www.organojudicial.gob.pa/uploads/wp_repo/uploads/2016/11/C%C3%B3digo-Procesal-Penal.pdf> | 2026-10-30 | No licence stated; official legal text as published in the Gaceta Oficial. |
| Órgano Judicial de Panamá: Código del Trabajo (Decreto de Gabinete 252 de 1971, con las modificaciones de la Ley 44 de 1995), edición del Ministerio de Trabajo y Desarrollo Laboral (Proyecto MATAC / OIT) | <https://www.organojudicial.gob.pa/uploads/wp_repo/uploads/2016/11/c%C3%B3digo-detrabajo.pdf> | 2026-10-30 | No licence stated; official legal text. |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitucion` | Constitución Política de la República de Panamá | 1 | 2004-11-15 to 2004-11-15 |
| `codigo-penal` | Código Penal de la República de Panamá (Texto Único) | 1 | 2019-12-11 to 2019-12-11 |
| `codigo-procesal-penal` | Código Procesal Penal (Ley 63 de 2008) | 1 | 2009-09-02 to 2009-09-02 |
| `codigo-del-trabajo` | Código del Trabajo (Decreto de Gabinete 252 de 1971) | 1 | 2003-06-26 to 2003-06-26 |

The build made 4 commits:

| Commits | Kind |
| ---: | --- |
| 4 | first version of an act |
| 0 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-30.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 3 laws in the record.
- 5 tags.

## Dates

Each commit is dated at noon (America/Panama) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: This record dates the Constitution text by the Gaceta Oficial in which its Texto Único was published (No. 25176, 15 November 2004). https://asamblea.gob.pa

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `3f32cb2db5d1df4be72c76201ecb1107fff68875b72dc00d981dedb89cc0bd9c` (1618798 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3d00541d258745461ab52b1b0cb4e1716a27a95d`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

4 versions of 4 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

A second build from the same corpus into an empty folder gave identical hashes for all 4 history commits and 5 tags (history tip `a886e74540ad0d3ea9d4ffe597161a280b10d5f8`).

## Decisions made by hand

- Language: Spanish, the official language.
- No dated past versions are online, so there is one version, credited to the publisher as "oldest version available" and dated 15 November 2004, the Gaceta Oficial date of the current Texto Unico.
- Cleaning: page headers and footers, Title and Chapter headings, and the closing date-and-amendments note were removed; line breaks inside a paragraph were joined (hyphenated words rejoined); typographic quotes normalised. The preamble and articles 1 to 328 are kept.
- [statutes] Código Penal: one version, the Procuraduría's Texto Único incorporating Ley 70 de 2019, credited to the publisher as oldest version available and dated 11 December 2019, the PDF's own creation date (the source states no commencement date for the consolidation; the Code itself took effect one year after its promulgation, art. 458). Headings (Libro, Título, Capítulo) and page headers were removed; wrapped lines were joined.
- Código Procesal Penal: one version, the text of Ley 63 de 2008 as published in Gaceta Oficial 26114 of 29 August 2008, credited to Ley 63 de 2008 as enacted and dated 2009-09-02, the date its art. 560 gives. Later laws postponed that date and staged the Code's application by district (art. 557 already staged it), and amended the text; none of them is in this record, so this version is the enacted text, not the text in force today.
- Código Procesal Penal: one unit per article (art-001 to art-560); the epigraph stays at the start of each article. The enacting article ("Artículo Único"), headings, page headers, the closing formula and signatures are left out. Paragraphs follow the blank lines of the Gaceta text; numbered items are their own lines.
- Código del Trabajo: one version, the Ministerio de Trabajo y Desarrollo Laboral / OIT (Proyecto MATAC) edition published by the Órgano Judicial, credited to the publisher as "oldest version available" and dated 2003-06-26, the creation date of its PDF; it contains the changes of Ley 44 de 1995 and notes later reforms up to Ley 8 de 1998. Later reforms are not applied.
- Código del Trabajo: one unit per article (art-NNN, art-NNNN, lettered articles as art-197-a). The two-column pages are read column by column, and a heading set across both columns starts a new band. Paragraphs start at indented lines; words hyphenated at line ends are joined. Headings, running heads, page numbers, the index and the editor's notes "(Adicionado/Modificado/Subrogado/Derogado por ...)" are left out; the "Parágrafo" clauses stay with their article.
- Código del Trabajo: articles whose only text is a repeal note read "Derogado." (art-080, art-081, art-232, art-233, art-281, art-347); Capítulo VIII "Trabajo en el mar y en las vías navegables", printed as its heading and the note "(Derogado por el artículo 143 de la Ley No. 8 de 26 de febrero de 1998)", is the single unit art-251-278 reading "Derogados.". The source prints "Artículo 336" between 635 and 637 (keyed art-636) and two articles numbered 954 (the second keyed art-954-2); it has no article 541.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- none
- none
- none
