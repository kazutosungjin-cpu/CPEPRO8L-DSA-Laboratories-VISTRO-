# Hand Traces (worked out on paper before running the program)

Graph: campus_edges.csv (undirected, metres). Neighbor rule: **alphabetical**.

Adjacency lists (alphabetical):
- Admin: Cafeteria 7, Gate 2, Library 1
- Annex: (none)
- Cafeteria: Admin 7, Gym 4, Library 5, ScienceLab 5
- Chapel: Dorm 3, Gate 20, ScienceLab 9
- Dorm: Chapel 3, Gym 6
- Gate: Admin 2, Chapel 20, ScienceLab 3
- Gym: Cafeteria 4, Dorm 6
- Library: Admin 1, Cafeteria 5
- ScienceLab: Cafeteria 5, Chapel 9, Gate 3

## 1. BFS from Gate (queue front at left; vertices marked visited when enqueued)

| Step | Selected (dequeued) | Enqueued | Queue after | Order so far |
|---:|---|---|---|---|
| 0 | – | Gate | [Gate] | – |
| 1 | Gate | Admin, Chapel, ScienceLab | [Admin, Chapel, ScienceLab] | Gate |
| 2 | Admin | Cafeteria, Library (Gate already visited) | [Chapel, ScienceLab, Cafeteria, Library] | Gate, Admin |
| 3 | Chapel | Dorm | [ScienceLab, Cafeteria, Library, Dorm] | …, Chapel |
| 4 | ScienceLab | none | [Cafeteria, Library, Dorm] | …, ScienceLab |
| 5 | Cafeteria | Gym | [Library, Dorm, Gym] | …, Cafeteria |
| 6 | Library | none | [Dorm, Gym] | …, Library |
| 7 | Dorm | none | [Gym] | …, Dorm |
| 8 | Gym | none | [] | …, Gym |

**BFS order:** Gate, Admin, Chapel, ScienceLab, Cafeteria, Library, Dorm, Gym (Annex unreachable).

## 2. DFS from Gate (explicit stack, top at right; visit on pop; unvisited neighbors pushed in reverse alphabetical order)

| Step | Pop | Action | Stack after | Order so far |
|---:|---|---|---|---|
| 1 | Gate | visit, push ScienceLab, Chapel, Admin | [ScienceLab, Chapel, Admin] | Gate |
| 2 | Admin | visit, push Library, Cafeteria | [S, Chapel, Library, Cafeteria] | Gate, Admin |
| 3 | Cafeteria | visit, push ScienceLab, Library, Gym | [S, Chapel, Library, S, Library, Gym] | …, Cafeteria |
| 4 | Gym | visit, push Dorm | [S, Chapel, Library, S, Library, Dorm] | …, Gym |
| 5 | Dorm | visit, push Chapel | [S, Chapel, Library, S, Library, Chapel] | …, Dorm |
| 6 | Chapel | visit, push ScienceLab | [S, Chapel, Library, S, Library, S] | …, Chapel |
| 7 | ScienceLab | visit, nothing new | [S, Chapel, Library, S, Library] | …, ScienceLab |
| 8 | Library | visit, nothing new | [S, Chapel, Library, S] | …, Library |
| 9–12 | ScienceLab, Library, Chapel, ScienceLab | already visited, skip | [] | unchanged |

(S = ScienceLab.) **DFS order:** Gate, Admin, Cafeteria, Gym, Dorm, Chapel, ScienceLab, Library.
Recursive reading: Gate → Admin → Cafeteria → Gym → Dorm → Chapel → ScienceLab, backtrack to Cafeteria → Library.

## 3. Second start vertex: Dorm

BFS: [Dorm] → pop Dorm, enqueue Chapel, Gym → pop Chapel, enqueue Gate, ScienceLab → pop Gym, enqueue Cafeteria → pop Gate, enqueue Admin → pop ScienceLab (nothing) → pop Cafeteria, enqueue Library → pop Admin, Library.
**BFS order:** Dorm, Chapel, Gym, Gate, ScienceLab, Cafeteria, Admin, Library.

DFS (recursive): Dorm → Chapel → Gate → Admin → Cafeteria → Gym (Dorm visited, back) → Library → ScienceLab.
**DFS order:** Dorm, Chapel, Gate, Admin, Cafeteria, Gym, Library, ScienceLab.

## 4. Dijkstra from Gate (min-heap of (distance, vertex); ties pop alphabetically)

| Pop | Action | Updates | dist after |
|---|---|---|---|
| (0, Gate) | settle | Admin=2, Chapel=20, ScienceLab=3 | Admin 2, Chapel 20, ScienceLab 3 |
| (2, Admin) | settle | Cafeteria=2+7=9, Library=2+1=3 | + Cafeteria 9, Library 3 |
| (3, Library) | settle | Cafeteria=3+5=8 (< 9) | Cafeteria 8 (prev Library) |
| (3, ScienceLab) | settle | Cafeteria 3+5=8 not < 8 (tie, keep Library); Chapel=3+9=12 (< 20) | Chapel 12 (prev ScienceLab) |
| (8, Cafeteria) | settle | Gym=8+4=12 | Gym 12 |
| (9, Cafeteria) | stale, skip | – | – |
| (12, Chapel) | settle | Dorm=12+3=15 | Dorm 15 |
| (12, Gym) | settle | Dorm 12+6=18 not < 15 | – |
| (15, Dorm) | settle | – | – |
| (20, Chapel) | stale, skip | – | – |

Annex is never reached: distance = ∞.

**Manual verification by summing edge weights**
- Gate → Dorm: Gate–ScienceLab 3 + ScienceLab–Chapel 9 + Chapel–Dorm 3 = **15**. The other routes are longer: Gate–Chapel–Dorm = 23; via Cafeteria–Gym = 8+4+6 = 18.
- Gate → Cafeteria: Gate–Admin 2 + Admin–Library 1 + Library–Cafeteria 5 = **8**. Equal-cost alternative Gate–ScienceLab 3 + ScienceLab–Cafeteria 5 = **8**; direct Gate–Admin–Cafeteria = 9.
- Gate → Chapel: 3 + 9 = **12**, beating the direct 20 m edge.

Equal-cost rule: Library and ScienceLab both settle at distance 3, Library pops first (alphabetical), and a later equal distance does not replace it, so the reported path goes through Library.
