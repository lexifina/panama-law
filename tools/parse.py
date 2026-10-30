"""Panama: parse the Constitution (Texto Unico, Gaceta Oficial 25176) from the Asamblea Nacional's 2024 edition PDF
into corpus.json. Usage: python -X utf8 parse.py <Reglamento_Organico_del_Regimen_Interno.pdf>"""
import hashlib, json, re, subprocess, sys
from pathlib import Path

PDF = Path(sys.argv[1])
URL = 'https://asamblea.gob.pa/Uploads/GestorFiles/Reglamento_Organico_del_Regimen_Interno.pdf'
RETRIEVED = '2026-10-29'
sha = hashlib.sha256(PDF.read_bytes()).hexdigest()
raw = subprocess.run(['pdftotext', '-enc', 'UTF-8', '-layout', str(PDF), '-'], capture_output=True, check=True).stdout.decode('utf8')
L = raw.replace('\r', '').replace('\f', '\n').replace(' ', ' ').split('\n')

first = next(i for i, l in enumerate(L) if re.match(r'^ARTICULO 1\.', l))
last = next(i for i, l in enumerate(L) if re.match(r'^ARTICULO 328\.', l))
stop = next(i for i, l in enumerate(L) if i > last and l.startswith('“Dada en la ciudad'))
seg = L[first:stop]

ART = re.compile(r'^\s*ARTICULO (\d+)\.\s*(.*)$')
NOISE = re.compile(r'^\s*(Constitución Política de la República de Panamá y Texto Único del|Reglamento Orgánico del Régimen Interno de la Asamblea Nacional|CONSTITUCIÓN POLÍTICA DE LA REPÚBLICA DE PANAMÁ)\b.*$')
PAGENO = re.compile(r'^\s*\d{1,3}\s*\.?\s*(Constitución Política.*)?$')


def is_heading(s):
    t = re.sub(r'[^A-ZÁÉÍÓÚÑÜa-záéíóúñü]', '', s)
    return bool(t) and t == t.upper() and not ART.match(s) and len(s) < 90


def clean(t):
    for a, b in (('’', "'"), ('‘', "'"), ('“', '"'), ('”', '"'), ('–', '-')):
        t = t.replace(a, b)
    t = re.sub(r'(?<=[a-záéíóúñüA-ZÁÉÍÓÚ])\d{1,2}(?=[\s.,;:)]|$)', '', t)  # footnote markers glued to a word
    return re.sub(r' {2,}', ' ', t).strip()


arts = []
cur = None
skipping = False
for l in seg:
    if re.search(r'_{5,}', l):
        skipping = True
        continue
    if NOISE.match(l):
        skipping = False
    if skipping:
        continue
    if NOISE.match(l) or PAGENO.match(l) and not ART.match(l):
        # a page footer; the number can be glued to the title ("... del . 13")
        continue
    s = l.strip()
    m = ART.match(l)
    if m:
        cur = {'n': int(m.group(1)), 'lines': [(0, m.group(2))]}
        arts.append(cur)
        continue
    if not s:
        continue
    if re.match(r'^(TITULO|CAPITULO|Capítulo|Título)\b', s) or is_heading(s):
        continue
    if re.fullmatch(r'\d{1,3}', s):
        continue
    ind = len(l) - len(l.lstrip())
    cur['lines'].append((ind, s))

units = {}
for a in arts:
    paras = [[a['lines'][0][1]]] if a['lines'][0][1] else []
    for ind, s in a['lines'][1:]:
        if 3 <= ind <= 6 or not paras:
            paras.append([s])
        else:
            paras[-1].append(s)
    out = []
    for p in paras:
        txt = ''
        for part in p:
            if txt.endswith('-') and part[:1].islower():
                txt = txt[:-1] + part
            else:
                txt = (txt + ' ' + part) if txt else part
        out.append(clean(txt))
    n = a['n']
    units['art-%03d' % n] = {'label': 'Artículo %d' % n, 'kind': 'article', 'text': '# Artículo %d\n' % n + '\n'.join(out) + '\n'}
assert [a['n'] for a in arts] == list(range(1, 329)), 'numbering'

# preamble
pi = next(i for i, l in enumerate(L) if l.strip() == 'PREÁMBULO')
pre = ' '.join(x.strip() for x in L[pi + 1:first] if x.strip() and not x.strip().startswith('TITULO') and not x.strip().startswith('EL ESTADO') and not NOISE.match(x))
units = {'preambulo': {'label': 'Preámbulo', 'kind': 'preamble', 'text': '# Preámbulo\n' + clean(pre) + '\n'}, **units}

FROM = '2004-11-15'
credits = {k: ['publisher-oldest'] for k in units}
corpus = {
    'country': {
        'code': 'PA', 'name': 'Panama', 'slug': 'panama', 'lang': 'es', 'tz': 'America/Panama', 'future_branch': 'future',
        'publisher': {'name': 'Asamblea Nacional de Panamá', 'email': 'constitucion@asamblea-gob-pa.invalid'},
        'default_in_force_rule': {'text': 'This record dates the Constitution text by the Gaceta Oficial in which its Texto Único was published (No. 25176, 15 November 2004).',
                                  'source': 'https://asamblea.gob.pa'},
        'licence_note': 'Text of the Constitución Política de la República de Panamá as printed in the Asamblea Nacional edition of April 2024 (asamblea.gob.pa). The site states no licence; legislation is reproduced as published.'},
    'sources': [{'name': 'Asamblea Nacional de Panamá, Constitución Política y Reglamento Orgánico del Régimen Interno (Edición 2024)',
                 'url': URL, 'retrieved': RETRIEVED,
                 'licence': 'No licence stated on the site; robots.txt does not disallow /Uploads/GestorFiles/',
                 'notes': 'PDF sha256 %s; born-digital PDF with a text layer, read with pdftotext. Only the Constitution part (pp. 7 to 113) is used.' % sha}],
    'laws': {'publisher-oldest': {'label': 'Asamblea Nacional', 'title': 'Asamblea Nacional de Panamá, edition of April 2024, oldest version available',
                                  'kind': 'publisher', 'enacted': FROM, 'published': FROM, 'url': URL,
                                  'temporary_until': None, 'restores': None, 'note': None}},
    'acts': [{'slug': 'constitucion', 'short': 'CP', 'title': 'Constitución Política de la República de Panamá', 'url': URL,
              'first_law': None, 'earlier_laws': [],
              'versions': [{'from': FROM, 'source_url': URL, 'sha256': sha, 'units': units, 'credits': credits,
                            'note': 'The 1972 Constitution as amended in 1978, 1983, 1993, 1994 and 2004, following the Texto Unico of Gaceta Oficial 25176 of 15 November 2004 (the Assembly edition says it keeps the original wording where the Texto Unico departs from it). Earlier texts are not online.'}]}],
    'applies': [],
    'decisions': [
        'Language: Spanish, the official language.',
        'No dated past versions are online, so there is one version, credited to the publisher as "oldest version available" and dated 15 November 2004, the Gaceta Oficial date of the current Texto Unico.',
        'Cleaning: page headers and footers, Title and Chapter headings, and the closing date-and-amendments note were removed; line breaks inside a paragraph were joined (hyphenated words rejoined); typographic quotes normalised. The preamble and articles 1 to 328 are kept.'],
    'ai_use': ['none']}
Path(__file__).with_name('corpus.json').write_text(json.dumps(corpus, indent=1, ensure_ascii=False) + '\n', encoding='utf8', newline='\n')
print(len(units), 'units')
