"""Add the Legispan laws (corpus.d/30-acts-*.json with a .PUBLISH) to repo/README.md, repo/LICENSE and
repo/jurisdiction.json, between markers. Deterministic; reads only the parts.

    python -X utf8 w3_docs.py
"""
import json
import re
from pathlib import Path

H = Path(__file__).resolve().parent
parts = sorted(p for p in (H / 'corpus.d').glob('30-acts-*.json') if p.with_suffix('.PUBLISH').exists())
acts = [a for p in parts for a in json.loads(p.read_text('utf-8'))['acts']]
acts.sort(key=lambda a: (a['versions'][0]['from'], a['slug']))
n = len(acts)
units = sum(len(a['versions'][0]['units']) for a in acts)
years = sorted({a['versions'][0]['from'][:4] for a in acts})
span = f'{years[0]} to {years[-1]}' if years else ''
A0, A1 = '<!-- acts:start -->', '<!-- acts:end -->'
rows = '\n'.join(f"| `{a['slug']}/` | [{a['title'].replace('|', '/')}]({a['url']}) | {a['versions'][0]['from']} |"
                 for a in acts)
SECTION = f"""{A0}
## Laws from Legispan, as enacted and never modified

{n} laws (leyes) of the Asamblea Nacional, promulgated {span}, {units:,} files: one folder per law, named by its year and number (`ley-2010-0045/` is Ley 45 de 2010). These are the laws whose record in Legispan, the Asamblea Nacional's legislation database, lists no norm that modifies, repeals, suspends or regulates them, so the text as enacted is also the text in force. Each is one version, dated by its promulgation in the Gaceta Oficial; where a law sets a later day for its entry into force, that day is not shown. Laws that Legispan records as modified are left out until their current text can be shown.

**Source.** Each Legispan record links a PDF that holds the Gaceta Oficial pages as scanned images followed by the Asamblea Nacional's typed edition of the law. Only the typed edition is read (its text layer); the scans are not read and no OCR is used. A law whose PDF has no typed edition, or an OCR text layer, is left out; so are recent laws published only as Gaceta scans.

**How it was checked.** Every word of the typed edition is in a file, in order, except the running header (G.O. number, "ASAMBLEA NACIONAL, REPÚBLICA DE PANAMÁ") and page numbers. The text before Artículo 1 is in `encabezado.md`, each article in `art-NNN.md` (with any heading printed above it), and the closing formula with the signatures in `firma.md`. A law whose own articles are not numbered 1, 2, 3 and so on, each once, is left out. The typed edition is the Asamblea's transcription, not a facsimile of the Gaceta.

| Folder | Law | In force from |
| --- | --- | --- |
{rows}
{A1}"""


def put(path: Path, text: str, anchor: str | None) -> None:
    s = path.read_text('utf-8') if path.exists() else ''
    if A0 in s:
        s = re.sub(re.escape(A0) + '.*?' + re.escape(A1), lambda m: text, s, flags=re.S)
    elif anchor and anchor in s:
        s = s.replace(anchor, text + '\n\n' + anchor, 1)
    else:
        s = s.rstrip('\n') + '\n\n' + text + '\n'
    path.write_text(s, 'utf-8', newline='\n')


put(H / 'repo' / 'README.md', SECTION, 'Dates are the day the change took effect.')
LIC = f"""{A0}
Laws in the folders ley-YYYY-NNNN/: the Asamblea Nacional de Panamá's typed editions of laws in Legispan
(https://legispan.asamblea.gob.pa/), retrieved November 2026. Legispan states no licence or terms of use (it
publishes a privacy policy only). The texts are reproduced without change to their wording, as the law of Panama.
{A1}"""
put(H / 'repo' / 'LICENSE', LIC, 'Changes made by Lexifina:')
j = json.loads((H / 'repo' / 'jurisdiction.json').read_text('utf-8'))
(H / 'repo' / 'jurisdiction.json').write_text(json.dumps(j, ensure_ascii=False, indent=2) + '\n', 'utf-8', newline='\n')
print(n, 'acts', units, 'units')
