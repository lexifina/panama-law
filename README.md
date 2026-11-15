# Panama: law history in git


The law of Panama as a git history: one file per article, one commit per version on the day it took effect, and the act that made each change as the commit's author. `git blame` names the act behind every article; `git log` lists every change to an article; picking a date gives the text in force that day.

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is Panama's national law, which global-law reads at `panama/national/acts/`.

**What is in it now:** the Constitution, three codes (the Código Penal, the Código Procesal Penal and the Código del Trabajo) and 777 laws (leyes) of the Asamblea Nacional promulgated from 1932 to 2019, each act in one version. The laws are those whose Legispan record lists no norm that modifies, repeals, suspends or regulates them, so the text as enacted is also the text in force. [`data/versions.json`](data/versions.json) lists every act with its versions; [`data/paths.json`](data/paths.json) maps each act id to its folder.

Each act is a folder `<kind>/<year>/<number>/` with one file per article and a `README.md` listing them (`ley/2010/0045/` is Ley 45 de 2010, with the text before Artículo 1 in `encabezado.md` and the closing formula in `firma.md`); the Constitution is [`constitution/constitucion/`](constitution/constitucion/) and the codes are under `code/` (`code/codigo-del-trabajo/` is the Código del Trabajo, Decreto de Gabinete 252 de 1971). The folders took these names on 2026-11-10 (commit `51cde9a`, no change of law): `git log` needs `--follow` to reach a file's earlier name, and `tools/on.py` reads both.

The text is in Spanish, as the sources print it. An English translation is not part of this record.

## Questions as git commands

| Question | Command |
| --- | --- |
| Every change to Article 54 of the Código del Trabajo (vacations) | `git log -p --follow --word-diff -- code/codigo-del-trabajo/art-054.md` |
| Which act wrote each line of Article 54? | `git blame code/codigo-del-trabajo/art-054.md` |
| Every version of the Código del Trabajo, with the day each took effect | `git log --no-walk --tags="codigo-del-trabajo/*" --format="%h %(trailers:key=In-force,valueonly,separator=) %an"` |
| Article 54 as in force on 1 January 2015 | `python tools/on.py 2015-01-01 codigo-del-trabajo art-054` |

**Outside git**, we also host this record publicly, for free:

