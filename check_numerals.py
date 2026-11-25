"""Coverage self-audit: list every numeral in paper/PAPER.md and check its binding in claims.yaml.

A numeral counts as bound when some claim's passage lies inside the paragraph that
contains it and the passage contains the same whole numeral token (with % kept).
Computation claims must also report that token. Numerals inside citations, math,
figure paths and the front matter are skipped; years (1900-2099) and labels such as
"Proposition 1" or "Table 2" are listed separately. Exit status 1 if any numeral is unbound.
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
NUM = re.compile(r"(?<![\w.+−-])[+−-]?(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?|\.\d+)(?:\\?%)?(?!\w|\.\d)")
LABEL = re.compile(r"(Proposition|Table|Figure|Fig\.)\s+\d+")


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


def strip_nonprose(par):
    par = re.sub(r"\[[^\]]*@[^\]]*\]", " ", par)          # citations
    par = re.sub(r"\$\$.*?\$\$|\$[^$]*\$", " ", par)       # math
    par = re.sub(r"\]\([^)]*\)\{[^}]*\}", "]", par)        # image path and attributes
    par = re.sub(r"https?://\S+", " ", par)
    par = LABEL.sub(" ", par)
    return par


def main():
    md = (ROOT / "paper" / "PAPER.md").read_text()
    md = md.split("---", 2)[2] if md.startswith("---") else md
    md = md.split("## References")[0]
    claims = yaml.safe_load((ROOT / "claims.yaml").read_text())["claims"]
    unbound, years, bound = [], [], 0
    for par in md.split("\n"):
        if not par.strip() or par.startswith("|:") or par.startswith("#"):
            continue
        npar = norm(par)
        inside = [c for c in claims if norm(c["passage"]) in npar]
        for m in NUM.finditer(strip_nonprose(par)):
            tok = m.group().replace("\\%", "%")
            value = tok.rstrip("%").replace(",", "")
            if "%" not in tok and "." not in value and 1900 <= int(value) <= 2099:
                years.append(tok)
                continue
            ok = False
            for c in inside:
                if NUM.search(c["passage"]) and tok in [t.group().replace("\\%", "%") for t in NUM.finditer(strip_nonprose(c["passage"]))]:
                    if c["kind"] == "computation" and c["evidence"]["reported"] != tok:
                        continue
                    ok = True
                    break
            if ok:
                bound += 1
            else:
                unbound.append((tok, npar[:90]))
    print(f"numerals bound: {bound}; years skipped: {len(years)}; unbound: {len(unbound)}")
    for tok, ctx in unbound:
        print(f"  UNBOUND {tok!r}: {ctx}")
    return 1 if unbound else 0


if __name__ == "__main__":
    sys.exit(main())
