"""BFS (queue) and DFS (recursive and explicit-stack) with deterministic order.

Both return (order, parent): `order` lists vertices in visit order and
`parent` maps each reached vertex to the vertex it was discovered from
(None for the start), which describes the traversal tree.
"""
from collections import deque


def _check(graph, start):
    if not graph.has_vertex(start):
        raise KeyError(f"unknown start vertex {start!r}")


def bfs(graph, start):
    _check(graph, start)
    visited = {start}
    parent = {start: None}
    order = []
    queue = deque([start])
    while queue:
        u = queue.popleft()
        order.append(u)
        for v, _ in graph.neighbors(u):
            if v not in visited:          # mark on enqueue -> no duplicates
                visited.add(v)
                parent[v] = u
                queue.append(v)
    return order, parent


def dfs(graph, start):
    """Recursive DFS."""
    _check(graph, start)
    visited, parent, order = set(), {start: None}, []

    def visit(u):
        visited.add(u)
        order.append(u)
        for v, _ in graph.neighbors(u):
            if v not in visited:
                parent[v] = u
                visit(v)

    visit(start)
    return order, parent


def bfs_trace(graph, start):
    """Rows of (selected vertex, queue after step, visited after step)."""
    _check(graph, start)
    visited, queue, rows = {start}, deque([start]), []
    rows.append(("(start)", list(queue), sorted(visited)))
    while queue:
        u = queue.popleft()
        for v, _ in graph.neighbors(u):
            if v not in visited:
                visited.add(v)
                queue.append(v)
        rows.append((u, list(queue), sorted(visited)))
    return rows


def dfs_stack_trace(graph, start):
    """Explicit-stack DFS (visit on pop; unvisited neighbors pushed in
    reverse alphabetical order so the alphabetically first is popped first).
    Rows of (popped vertex, action, stack top-at-right, visited, order)."""
    _check(graph, start)
    stack, visited, order, rows = [start], set(), [], []
    parent = {start: None}
    while stack:
        u = stack.pop()
        if u in visited:
            rows.append((u, "skip (already visited)", list(stack), sorted(visited), list(order)))
            continue
        visited.add(u)
        order.append(u)
        for v, _ in reversed(graph.neighbors(u)):
            if v not in visited:
                stack.append(v)
        rows.append((u, "visit", list(stack), sorted(visited), list(order)))
    return order, rows
