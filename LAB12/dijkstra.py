"""Dijkstra's single-source shortest paths using heapq.

Ties: heap entries are (distance, vertex_name), so equal distances pop in
alphabetical order, and a distance is replaced only when strictly smaller.
The first shortest path found therefore wins, deterministically.
"""
import heapq
import math


class NegativeWeightError(ValueError):
    """Dijkstra is only valid for non-negative edge weights."""


def dijkstra(graph, source, check_negative=True, trace=None):
    """Return (dist, prev). dist[v] is math.inf for unreachable vertices.

    check_negative=False exists ONLY to demonstrate why negative weights break
    the algorithm (see test_graph.py); never use it for real routing.
    `trace`, if a list, receives one row per heap pop.
    """
    if not graph.has_vertex(source):
        raise KeyError(f"unknown source vertex {source!r}")
    if check_negative and graph.has_negative_weight():
        raise NegativeWeightError("graph has a negative edge weight; "
                                  "Dijkstra's algorithm is not valid")
    dist = {v: math.inf for v in graph.vertices()}
    prev = {v: None for v in graph.vertices()}
    dist[source] = 0
    heap = [(0, source)]
    done = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:                     # stale heap entry
            if trace is not None:
                trace.append((d, u, "stale, skipped", []))
            continue
        done.add(u)
        changed = []
        for v, w in graph.neighbors(u):
            if v not in done and d + w < dist[v]:
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))
                changed.append(f"{v}={dist[v]}")
        if trace is not None:
            trace.append((d, u, "settled", changed))
    return dist, prev


def reconstruct_path(prev, source, target, dist=None):
    """Path source..target as a list, or None when target is unreachable."""
    if dist is not None and dist.get(target, math.inf) == math.inf:
        return None
    path, cur = [], target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path if path and path[0] == source else None


def path_cost(graph, path):
    """Sum of edge weights along a path (used to verify results by hand)."""
    return sum(dict(graph.neighbors(a))[b] for a, b in zip(path, path[1:]))
