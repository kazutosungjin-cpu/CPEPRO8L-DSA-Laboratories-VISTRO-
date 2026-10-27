| # | Test | Expected | Observed | Status |
|---:|---|---|---|---|
| 1 | Graph has 9 vertices / 11 edges | (9, 11) | (9, 11) | PASS |
| 2 | Structure matches source CSV | [] | [] | PASS |
| 3 | BFS from Gate | ['Gate', 'Admin', 'Chapel', 'ScienceLab', 'Cafeteria', 'Library', 'Dorm', 'Gym'] | ['Gate', 'Admin', 'Chapel', 'ScienceLab', 'Cafeteria', 'Library', 'Dorm', 'Gym'] | PASS |
| 4 | DFS from Gate | ['Gate', 'Admin', 'Cafeteria', 'Gym', 'Dorm', 'Chapel', 'ScienceLab', 'Library'] | ['Gate', 'Admin', 'Cafeteria', 'Gym', 'Dorm', 'Chapel', 'ScienceLab', 'Library'] | PASS |
| 5 | BFS from Dorm | ['Dorm', 'Chapel', 'Gym', 'Gate', 'ScienceLab', 'Cafeteria', 'Admin', 'Library'] | ['Dorm', 'Chapel', 'Gym', 'Gate', 'ScienceLab', 'Cafeteria', 'Admin', 'Library'] | PASS |
| 6 | DFS from Dorm | ['Dorm', 'Chapel', 'Gate', 'Admin', 'Cafeteria', 'Gym', 'Library', 'ScienceLab'] | ['Dorm', 'Chapel', 'Gate', 'Admin', 'Cafeteria', 'Gym', 'Library', 'ScienceLab'] | PASS |
| 7 | Recursive DFS == explicit-stack DFS (Gate) | ['Gate', 'Admin', 'Cafeteria', 'Gym', 'Dorm', 'Chapel', 'ScienceLab', 'Library'] | ['Gate', 'Admin', 'Cafeteria', 'Gym', 'Dorm', 'Chapel', 'ScienceLab', 'Library'] | PASS |
| 8 | Dijkstra distances from Gate | {'Admin': 2, 'Annex': inf, 'Cafeteria': 8, 'Chapel': 12, 'Dorm': 15, 'Gate': 0, 'Gym': 12, 'Library': 3, 'ScienceLab': 3} | {'Admin': 2, 'Annex': inf, 'Cafeteria': 8, 'Chapel': 12, 'Dorm': 15, 'Gate': 0, 'Gym': 12, 'Library': 3, 'ScienceLab': 3} | PASS |
| 9 | Path Gate->Dorm (cost 3+9+3=15) | (['Gate', 'ScienceLab', 'Chapel', 'Dorm'], 15) | (['Gate', 'ScienceLab', 'Chapel', 'Dorm'], 15) | PASS |
| 10 | Path Gate->Cafeteria (cost 2+1+5=8) | (['Gate', 'Admin', 'Library', 'Cafeteria'], 8) | (['Gate', 'Admin', 'Library', 'Cafeteria'], 8) | PASS |
| 11 | Equal-cost alternative Gate-ScienceLab-Cafeteria also costs 8 | 8 | 8 | PASS |
| 12 | Unreachable target Annex (dist inf, no path) | (inf, None) | (inf, None) | PASS |
| 13 | Isolated vertex Annex: BFS and DFS visit only itself | (['Annex'], ['Annex']) | (['Annex'], ['Annex']) | PASS |
| 14 | Cycle A-B-C: BFS/DFS terminate, each vertex once | (['A', 'B', 'C'], ['A', 'B', 'C']) | (['A', 'B', 'C'], ['A', 'B', 'C']) | PASS |
| 15 | Negative weight rejected by Dijkstra | NegativeWeightError | NegativeWeightError | PASS |
| 16 | Why negative is invalid: unchecked Dijkstra says A->B=4, true value 2 | (4, 2) | (4, 2) | PASS |
| 17 | Directed edge X->Y: Y cannot reach X | (['X', 'Y'], ['Y']) | (['X', 'Y'], ['Y']) | PASS |
| 18 | BFS tree (1 edge, weight 20) differs from shortest-path tree (2 edges, weight 12) | (['Gate', 'Chapel'], ['Gate', 'ScienceLab', 'Chapel']) | (['Gate', 'Chapel'], ['Gate', 'ScienceLab', 'Chapel']) | PASS |
| 19 | Unknown start vertex raises KeyError | ('KeyError', 'KeyError') | ('KeyError', 'KeyError') | PASS |
| 20 | Non-numeric weight rejected | TypeError | TypeError | PASS |
| 21 | Dijkstra == Bellman-Ford from every source vertex | True | True | PASS |

21/21 passed
