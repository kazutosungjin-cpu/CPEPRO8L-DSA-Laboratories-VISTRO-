"""Adjacency-list graph model (directed or undirected, weighted or not).

Neighbor-ordering rule (used by every algorithm in this lab):
    neighbors are always processed in ALPHABETICAL order of vertex name.
"""
import csv


class Graph:
    def __init__(self, directed=False, weighted=True):
        self.directed = directed
        self.weighted = weighted
        self._adj = {}                      # vertex -> {neighbor: weight}

    # ---- construction -------------------------------------------------
    def add_vertex(self, v):
        self._adj.setdefault(v, {})

    def add_edge(self, u, v, weight=1):
        if u == "" or v == "":
            raise ValueError("edge endpoints must be non-empty")
        if not self.weighted:
            weight = 1
        if isinstance(weight, bool) or not isinstance(weight, (int, float)):
            raise TypeError(f"weight must be a number, got {weight!r}")
        if v in self._adj.get(u, {}):
            raise ValueError(f"duplicate edge {u}->{v}")
        self.add_vertex(u)
        self.add_vertex(v)
        self._adj[u][v] = weight
        if not self.directed:
            self._adj[v][u] = weight

    # ---- queries ------------------------------------------------------
    def vertices(self):
        return sorted(self._adj)

    def has_vertex(self, v):
        return v in self._adj

    def neighbors(self, v):
        """[(neighbor, weight), ...] sorted alphabetically by neighbor."""
        if v not in self._adj:
            raise KeyError(f"unknown vertex {v!r}")
        return sorted(self._adj[v].items())

    def edges(self):
        """Each edge once: (u, v, w). Undirected edges listed with u < v."""
        out = []
        for u in self.vertices():
            for v, w in self.neighbors(u):
                if self.directed or u < v:
                    out.append((u, v, w))
        return out

    def has_negative_weight(self):
        return any(w < 0 for _, _, w in self.edges())

    # ---- loading / validation ----------------------------------------
    @classmethod
    def from_csv(cls, path, directed=False, weighted=True):
        """Rows are u,v,weight. A row with an empty v declares an isolated vertex."""
        g = cls(directed=directed, weighted=weighted)
        with open(path, newline="") as f:
            for row in csv.DictReader(f):
                u, v, w = row["u"].strip(), row["v"].strip(), row["weight_m"].strip()
                if v == "":
                    g.add_vertex(u)
                else:
                    g.add_edge(u, v, float(w) if "." in w else int(w))
        return g


def verify_against_csv(graph, path):
    """Independently re-read the CSV and list every mismatch (empty = OK)."""
    problems, want_edges, want_vertices = [], set(), set()
    with open(path, newline="") as f:
        for row in csv.reader(f):
            if row[0] == "u":
                continue
            u, v, w = row[0], row[1], row[2]
            want_vertices.add(u)
            if v:
                want_vertices.add(v)
                want_edges.add(frozenset((u, v)) if not graph.directed else (u, v))
                got = dict(graph.neighbors(u)).get(v)
                if got is None or float(got) != float(w):
                    problems.append(f"edge {u}-{v}: expected {w}, got {got}")
    for v in want_vertices:
        if not graph.has_vertex(v):
            problems.append(f"missing vertex {v}")
    if set(graph.vertices()) != want_vertices:
        problems.append("extra vertices in structure")
    if len(graph.edges()) != len(want_edges):
        problems.append(f"edge count {len(graph.edges())} != {len(want_edges)}")
    return problems
