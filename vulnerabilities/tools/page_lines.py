"""Hand-check helper for panama-law: at one commit, (1) the lines in article files that hold only a page header or footer
of the edition ("G.O. 27,027-A", "ASAMBLEA NACIONAL, REPÚBLICA DE PANAMÁ"), and (2) the laws whose own commencement
article ("Artículo 2. Esta Ley comenzará a regir ...") sits in the file of an earlier article. The counts in the README.

    python -X utf8 page_lines.py <bare repo> <sha>
"""
import collections, re, subprocess, sys

repo, sha = sys.argv[1], sys.argv[2]
git = lambda *a: subprocess.run(["git", "-C", repo, *a], capture_output=True, check=True).stdout.decode("utf-8", "replace")
files = [p for p in git("ls-tree", "-r", "--name-only", sha, "--", "ley", "code", "constitution").splitlines()
         if re.search(r"/art-[^/]*\.md$", p)]
PAGE = {"gaceta": re.compile(r"^G\.\s?O\.\s?[0-9][0-9,.]*\s?[‐-]?\s?[A-Z]?\s*$"),
        "asamblea": re.compile(r"^ASAMBLEA NACIONAL, REPÚBLICA DE PANAMÁ\s*$")}
START = re.compile(r"^Art[ií]culo (\d+)[º°o]?\.?-?\s*(?:La presente|Esta) Ley (?:comenzará|entrará|empezará|regirá|rige|entra)", re.I)
lines, nfiles, acts = collections.Counter(), collections.Counter(), collections.defaultdict(set)
merged = []
blob = subprocess.run(["git", "-C", repo, "cat-file", "--batch"], input="".join(f"{sha}:{p}\n" for p in files).encode(),
                      capture_output=True, check=True).stdout
pos = 0
for p in files:
    nl = blob.index(b"\n", pos); size = int(blob[pos:nl].split()[2]); body = blob[nl + 1: nl + 1 + size].decode("utf-8", "replace")
    pos = nl + 2 + size
    own = int(re.search(r"art-0*(\d+)", p).group(1))
    for k, rx in PAGE.items():
        n = sum(1 for l in body.splitlines() if rx.match(l))
        if n:
            lines[k] += n; nfiles[k] += 1; acts[k].add(p.rsplit("/", 1)[0])
    for l in body.splitlines():
        m = START.match(l)
        if m and int(m.group(1)) != own and not re.search(r"\b(queda|quedará) así", body.splitlines()[0]):
            merged.append((p, int(m.group(1))))
for k in PAGE:
    print(f"{k}: {lines[k]} lines in {nfiles[k]} article files of {len(acts[k])} acts")
print(f"commencement article in an earlier article's file: {len(merged)}")
for p, n in merged:
    print(f"  {p} holds Artículo {n}")
