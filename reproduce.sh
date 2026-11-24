#!/bin/bash
# Rebuild the graph from Google's file, verify the hypotheses of Theorem 3, and check the graph with exact programs.
# Needs: python3 (standard library), gcc (with OpenMP for check_enumerate).
# Default run: build seconds, clique-side and G-block checks about 10 minutes on an idle machine.
# The long independent-set searches are optional:
#   bash reproduce.sh long     (about 4 hours for each of the two programs, one core each)
set -e
cd "$(dirname "$0")"
sha256sum -c SHA256SUMS
echo "== Rebuild"
python3 build.py theorem3_R10_12_857.txt input_google_R10_12_856.txt rebuilt_857.txt
cmp rebuilt_857.txt R10_12_857.txt
echo "rebuilt graph is byte-identical to R10_12_857.txt"
echo "== Hypotheses of Theorem 3"
python3 verify_theorem3.py theorem3_R10_12_857.txt input_google_R10_12_856.txt R10_12_857.txt
gcc -O3 -o check_russian_doll check_russian_doll.c
gcc -O3 -fopenmp -o check_enumerate check_enumerate.c
gcc -O3 -o check_split_branch_bound check_split_branch_bound.c
echo "== Clique side (Russian-doll method; in clique mode the line 'clique number = N' is the exact clique number)"
./check_russian_doll R10_12_857.txt 10 c | tee out_857_c.txt; grep -q "exists: no" out_857_c.txt
echo "== Clique side (plain enumeration, counts every size)"
./check_enumerate R10_12_857.txt 10 c | tee out_857_ce.txt; grep -q "exists: no" out_857_ce.txt
echo "== G block (rows and columns 0..796, Paley(797)): no K10 and no independent 10-set"
python3 - <<'PY'
import re
d = [int(c) for c in re.sub(r'[^01]', '', open("R10_12_857.txt").read())]
N = int(round(len(d) ** 0.5))
open("G797.txt", "w").write("".join(" ".join(map(str, d[i * N:i * N + 797])) + "\n" for i in range(797)))
PY
./check_enumerate G797.txt 10 c | tee out_G797_c.txt; grep -q "exists: no" out_G797_c.txt
./check_enumerate G797.txt 10 i | tee out_G797_i.txt; grep -q "exists: no" out_G797_i.txt
if [ "$1" = "long" ]; then
  echo "== Independent-set side, Russian-doll method (long)"
  ./check_russian_doll R10_12_857.txt 12 i | tee out_857_i.txt; grep -q "exists: no" out_857_i.txt
  echo "== Second program (long)"
  ./check_split_branch_bound R10_12_857.txt 797 10 12 | tee out_857_sbb.txt; grep -q "^PASS" out_857_sbb.txt
fi
echo "ALL CHECKS PASSED"
