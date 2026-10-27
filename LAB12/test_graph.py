"""Automated tests. Run: python test_graph.py
Expected values below were derived BY HAND (see hand_traces.md) before running."""
import math
import unittest

from graph import Graph, verify_against_csv
from traversals import bfs, dfs, dfs_stack_trace
from dijkstra import dijkstra, reconstruct_path, path_cost, NegativeWeightError

CSV = "campus_edges.csv"


def campus():
    return Graph.from_csv(CSV)


def bellman_ford(graph, source):
    """Independent reference implementation (different algorithm)."""
    dist = {v: math.inf for v in graph.vertices()}
    dist[source] = 0
    for _ in range(len(dist) - 1):
        for u, v, w in graph.edges():
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
            if not graph.directed and dist[v] + w < dist[u]:
                dist[u] = dist[v] + w
    return dist


def _attempt(fn):
    try:
        return fn()
    except Exception as e:                      # noqa: BLE001
        return f"{type(e).__name__}"


def run_cases():
    """Return rows: (id, description, expected, observed, status)."""
    g = campus()
    rows = []

    def add(desc, expected, observed):
        rows.append((len(rows) + 1, desc, expected, observed,
                     "PASS" if expected == observed else "FAIL"))

    add("Graph has 9 vertices / 11 edges", (9, 11), (len(g.vertices()), len(g.edges())))
    add("Structure matches source CSV", [], verify_against_csv(g, CSV))
    add("BFS from Gate",
        ["Gate", "Admin", "Chapel", "ScienceLab", "Cafeteria", "Library", "Dorm", "Gym"],
        bfs(g, "Gate")[0])
    add("DFS from Gate",
        ["Gate", "Admin", "Cafeteria", "Gym", "Dorm", "Chapel", "ScienceLab", "Library"],
        dfs(g, "Gate")[0])
    add("BFS from Dorm",
        ["Dorm", "Chapel", "Gym", "Gate", "ScienceLab", "Cafeteria", "Admin", "Library"],
        bfs(g, "Dorm")[0])
    add("DFS from Dorm",
        ["Dorm", "Chapel", "Gate", "Admin", "Cafeteria", "Gym", "Library", "ScienceLab"],
        dfs(g, "Dorm")[0])
    add("Recursive DFS == explicit-stack DFS (Gate)",
        dfs(g, "Gate")[0], dfs_stack_trace(g, "Gate")[0])

    dist, prev = dijkstra(g, "Gate")
    add("Dijkstra distances from Gate",
        {"Admin": 2, "Annex": math.inf, "Cafeteria": 8, "Chapel": 12, "Dorm": 15,
         "Gate": 0, "Gym": 12, "Library": 3, "ScienceLab": 3},
        dist)
    add("Path Gate->Dorm (cost 3+9+3=15)",
        (["Gate", "ScienceLab", "Chapel", "Dorm"], 15),
        (reconstruct_path(prev, "Gate", "Dorm", dist),
         path_cost(g, reconstruct_path(prev, "Gate", "Dorm", dist))))
    add("Path Gate->Cafeteria (cost 2+1+5=8)",
        (["Gate", "Admin", "Library", "Cafeteria"], 8),
        (reconstruct_path(prev, "Gate", "Cafeteria", dist),
         path_cost(g, reconstruct_path(prev, "Gate", "Cafeteria", dist))))
    add("Equal-cost alternative Gate-ScienceLab-Cafeteria also costs 8",
        8, path_cost(g, ["Gate", "ScienceLab", "Cafeteria"]))
    add("Unreachable target Annex (dist inf, no path)",
        (math.inf, None), (dist["Annex"], reconstruct_path(prev, "Gate", "Annex", dist)))
    add("Isolated vertex Annex: BFS and DFS visit only itself",
        (["Annex"], ["Annex"]), (bfs(g, "Annex")[0], dfs(g, "Annex")[0]))

    tri = Graph()
    for a, b in (("A", "B"), ("B", "C"), ("C", "A")):
        tri.add_edge(a, b, 1)
    add("Cycle A-B-C: BFS/DFS terminate, each vertex once",
        (["A", "B", "C"], ["A", "B", "C"]), (bfs(tri, "A")[0], dfs(tri, "A")[0]))

    neg = Graph(directed=True)
    neg.add_edge("A", "B", 4)
    neg.add_edge("A", "C", 5)
    neg.add_edge("C", "B", -3)
    add("Negative weight rejected by Dijkstra", "NegativeWeightError",
        _attempt(lambda: dijkstra(neg, "A")))
    wrong, _ = dijkstra(neg, "A", check_negative=False)
    add("Why negative is invalid: unchecked Dijkstra says A->B=4, true value 2",
        (4, 2), (wrong["B"], bellman_ford(neg, "A")["B"]))

    d = Graph(directed=True)
    d.add_edge("X", "Y", 1)
    add("Directed edge X->Y: Y cannot reach X",
        (["X", "Y"], ["Y"]), (bfs(d, "X")[0], bfs(d, "Y")[0]))

    bfs_path_gate_chapel = _bfs_path(bfs(g, "Gate")[1], "Chapel")
    add("BFS tree (1 edge, weight 20) differs from shortest-path tree (2 edges, weight 12)",
        (["Gate", "Chapel"], ["Gate", "ScienceLab", "Chapel"]),
        (bfs_path_gate_chapel, reconstruct_path(prev, "Gate", "Chapel", dist)))

    add("Unknown start vertex raises KeyError", ("KeyError", "KeyError"),
        (_attempt(lambda: bfs(g, "Nope")), _attempt(lambda: dijkstra(g, "Nope"))))
    bad = Graph()
    add("Non-numeric weight rejected", "TypeError", _attempt(lambda: bad.add_edge("A", "B", "x")))

    ok = all(dijkstra(g, s)[0] == bellman_ford(g, s) for s in g.vertices())
    add("Dijkstra == Bellman-Ford from every source vertex", True, ok)
    return rows


def _bfs_path(parent, target):
    path = []
    while target is not None:
        path.append(target)
        target = parent[target]
    return path[::-1]


class TestGraph(unittest.TestCase):
    def test_all_cases(self):
        for row in run_cases():
            with self.subTest(case=row[1]):
                self.assertEqual(row[4], "PASS", f"expected {row[2]} observed {row[3]}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
