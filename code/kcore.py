"""k-core decomposition for the DGM (2006) reproduction, in NumPy plus one peeling loop.

core_numbers implements the O(V + E) bucket algorithm of Batagelj and Zaversnik (2003):
repeatedly remove a vertex of minimum remaining degree; its core number is that degree.
"""
import numpy as np


def clean_edges(edges):
    """Drop self-loops and duplicate (unordered) edges. Returns an (E, 2) int64 array with u < v."""
    e = np.asarray(edges, dtype=np.int64).reshape(-1, 2)
    e = e[e[:, 0] != e[:, 1]]
    e = np.sort(e, axis=1)
    return np.unique(e, axis=0)


def er_edges(N, z, rng):
    """Erdos-Renyi multigraph sample with mean degree z, cleaned to a simple graph."""
    E = rng.poisson(z * N / 2)
    return clean_edges(rng.integers(N, size=(E, 2)))


def core_numbers(N, edges, alive=None):
    """Core number of every vertex of a simple graph; vertices with alive == False get 0."""
    e = np.asarray(edges, dtype=np.int64).reshape(-1, 2)
    if alive is not None:
        alive = np.asarray(alive, dtype=bool)
        e = e[alive[e[:, 0]] & alive[e[:, 1]]]
    # CSR adjacency
    src = np.concatenate([e[:, 0], e[:, 1]])
    dst = np.concatenate([e[:, 1], e[:, 0]])
    order = np.argsort(src, kind="stable")
    nbr = dst[order]
    deg = np.bincount(src, minlength=N).astype(np.int64)
    ptr = np.concatenate(([0], np.cumsum(deg)))
    # bucket sort vertices by degree
    md = int(deg.max()) if N else 0
    bin_start = np.concatenate(([0], np.cumsum(np.bincount(deg, minlength=md + 1))))[:-1].astype(np.int64)
    vert = np.argsort(deg, kind="stable").astype(np.int64)
    pos = np.empty(N, dtype=np.int64)
    pos[vert] = np.arange(N)
    deg = deg.tolist(); vert = vert.tolist(); pos = pos.tolist(); bins = bin_start.tolist()
    nbr = nbr.tolist(); ptr = ptr.tolist()
    for i in range(N):
        v = vert[i]
        dv = deg[v]
        for j in range(ptr[v], ptr[v + 1]):
            u = nbr[j]
            du = deg[u]
            if du > dv:                       # move u one bucket down
                pu, pw = pos[u], bins[du]
                w = vert[pw]
                if u != w:
                    vert[pu], vert[pw] = w, u
                    pos[u], pos[w] = pw, pu
                bins[du] += 1
                deg[u] = du - 1
    core = np.array(deg, dtype=np.int64)
    if alive is not None:
        core[~alive] = 0
    return core


def kcore_sizes(core, ks):
    """Share of all vertices whose core number is at least k, for each k in ks."""
    core = np.asarray(core)
    return {k: float(np.mean(core >= k)) for k in ks}
