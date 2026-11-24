# R(10,12) ≥ 857

This repository gives a graph on 856 vertices that contains no clique of 10 vertices and no independent set of 12 vertices. It shows that the Ramsey number R(10,12) is at least 857.

A companion result, R(9,11) ≥ 620, is at https://github.com/Petebacher/ramsey-r9-11.

## Results

| Bound | Graph file | Vertices | Previous best public bound we could find | Gain |
|---|---|---|---|---|
| R(10,12) ≥ 857 | `R10_12_857.txt` | 856 | 856 (Google Research) | +1 |

Prior art. Google Research published R(10,12) ≥ 856 (an 855-vertex graph) on 22 October 2026 in `google-research/google-research`, folder `ramsey_number_bounds/improved_bounds`, file `R(10, 12) >= 856.txt` (commit 0d94f8c). The Leaps in Bounds tracker lists that value. The dynamic survey *Small Ramsey Numbers* (S. P. Radziszowski, DS1 revision 18, April 2026) prints no lower bound for this cell. These are the best public bounds we could find as of 24 November 2026; we searched the web, arXiv, Zenodo, GitHub, the Leaps in Bounds tracker and the repositories of other recent contributors. We did not search social media, MathOverflow or mailing lists, so this is not a claim about everything that is known.

## Where the graph comes from

The graph uses **Theorem 3** of Xu Xiaodong, Shao Zehui and S. P. Radziszowski, "More constructive lower bounds on classical Ramsey numbers", SIAM J. Discrete Math. 25 (2011) 394-400. We read the theorem in the authors' preprint (dated 14 September 2010); the theorem number is as in the preprint, and we could not check it against the journal version. The theorem says:

> Let k ≥ 4 and s, t ≥ 2. Let G be a (k,s)-graph (no K_k, no independent s-set) and H a (k,t)-graph. Let M be a graph isomorphic to an induced subgraph of both G and H. If the vertex set of M can be split into two nonempty sets W1 and W2 so that for i = 1, 2 and every vertex v of M outside Wi the graph M[Wi + v] has no K_(k−1), then R(k, s+t−1) ≥ n(G) + n(H) + n(M) + 1.

The inputs are not new. G is the Paley graph on 797 vertices (797 is prime and 1 mod 4; vertices i and j are adjacent when i − j is a nonzero square mod 797). It is exactly rows 0 to 796 of Google's 855-vertex R(10,12) file, with the identity labelling. H is the 39-vertex block (rows 797 to 835) of that file. **The new part is the larger common subgraph M (20 vertices) together with a valid split.**

| | R(10,12) ≥ 857 |
|---|---|
| k, s, t | 10, 10, 3 |
| G | Paley(797), a (10,10)-graph |
| H | 39 vertices, clique number 9, independence number 2, so a (10,3)-graph |
| M | 20 vertices, 145 edges, clique number 8 |
| split | 19 + 1 |
| largest clique in any M[Wi + v] | 8 (limit k−2 = 8) |
| count | 797 + 39 + 20 = 856 |
| s + t − 1 | 10 + 3 − 1 = 12 |

Here M has no K9, so the simpler survey rule (item 2.3.h, a common part without K_(k−1)) would also apply; Theorem 3 is what we used.

The pairing and the split are a plain file, `theorem3_R10_12_857.txt`. It lists the 20 pairs u:v (u a vertex of G, v the matching vertex of H) and the split. M was found by local search for large common induced subgraphs.

## The graph F built from the data

F has the vertices of G, then the vertices of H, then 20 new vertices z_1 ... z_20, one per pair (u_i, v_i):
- the edges of G and of H are kept;
- u_i is joined to v_i (a matching; these are the only edges between G and H);
- z_i is joined to the neighbours of u_i in G and to the neighbours of v_i in H (not to u_i or v_i themselves);
- z_i and z_j are joined when u_i u_j is an edge of G and i, j are on the same side of the split.
`build.py` does this using the Python standard library only.
G is generated as the Paley graph and compared with rows 0 to 796 of Google's file.

## Why it works (Theorem 3, short form)

- **No K_k.** A clique that meets both G and H has exactly one vertex u_j in G and one v_j in H, since only matching edges join them. Its other k−2 vertices cannot be in both parts of the split, so they are new vertices z_i with all their indices i in one Wi, and those indices together with j form a K_(k−1) in M[Wi + j] (or in M[Wi], when j itself is in Wi). The split condition excludes this. A clique missing H or G is mapped to a clique of G (or H) of the same size by replacing each z_j by u_j (v_j), so it has fewer than k vertices.
- **No independent set of size s + t − 1.** Split an independent set I into its parts in G, in H, in W1 and in W2, and sort the G and H vertices by whether their partner z is in I. The parts that sit next to G embed in G as one independent set, giving at most s − 1 vertices; the others embed in H, giving at most t − 1. So |I| ≤ s + t − 2.

The full proof is in the paper. The direct checks below do not depend on it.

## Verification

Everything below was run on the files in this repository (the sha256 values are in `SHA256SUMS`).

