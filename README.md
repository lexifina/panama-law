# Panama: law history in git

The law of Panama (PA) as a git history: one file per provision, one commit per law on the day it took effect, and the law that made the change as the commit author. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `pa/`.

**First build, deliberately small.** Language: Spanish (the official language).

| Folder | Text | Versions | History |
| --- | --- | ---: | --- |
| `constitucion/` | Constitución Política de la República de Panamá: preámbulo and articles 1 to 328 | 1 | Oldest version available: the Texto Único of Gaceta Oficial 25176, 15 November 2004 (the 1972 Constitution as amended to 2004) |
| `codigo-penal/` | Código Penal de la República de Panamá (Texto Único): articles 1 to 458 (article 282 is absent from the source) | 1 | Oldest version available: the Procuraduría General de la Nación's Texto Único incorporating Ley 70 de 2019, dated 11 December 2019 (the PDF's creation date) |
| `codigo-procesal-penal/` | Código Procesal Penal (Ley 63 de 2008): articles 1 to 560, as enacted | 1 | The text published in Gaceta Oficial 26114 of 29 August 2008, dated 2 September 2009 by its art. 560; later laws that postponed its entry into force and amended it are not applied |
| `codigo-del-trabajo/` | Código del Trabajo (Decreto de Gabinete 252 de 1971): articles 1 to 1067 | 1 | Oldest version available: the Ministerio de Trabajo / OIT edition with the changes of Ley 44 de 1995, dated 26 June 2003 (the edition's file date); later reforms are not applied |

**Códigos.** The Código Penal comes from the Procuraduría General de la Nación (ministeriopublico.gob.pa), born-digital PDF, retrieved 30 October 2026. The Código Procesal Penal is the Gaceta Oficial 26114 text in the Asamblea Nacional's Legispan record as published by the Órgano Judicial (organojudicial.gob.pa), read from an Internet Archive copy on 30 October 2026. The Código del Trabajo is the Ministerio de Trabajo y Desarrollo Laboral / OIT (Proyecto MATAC) edition published by the Órgano Judicial, also read from an Internet Archive copy; its editor's notes on reforms are not reproduced. The Código Civil and the Código de Comercio (Ley 2 de 1916) are not included yet: no official copy with a usable text layer was found.

**Why only this.** Panama's gazette (gacetaoficial.gob.pa) and Legispan publish each norm as enacted, with no consolidated text and no dated versions, so a statute history cannot be built from them without guessing. The Asamblea Nacional publishes the current Constitution as a born-digital PDF, so that is the first text recorded. Earlier texts (1972 and the reforms of 1978, 1983, 1993, 1994) are not available as separate versions here, so the history starts at this version.

**Source:** [Asamblea Nacional de Panamá](https://asamblea.gob.pa), official, edition of April 2024, retrieved 29 October 2026. See `LICENSE` and `REPRODUCE.md`.

Dates are the day the change took effect. This repository is not legal advice; for anything that matters, read the original.