- **[Ask Claude about Panamanian law](https://global-law.lexifina.com/v1/try_claude?country=panama)**: opens Claude with a first question ready.
- **[Ask ChatGPT](https://global-law.lexifina.com/v1/try_chatgpt?country=panama)**: the same question in ChatGPT.
- **[Search Panamanian law on our site](https://lexifina.com/law?country=panama&q=vacaciones)**: a search for "vacaciones" (annual leave), with each provision's text and its versions, no account needed.
- **[Developer REST API](https://global-law.lexifina.com/v1/search_law?query=vacaciones&jurisdiction=panama)**: the same search as JSON, with no key. See the [documentation here](https://lexifina.com/api/global-law).

Both assistants read the record through the free Global law connector (MCP, `https://global-law.lexifina.com/mcp`); the first time, the chat gives you the link that adds it. Ask in Spanish or in English.

**Host it yourself easily.** All it takes is git and Python, and the tools run on your machine:

```sh
git clone --depth 1 https://github.com/lexifina/global-law && cd global-law
python3 tools/countries.py add panama/national/acts
python3 tools/law.py show 2026-01-01 panama/national/acts/code/codigo-del-trabajo/art-054.md
```

Opened in Claude Code, Cursor, VS Code or Codex, the clone also starts a local MCP server with the same tools ([MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md)).

## Dates

Each commit is dated at noon, America/Panama, on the day the version took effect, and carries it in its `In-force:` trailer:

- for the 777 laws, the day of their promulgation in the Gaceta Oficial, as their Legispan record gives it; a later day a law sets for its own entry into force is not shown;
- for the Código Procesal Penal (Ley 63 de 2008), 2 September 2009, the day its art. 560 gives;
- for the Constitution, 15 November 2004, the day of the Gaceta Oficial (No. 25176) that published its Texto Único; for the Código Penal and the Código del Trabajo, the creation date of their source PDFs (11 December 2019 and 26 June 2003), as the sources give no date for the edition;
- git cannot store dates before 1970, so the 2 earlier commits (Ley 46 de 1932 and Ley 18 de 1959) are dated 1970-01-01, with the real day in `In-force:`. Ask for a date with `tools/on.py`, not `git log --before`.

Each law is credited to itself (`Ley 45 de 2010`), and the Código Procesal Penal to `Ley 63 de 2008`. The Constitution, the Código Penal and the Código del Trabajo are each the oldest version available as text, credited to the publisher as `Asamblea Nacional de Panamá` (`Kind: publisher`).

## How it is checked

- Every word of the Asamblea Nacional's typed edition of a law is in a file, in order, except the running header and page numbers; a law whose own articles are not numbered 1, 2, 3 and so on, each once, is left out.
- Only text layers are read: the scanned Gaceta pages are not read and no OCR is used; a law with no typed edition, or only an OCR layer, is left out.
- `tools/check_repo.py` reads every version back from git on its day and compares it with the corpus, and the same corpus gives the same commit hashes; [`REPRODUCE.md`](REPRODUCE.md) gives the corpus and builder hashes, but records no check run and no second build yet.
- History is append-only: no merge commits, and later changes (such as the folder move) are new commits on top.

## What it does not show

- **Laws Legispan records as modified, repealed, suspended or regulated**: they are left out until their current text can be shown, as are laws whose PDF has no typed edition, such as recent laws published only as Gaceta scans; none after 2019 is here yet.
- **Any act's changes over time.** Every act is one version: the Constitution's 1972 text and its reforms (1978, 1983, 1993, 1994) are not here; reforms after the 2003 edition of the Código del Trabajo are not applied; and the Código Procesal Penal is the text as enacted, without the later laws that amended it and postponed and staged its entry into force.
- **The Código Civil and the Código de Comercio**: no official copy with a usable text layer was found.
- **Executive decrees and other regulations, municipal acts and case law.**

## Sources

| Source | Kind | Past versions | Notes |
| --- | --- | --- | --- |
| [Asamblea Nacional de Panamá](https://asamblea.gob.pa) | Constitution, Texto Único (edition of April 2024) | no | Born-digital PDF, retrieved 29 October 2026 |
| [Legispan](https://legispan.asamblea.gob.pa/) (Asamblea Nacional) | Laws: the Gaceta Oficial pages and the Asamblea's typed edition | no, each law as enacted | Retrieved 3 November 2026; only the typed edition is read |
| [Procuraduría General de la Nación](https://ministeriopublico.gob.pa) | Código Penal, Texto Único with Ley 70 de 2019 | no | Born-digital PDF, retrieved 30 October 2026 |
| Órgano Judicial (organojudicial.gob.pa) | Código Procesal Penal (the Gaceta Oficial 26114 text), Código del Trabajo (Ministerio de Trabajo / OIT edition) | no | Read from Internet Archive copies on 30 October 2026; the Código del Trabajo editor's notes on reforms are not reproduced |

## Licence

See [`LICENSE`](LICENSE). None of the sources states a licence; the texts are reproduced without change to their wording, as the law of Panama, and the Asamblea Nacional does not endorse this repository. Lexifina's own contributions (the arrangement of the history, the commit messages and the tools) are CC0 1.0.

No AI model wrote, translated or corrected legal text, and none runs at build time; the scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (see [`REPRODUCE.md`](REPRODUCE.md)).

## More

From [lexifina/global-law](https://github.com/lexifina/global-law):

- [FEATURES.md](https://github.com/lexifina/global-law/blob/main/FEATURES.md): every feature, and what every corpus must support (`git blame`, `law.py`, the MCP tools)
- [FAQ.md](https://github.com/lexifina/global-law/blob/main/FAQ.md): questions and answers · [CONTRIBUTING.md](https://github.com/lexifina/global-law/blob/main/CONTRIBUTING.md): proposing changes · [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md): the MCP server · [REPRODUCE.md](https://github.com/lexifina/global-law/blob/main/REPRODUCE.md): how it was built · [CHANGELOG.md](https://github.com/lexifina/global-law/blob/main/CHANGELOG.md)
- [FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md): how current each corpus is · [Monitoring](https://github.com/lexifina/global-law/tree/main/monitoring): whether updates are running · [WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md): how each official source is watched for changes
- [performance/](https://github.com/lexifina/global-law/tree/main/performance): how fast the tools are, measured
- [visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations): charts and bridges across the world's law
- [Vulnerabilities](https://github.com/lexifina/global-law/tree/main/vulnerabilities): mistakes in legislation as published
