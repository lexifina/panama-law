"""Panama: add core statutes to corpus.json (Spanish; official copies). Reads .cache only.
The Constitution act from the first build is kept byte-for-byte; added acts are rebuilt on every run."""
import hashlib, json, os, re, subprocess
from pathlib import Path

here = Path(__file__).parent
KEEP = ('constitucion',)
RETRIEVED = '2026-10-30'
ART = re.compile(r'^\s*\d{0,2}\s*Art[ií]culo\s+(\d+(?:[-\s][A-Z]{1,2})?)\s*[.º°]\s*(.*)$')
HEAD = re.compile(r'^\s*(LIBRO|T[ií]tulo|Cap[ií]tulo|Secci[oó]n|Subsecci[oó]n|TITULO|CAPITULO)\b')


def norm(s):
    for a, b in ((' ', ' '), ('’', "'"), ('‘', "'"), ('“', '"'), ('”', '"'), ('–', '-'), ('\f', '')):
        s = s.replace(a, b)
    return re.sub(r'[ \t]+', ' ', s).strip()


def parse_penal(txt):
    L = txt.replace('\r', '').split('\n')
    first = next(i for i, l in enumerate(L) if re.match(r'^\s*Art[ií]culo 1\.', l.replace('\f', '')) and i > 200)
    last = next(i for i in range(len(L) - 1, 0, -1) if re.match(r'^\s*Comun[ií]quese', L[i]))
    arts = []
    cur = None
    skip = False
    for l in L[first:last]:
        s = norm(l)
        if re.match(r'^Texto [ÚU]nico del C[óo]digo Penal', s) or s == 'Procuraduría General de la Nación' or re.fullmatch(r'\d{1,3}', s):
            continue
        if not s:
            skip = False
            continue
        if HEAD.match(s):
            skip = True
            continue
        if skip and not ART.match(l):
            continue
        skip = False
        if re.match(r'^\d{1,3}\s+(Literal|Numeral|Art[ií]culo|Par[aá]grafo|P[aá]rrafo|Adicionad|Modificad|Subrogad|Derogad|Declarad|T[ií]tulo|Cap[ií]tulo|Secci[oó]n|Ordinal|Inciso|Frase|Palabra|Expresi[oó]n|Texto|Ac[aá]pite|Aparte|Nota|Ver|Reformad|Sentencia|Fallo)', s) and not ART.match(l):
            continue
        m = ART.match(l.replace('\f', ''))
        if m:
            num = re.sub(r'\s', '-', m.group(1))
            cur = {'n': num, 'lines': [m.group(2)] if m.group(2) else []}
            arts.append(cur)
            continue
        if cur is not None:
            cur['lines'].append(s)
    units = {}
    for a in arts:
        paras = []
        for s in a['lines']:
            s = re.sub(r'(?<=[a-záéíóúñ.,;:)])\d{1,2}(?=\s|$)', '', norm(s))
            if paras and not (paras[-1].endswith(('.', ':', ';')) and re.match(r'^(["A-ZÁÉÍÓÚÑ0-9]|\(?[a-z0-9]\)|\d+\.)', s)):
                if paras[-1].endswith('-') and s[:1].islower():
                    paras[-1] = paras[-1][:-1] + s
                else:
                    paras[-1] += ' ' + s
            else:
                paras.append(s)
        m = re.fullmatch(r'(\d+)(?:-([A-Z]+))?', a['n'])
        k = 'art-%03d' % int(m.group(1)) + ('-' + m.group(2).lower() if m.group(2) else '')
        if k in units:
            continue  # a footnote quoting an earlier wording of the article; the first occurrence is the article
        units[k] = {'label': 'Artículo ' + a['n'], 'kind': 'article', 'text': '# Artículo %s\n' % a['n'] + '\n'.join(paras) + '\n'}
    return units


def pdf_text(pdf):
    t = pdf.with_suffix('.txt')
    subprocess.run(['pdftotext', '-enc', 'UTF-8', '-layout', str(pdf), str(t)], check=True, capture_output=True)
    return t.read_text(encoding='utf8')


STATUTES = json.loads((here / 'statutes.json').read_text(encoding='utf8'))
PARSERS = {'penal': parse_penal}


def main():
    c = json.loads((here / 'corpus.json').read_text(encoding='utf8'))
    acts = [a for a in c['acts'] if a['slug'] in KEEP]
    laws = {k: v for k, v in c['laws'].items() if k == 'publisher-oldest'}
    sources = [s for s in c['sources'] if not s.get('added')]
    decisions = [d for d in c['decisions'] if not d.startswith('[statutes]')]
    for st in STATUTES:
        pdf = here / '.cache' / 'st' / st['file']
        units = PARSERS[st['parser']](pdf_text(pdf))
        sha = hashlib.sha256(pdf.read_bytes()).hexdigest()
        lk = 'publisher-' + st['slug']
        laws[lk] = {'label': st['publisher'], 'title': st['law_title'], 'kind': 'publisher', 'enacted': st['from'], 'published': st['from'],
                    'url': st['url'], 'temporary_until': None, 'restores': None, 'note': None}
        acts.append({'slug': st['slug'], 'short': st['short'], 'title': st['title'], 'url': st['url'], 'first_law': None, 'earlier_laws': [],
                     'versions': [{'from': st['from'], 'source_url': st['url'], 'sha256': sha, 'units': units,
                                   'credits': {k: [lk] for k in units}, 'note': st['note']}]})
        sources.append({'name': st['source_name'], 'url': st['url'], 'retrieved': RETRIEVED, 'requests': 1, 'licence': st['licence'],
                        'notes': 'PDF sha256 %s; text layer read with pdftotext.' % sha, 'added': True})
        decisions.append('[statutes] ' + st['decision'])
    c['acts'], c['laws'], c['sources'], c['decisions'] = acts, laws, sources, decisions
    (here / 'corpus.json.tmp').write_text(json.dumps(c, ensure_ascii=False, indent=1) + '\n', encoding='utf8', newline='\n')
    os.replace(here / 'corpus.json.tmp', here / 'corpus.json')


main()
