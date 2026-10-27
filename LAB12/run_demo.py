"""Generates every output file. Run: python run_demo.py"""
import csv
import math

from graph import Graph
from traversals import bfs, dfs, bfs_trace, dfs_stack_trace
from dijkstra import dijkstra, reconstruct_path, path_cost, NegativeWeightError
from test_graph import run_cases, bellman_ford

SOURCE = "Gate"
g = Graph.from_csv("campus_edges.csv")

# ---- edge table -------------------------------------------------------
with open("edge_table.md", "w") as f:
    f.write("| # | From | To | Weight (m) |\n|---:|---|---|---:|\n")
    for i, (u, v, w) in enumerate(g.edges(), 1):
        f.write(f"| {i} | {u} | {v} | {w} |\n")
    iso = [v for v in g.vertices() if not g.neighbors(v)]
    f.write(f"\nIsolated vertices: {', '.join(iso)}\n")

# ---- traversal output + program traces ---------------------------------
with open("traversal_results.txt", "w") as f:
    for start in ("Gate", "Dorm"):
        f.write(f"BFS from {start}: {' -> '.join(bfs(g, start)[0])}\n")
        f.write(f"DFS from {start}: {' -> '.join(dfs(g, start)[0])}\n")
    f.write("\n== BFS trace from Gate (program) ==\n")
    for u, q, vis in bfs_trace(g, "Gate"):
        f.write(f"select={u:<10} queue={q}  visited={vis}\n")
    f.write("\n== DFS (explicit stack) trace from Gate (program) ==\n")
    for u, act, st, vis, order in dfs_stack_trace(g, "Gate")[1]:
        f.write(f"pop={u:<10} {act:<24} stack={st}  order={order}\n")
    tr = []
    dijkstra(g, SOURCE, trace=tr)
    f.write("\n== Dijkstra heap pops from Gate (program) ==\n")
    for d, u, what, ch in tr:
        f.write(f"pop ({d}, {u}) {what}; updates: {ch}\n")

# ---- routing table -----------------------------------------------------
dist, prev = dijkstra(g, SOURCE)
bfs_parent = bfs(g, SOURCE)[1]
rows = []
for t in g.vertices():
    p = reconstruct_path(prev, SOURCE, t, dist)
    rows.append([t, "unreachable" if p is None else dist[t],
                 "-" if p is None else " > ".join(p),
                 "-" if p is None else len(p) - 1])
with open("routing_table.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["target", "distance_m", "path", "edges"])
    w.writerows(rows)
with open("routing_table.md", "w") as f:
    f.write(f"Source: {SOURCE}\n\n| Target | Distance (m) | Shortest path | Edges |\n|---|---:|---|---:|\n")
    for r in rows:
        f.write(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |\n")
    f.write("\n**BFS tree vs shortest-path tree (from Gate)**\n\n| Target | BFS path (min edges) | BFS cost | Dijkstra path | Dijkstra cost |\n|---|---|---:|---|---:|\n")
    for t in g.vertices():
        if t == SOURCE or t not in bfs_parent:
            continue
        bp, cur = [], t
        while cur is not None:
            bp.append(cur); cur = bfs_parent[cur]
        bp.reverse()
        dp = reconstruct_path(prev, SOURCE, t, dist)
        f.write(f"| {t} | {' > '.join(bp)} | {path_cost(g, bp)} | {' > '.join(dp)} | {dist[t]} |\n")

# ---- test table + rejected cases ----------------------------------------
cases = run_cases()
with open("test_results.md", "w") as f:
    f.write("| # | Test | Expected | Observed | Status |\n|---:|---|---|---|---|\n")
    for n, desc, exp, obs, st in cases:
        e = str(exp).replace("|", "/"); o = str(obs).replace("|", "/")
        f.write(f"| {n} | {desc} | {e} | {o} | {st} |\n")
    f.write(f"\n{sum(c[4]=='PASS' for c in cases)}/{len(cases)} passed\n")
print(open("test_results.md").read().splitlines()[-1])

neg = Graph(directed=True)
neg.add_edge("A", "B", 4); neg.add_edge("A", "C", 5); neg.add_edge("C", "B", -3)
with open("rejected_cases.txt", "w") as f:
    try:
        dijkstra(neg, "A")
    except NegativeWeightError as e:
        f.write(f"dijkstra(neg, 'A') -> NegativeWeightError: {e}\n")
    wrong, _ = dijkstra(neg, "A", check_negative=False)
    f.write(f"Unchecked Dijkstra A->B = {wrong['B']}; true shortest (Bellman-Ford) = {bellman_ford(neg, 'A')['B']} (A>C>B = 5 + -3)\n")
    try:
        bfs(g, "Nope")
    except KeyError as e:
        f.write(f"bfs(g, 'Nope') -> KeyError: {e}\n")

# ---- diagram ---------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
pos = {"Gate": (0, 2), "Admin": (2, 3.8), "Library": (4.2, 3.8), "ScienceLab": (2, 0.4),
       "Cafeteria": (5, 2), "Gym": (7.6, 1.2), "Dorm": (6.6, -0.8), "Chapel": (3.4, -1.3),
       "Annex": (8, 3.6)}
fig, ax = plt.subplots(figsize=(10, 6.5))
for u, v, w in g.edges():
    (x1, y1), (x2, y2) = pos[u], pos[v]
    ax.plot([x1, x2], [y1, y2], color="#888", zorder=1)
    ax.text((x1 + x2) / 2, (y1 + y2) / 2, str(w), ha="center", va="center", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"), zorder=3)
for v, (x, y) in pos.items():
    ax.scatter([x], [y], s=1700, color="#cfe3ff" if v != "Annex" else "#ffd6d6", ec="#345", zorder=2)
    ax.text(x, y, v, ha="center", va="center", fontsize=8, zorder=4)
ax.set_title("Campus routing graph (undirected, weights in metres; Annex is isolated)")
ax.axis("off"); fig.tight_layout(); fig.savefig("graph_diagram.png", dpi=130)
print("done")
