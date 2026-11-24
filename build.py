"""Build the 856-vertex graph for R(10,12) >= 857, standard library only.
Construction: Theorem 3 of Xu, Shao, Radziszowski, "More constructive lower bounds on classical Ramsey numbers",
SIAM J. Discrete Math. 25 (2011) 394-400. The data file theorem3_R10_12_857.txt names k, the sizes of G and H, where H sits
in Google's R(10,12) file, the 20 pairs (u in G, v in H) and the split W1/W2 of the common part M.
G is the Paley graph on 797 vertices (generated here, and checked to equal rows 0..796 of Google's file); H is rows 797..835.
The new vertices z_i are joined to N_G(u_i) and N_H(v_i); u_i is joined to v_i; z_i, z_j are joined when u_i u_j is an
edge of G and i, j lie on the same side of the split.
Output: n rows of n space-separated 0/1 entries, one row per line, no header line (the layout of Google's matrices,
without the brackets and line wrapping).
Usage: python3 build.py theorem3_R10_12_857.txt input_google_R10_12_856.txt out.txt"""
import re, sys

def read_matrix(path):
    d = [int(c) for c in re.sub(r'[^01]', '', open(path).read())]
    n = int(round(len(d) ** 0.5)); assert n * n == len(d)
    return [d[i * n:(i + 1) * n] for i in range(n)]


def read_spec(path):
    spec = {}
    for line in open(path):
        line = line.split('#')[0].split()
        if line:
            spec[line[0]] = line[1:]
    return spec


def paley(p):
    sq = {(x * x) % p for x in range(1, p)}
    return [[1 if (i - j) % p in sq else 0 for j in range(p)] for i in range(p)]


def build_t3(specf, srcf, out):
    sp = read_spec(specf)
    nG, nH, h0 = int(sp['nG'][0]), int(sp['nH'][0]), int(sp['h_start'][0])
    pairs = [tuple(map(int, p.split(':'))) for p in sp['pairs']]
    W1 = set(map(int, sp['W1']))
    m = len(pairs)
    A = read_matrix(srcf)
    G = [r[:nG] for r in A[:nG]]
    if sp['g_source'][0] == 'paley':
        assert nG % 4 == 1 and all(nG % q for q in range(2, int(nG ** 0.5) + 1)), 'Paley needs a prime = 1 mod 4'
        assert paley(nG) == G, 'Paley graph differs from the rows of the Google file'
        G = paley(nG)
    H = [r[h0:h0 + nH] for r in A[h0:h0 + nH]]
    U = [u for u, v in pairs]; V = [v for u, v in pairs]
    for i in range(m):
        for j in range(m):
            assert G[U[i]][U[j]] == H[V[i]][V[j]], 'not a common induced subgraph'
    N = nG + nH + m
    B = [[0] * N for _ in range(N)]
    for i in range(nG):
        for j in range(nG):
            B[i][j] = G[i][j]
    for i in range(nH):
        for j in range(nH):
            B[nG + i][nG + j] = H[i][j]
    for i in range(m):                                  # matching u_i -- v_i
        B[U[i]][nG + V[i]] = B[nG + V[i]][U[i]] = 1
    for i in range(m):                                  # z_i copies the neighbours of u_i in G and of v_i in H
        z = nG + nH + i
        for j in range(nG):
            B[z][j] = B[j][z] = G[U[i]][j]
        for j in range(nH):
            B[z][nG + j] = B[nG + j][z] = H[V[i]][j]
        for j in range(m):                              # M[W1] and M[W2], no W1-W2 edges
            if (i in W1) == (j in W1):
                B[z][nG + nH + j] = G[U[i]][U[j]]
    assert all(B[i][j] == B[j][i] for i in range(N) for j in range(N)) and all(B[i][i] == 0 for i in range(N))
    open(out, 'w').write(''.join(' '.join(map(str, r)) + '\n' for r in B))
    print('built', N, 'vertices, common part m =', m)

build_t3(sys.argv[1], sys.argv[2], sys.argv[3])