**File format.** `R10_12_857.txt` is 856 lines, each a row of 856 entries 0/1 separated by single spaces. There is no header line. (Google's own files use the same entries inside `[[ ... ]]` with wrapped lines.) All checkers read every `0` and `1` character of the file and nothing else, so do not add a header line.

**1. Hypotheses of Theorem 3** (`verify_theorem3.py`, standard library only, seconds): F is symmetric with zero diagonal; its G block is exactly Paley(797) and the stated rows of Google's file, and its H block is the stated rows; the G-H edges are exactly the matching; every z_i has exactly the neighbourhoods N_G(u_i), N_H(v_i); M is the same graph in G and in H; Z = M[W1] + M[W2] with no W1-W2 edge; the split condition holds; H is a (10,3)-graph; the counts add up. All pass (`logs/verify_theorem3_R10_12_857.log`).

**2. G is a (10,10)-graph.** Not done in pure Python (too slow). Done with `check_enumerate` (exhaustive enumeration, no pruning): Paley(797) has no K10 and no independent 10-set (`logs/enumerate_P797_*.log`, 34 s each).

**3. Direct exact checks of the finished graph.** Every run says "no":

| Program | Method | R10_12_857.txt (856 vertices) |
|---|---|---|
| `check_russian_doll.c` | Östergård's Russian-doll method, exact | clique number exactly 9 (258 s); independence number exactly 11 (15,121 s, 4.2 hours) |
| `check_split_branch_bound.c` | branch and bound; independent sets via full enumeration of the small part | no K10 (538,460,842 nodes); no independent 12-set (89,246,018,071 nodes) |
| `check_enumerate.c` | plain enumeration with no pruning at all, counts every size | 0 cliques of size 10; 0 independent sets of size 12 |

Counts from `check_enumerate.c`, which anyone can match against a rerun: 946,813,214 cliques of size 9 and 0 of size 10; 127,023,891,381 independent sets of size 11 and 0 of size 12.

The searches also find sets one size below the target (cliques of size 9, independent sets of size 11), which works as a positive control.

How independent the checks are: `check_split_branch_bound.c` uses a colouring branch and bound for cliques, so on the clique side it is a different method from the Russian-doll search and from the plain enumeration; the three methods differ from each other. A further private check program without a published source gave the same answers; we do not count it here.

**Logs.** `logs/` holds the finished runs. Notes:
- The logs named `rdoll_old_*`, `split_bb_*` and `enumerate_*` were made on files with identical content (same sha256) under earlier working names such as `t3_10_856_s23.txt`; the name inside the log is that working name (in the `enumerate_*` logs a directory path was removed from the first line). The long searches were not repeated.
- The `rdoll_old_*` logs were written by the version of `check_russian_doll.c` before a printing fix. In clique mode that version called the result "independence number" (it works on the complement, so the number it prints is the clique number), and it printed "K4 count: 0" even when the count was skipped for n > 300. The shipped `check_russian_doll.c` fixes only these printed labels; the search code is unchanged. The change is in `logs/check_russian_doll_label_fix.diff`. Read "independence number" in the clique-mode `rdoll_old_*` logs as "clique number", and ignore "K4 count: 0".
- The logs whose names start with `check_` were produced by the shipped programs on the shipped files on 24 November 2026 (clique sides only; the machine was busy, so the cpu times are longer than in the `rdoll_old_*` logs, with the same node counts: 8,575,349,401 for R10_12_857.txt). They show the corrected labels.

`reproduce.sh` runs the checksum check, the rebuild with byte comparison, the hypothesis verifier, and the fast clique-side and G-block checks (about 10 minutes on an idle machine). The long independent-set searches are optional: `reproduce.sh long` (about 4 hours for each).

## Files

- `R10_12_857.txt`: the graph (format above).
- `input_google_R10_12_856.txt`: Google's 855-vertex R(10,12) graph, redistributed unchanged (renamed from `R(10, 12) >= 856.txt`) with attribution; see License.
- `theorem3_R10_12_857.txt`: pairing and split.
- `build.py`: rebuilds the graph (Paley(797) is generated). `verify_theorem3.py`: the hypothesis checker.
- `check_russian_doll.c` (usage `file T i|c`), `check_split_branch_bound.c` (usage `file n1 k t`), `check_enumerate.c` (usage `file T c|i`, needs OpenMP).
- `reproduce.sh`, `SHA256SUMS`, `logs/`.

## Credit and method

The starting graphs are Google Research's blocks and the Paley graph. Theorem 3 is due to Xu, Shao and Radziszowski. The new part is the 20-vertex common subgraph and its split, found by search, and the checks. The gain over Google's bound is one.

This work was directed by Peter J. Chrisbacher. The search, construction and checks were carried out with AI coding agents (Anthropic's Claude Code), working under fixed rules: every claim needs independently written exact checks and a check of published results before any announcement. A separate AI review re-derived the theorem's proof, re-checked every hypothesis and wrote the unpruned enumeration program that is shipped here as check_enumerate.c; the logs/enumerate_* files are that review's runs, so the enumeration is one of the three programs above, not a fourth.

## Changelog

- **v1.0 (24 November 2026).** First release: R(10,12) ≥ 857.

## License

- Code (`build.py`, `verify_theorem3.py`, the checkers, `reproduce.sh`): MIT.
- The new graph, the pairing file and this text: CC BY 4.0.
- `input_google_R10_12_856.txt` is Google's file, redistributed unchanged with attribution under the terms of google-research/google-research (Apache 2.0 for source files, CC BY 4.0 for datasets; the Apache text is in `LICENSES/`). The graph `R10_12_857.txt` contains Google's 39-vertex block and the Paley graph unchanged (plus new vertices and edges).

## How to cite

See `CITATION.cff`, or cite the Zenodo record for this repository once it is published.
