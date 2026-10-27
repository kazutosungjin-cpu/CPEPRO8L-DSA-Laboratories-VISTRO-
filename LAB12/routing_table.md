Source: Gate

| Target | Distance (m) | Shortest path | Edges |
|---|---:|---|---:|
| Admin | 2 | Gate > Admin | 1 |
| Annex | unreachable | - | - |
| Cafeteria | 8 | Gate > Admin > Library > Cafeteria | 3 |
| Chapel | 12 | Gate > ScienceLab > Chapel | 2 |
| Dorm | 15 | Gate > ScienceLab > Chapel > Dorm | 3 |
| Gate | 0 | Gate | 0 |
| Gym | 12 | Gate > Admin > Library > Cafeteria > Gym | 4 |
| Library | 3 | Gate > Admin > Library | 2 |
| ScienceLab | 3 | Gate > ScienceLab | 1 |

**BFS tree vs shortest-path tree (from Gate)**

| Target | BFS path (min edges) | BFS cost | Dijkstra path | Dijkstra cost |
|---|---|---:|---|---:|
| Admin | Gate > Admin | 2 | Gate > Admin | 2 |
| Cafeteria | Gate > Admin > Cafeteria | 9 | Gate > Admin > Library > Cafeteria | 8 |
| Chapel | Gate > Chapel | 20 | Gate > ScienceLab > Chapel | 12 |
| Dorm | Gate > Chapel > Dorm | 23 | Gate > ScienceLab > Chapel > Dorm | 15 |
| Gym | Gate > Admin > Cafeteria > Gym | 13 | Gate > Admin > Library > Cafeteria > Gym | 12 |
| Library | Gate > Admin > Library | 3 | Gate > Admin > Library | 3 |
| ScienceLab | Gate > ScienceLab | 3 | Gate > ScienceLab | 3 |
