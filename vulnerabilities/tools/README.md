# Tools

The scripts behind this Panama-only run of global-law's vulnerability detectors. They run inside a copy of
[global-law/vulnerabilities/scripts](https://github.com/lexifina/global-law/tree/main/vulnerabilities/scripts) (Python 3.11+,
`pip install duckdb pyarrow`), with a bare clone of this repository at `sources/corpus/panama-law.git`, a blobless bare
clone of global-law at `sources/global-law.git`, and a `pins.json` that names only panama-law, its commit and its
language (`es`). `build_vulns.py`, `flags_chart.py`, `late_ext_select.py`, `late_ext_rebut.py`, `patch_pa.py`,
`page_lines.py` and `config.json` sit two folders above the scripts.

| Script | What it does |
| --- | --- |
| `run.sh` | Indexes the history and texts, maps paths to the folders since the move (`map_moved.py`), adds this repository's history rows, and runs the detectors (`bash run.sh <shards>`) |
| `add_root.py` | Builds the history rows from this repository's own commits (global-law replays it only up to an earlier commit), so the history detectors read every change |
| `map_moved.py` | Rewrites the paths in the history table to each act's folder since the move of 10 November 2026 (`data/paths.json`), so that an act's history is not split in two at the move; `run.sh` runs it after the history is indexed |
| `run_triage.sh` | The model review: the 40 strongest flags per category, the 40 strongest lapsed time limits in law texts, and the empty periods (here none) |
| `late_ext_select.py` | Chooses the empty periods for global-law's review of that category (here there were none) |
| `late_ext_rebut.py` | Adds the second, arguing-against pass to the empty-period review, as `triage.py` does for the other categories |
| `build_vulns.py` | Builds `data/flags.csv`, `data/reviewed.csv` and `data/by_category.csv` from the findings and the model review |
| `flags_chart.py` | Draws the chart at the top of the READMEs, in Spanish and English, light and dark |
| `config.json` | The repository, the Spanish category names, the folders and files that are not law, and the chart's labels |
| `patch_detectors.py` | Fixes blind spots found in runs on several country repositories in the copy of global-law's scripts (`python -X utf8 patch_detectors.py <scripts dir>`; a fix already in place is skipped) |
| `patch_detectors_vi.py`, `patch_es.py`, `patch_ca.py`, `patch_en.py`, `patch_de.py`, `patch_en_et.py`, `patch_co.py`, `patch_sv.py`, `patch_pt.py`, `patch_ru.py`, `patch_r18.py`, `patch_xk.py`, `patch_mo.py`, `patch_lu.py`, `patch_li.py`, `patch_mx.py`, `patch_mn.py`, `patch_mt.py`, `patch_np.py`, `patch_en_nr.py`, `patch_dv.py`, `patch_az.py`, `patch_ar.py`, `patch_en_nz.py`, `patch_nb.py`, `patch_mk.py` | The same for the Vietnamese, Spanish, Catalan, English, German, Colombian, Salvadoran, Brazilian, Russian, Kosovar, Macanese, Luxembourg, Liechtenstein, Mexican, Mongolian, Maltese, Nepalese, Nauruan, Maldivian, Azerbaijani, Omani, New Zealand, Norwegian and Macedonian blind spots and a round on currencies, found by other runs; this run's copy carries them all. Of them, the Spanish, Colombian, Salvadoran and Mexican date forms ("hasta el día 31 de diciembre de 2020", "1o. de enero", "hasta el treinta (30) de junio de 1982", "a más tardar el 31 de diciembre de 2020") also serve Panamanian Spanish |
| `patch_pa.py` | The two fixes below, made for this repository |
| `apply_patches.py` | Applies every patch above once, in order (`patch_pa.py` last), recording each in `.kit_patches.json` beside the scripts so that none runs twice (`python -X utf8 apply_patches.py <scripts dir>`) |
| `redo.py` | Runs the patches, then again only the scans and detectors the fixes change, the model review of lapsed time limits, references to deleted provisions and empty periods, and the build (`python -X utf8 redo.py <run folder> [--keep-reviews] [--full]`; `--full` runs every step again through `run.sh`; `EMBED_FONTS` names the script that embeds the chart's fonts). It applies the patches through the `apply_patches.py` beside it, `patch_pa.py` among them; only `--full` runs the duplicate-numbering search again |
| `page_lines.py` | Hand-check helper: the page headers and footers left in article files ("G.O. 27,027-A", "ASAMBLEA NACIONAL, REPÚBLICA DE PANAMÁ"), and the laws whose commencement article sits in an earlier article's file (`python -X utf8 page_lines.py <bare repo> <sha>`; the counts in the README) |

The model review needs `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` and `LLM_AUTH` set for an OpenAI-compatible Responses API.
It was run as `bash run_triage.sh '^(data/|tools/|README|REPRODUCE|LICENSE|jurisdiction\.json)|/README\.md$'`. Every
lapsed time limit is in a law text, so the two reviews of that category drew the same 40 flags; `build_vulns.py` keeps the
later review of each flag (the first found no candidate defect, the second five, of which four survived).

Changes made for this repository:

- `add_root.py` needed no change: this repository marks its laws `Kind: law` and the oldest available text of the
  Constitution, the Criminal Code and the Labour Code `Kind: publisher`, both already counted as law: 781 of the 796
  commits. Of the other 15, 2 are documentation (`Kind: documentation`) and 13 carry no `In-force:` trailer. Each act
  has a single version, so the history detectors found nothing.
- `patch_pa.py`, duplicate numbering: the treaties that Panama's approving laws reproduce break lines before a
  reference, so a line can open with "Artículo 2 de este Acuerdo y la ruta ...", "Artículo 14, apartado 2 del
  mencionado Tratado", "Artículo 4.2)b), dicho domicilio;" or "Artículo 26 no incluye ...", which the search read as a
  second heading with that number. In a Spanish text, a line whose label is followed by a comma, a paragraph number with
  a bracket, or "de", "del", "y", "o", "no" (directly or after a bracketed title) is now read as a reference: 108 flags
  became 90. `detectors/dup_labels.py` was then run again, before the build; the model does not review this category.
- `patch_pa.py`, dead currencies: "francos" was read in any case, so "Victoriano Franco 67 soluciones habitacionales"
  (a peasant settlement in Veraguas and its 67 dwellings, Law 50 of 2001, Article 2) counted as 67 francs. The Spanish
  word is now read in lower case or in capitals only ("francos", "FRANCOS"): 2 flags became 1, the "15 francos oro" of
  the Athens Convention. `detectors/currency_scan.py` was then run again.
- `patch_nb.py` and `patch_mk.py` reached the kit after the first run; `apply_patches.py` applied them with `patch_pa.py`.
  Their changes to the scans read only Norwegian and Macedonian texts, and the duplicate-numbering and currency searches,
  which they also touch, were run again after them; no count changed.
- `flags_chart.py` takes a `tip1` from `config.json`, the tooltip for a category with one flag ("1 alerta", not
  "1 alertas"); English already had it.
- `config.json` counts as not law `data/`, `tools/` and the top-level files (`README`, `REPRODUCE.md`, `LICENSE`,
  `jurisdiction.json`), and each act's `README.md` (its list of provisions) wherever it is. `constitution/`, `code/` and
  `ley/` are law. It gives the chart shorter Spanish labels for the two reference categories, as Mexico's does.
- `pins.json` already named the language (`es`); Spanish month names were already in the time-limit search.
