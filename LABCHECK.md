# Laboratory Submission Recheck

**Course:** CPEPRO8L — Data Structures and Algorithms Laboratory  
**Student:** Runzyle V. Vistro  
**Repository:** `kazutosungjin-cpu/CPEPRO8L-DSA-Laboratories-VISTRO-`  
**Recheck date:** August 14, 2026  
**Status:** Provisional repository-based evaluation

## Recheck Summary

- Labs found: **1–7**
- Newly evaluated: **Labs 5, 6, and 7**
- Missing from the current sequence: **None**
- All submitted Python files compile successfully.
- All seven implementations pass the functional and edge-case tests.

## Evaluation Criteria

| Criterion | Weight |
|---|---:|
| Program Correctness and Functionality | 40% |
| Code Quality and Organization | 20% |
| Analysis and Understanding | 20% |
| Documentation (`README.md`) | 10% |
| GitHub Repository Organization and Submission | 10% |
| **Total** | **100%** |

## Updated Results

| Laboratory | Correctness /40 | Code /20 | Analysis /20 | Documentation /10 | Repository /10 | Grade |
|---:|---:|---:|---:|---:|---:|---:|
| Lab 1 | 40 | 18 | 20 | 10 | 8 | **96/100** |
| Lab 2 | 40 | 17 | 19 | 9 | 9 | **94/100** |
| Lab 3 | 40 | 18 | 20 | 9 | 9 | **96/100** |
| Lab 4 | 40 | 18 | 20 | 9 | 9 | **96/100** |
| Lab 5 | 40 | 15 | 20 | 7 | 7 | **89/100** |
| Lab 6 | 40 | 18 | 20 | 8 | 8 | **94/100** |
| Lab 7 | 40 | 18 | 20 | 7 | 8 | **93/100** |
| **Average of submitted labs** | **40.0** | **17.4** | **19.9** | **8.4** | **8.3** | **94.0/100** |

## Verified Tests

- Labs 1–4: all previous correctness and pointer tests remain passing.
- Lab 5: stack LIFO behavior, underflow, and ten balanced/unbalanced expressions
- Lab 6: FIFO ordering, overflow, underflow, full-capacity behavior, and circular wraparound
- Lab 7: first, middle, and last targets; absent target; empty-array base case

## Important Documentation Finding

The new functions are correct, but several console traces in the reports cannot be reproduced by running the submitted source files as written:

- **Lab 5:** The report shows five customized expression tests, but the source file executes only two expressions.
- **Lab 6:** The report shows a 10-operation queue trace, but the source file executes only the short four-enqueue sample.
- **Lab 7:** The report shows results for targets `23`, `56`, and `99`, but the source file executes only target `23`.

This does not invalidate the correct functions, but it reduces code quality, documentation reliability, and reproducibility.

## Corrections Required

1. Rename `LAB 5/LAB REPORT 5.py` to the required `lab5_bracket_parser.py`.
2. Add the five customized expression tests to the Lab 5 source file.
3. Add the documented 10-operation trace driver to the Lab 6 source file.
4. Add the documented `23`, `56`, and `99` target tests to the Lab 7 source file.
5. Rename `LAB REPORT 6.md` and `LAB REPORT 7.md` to `README.md` within their lab folders.
6. Expand the root README with navigation links to Labs 1–7.
7. Use a consistent folder and filename convention without spaces or ambiguous labels.

## Instructor Note

The repository now contains the complete Lab 1–7 sequence, and every implementation passed independent tests. The primary deductions on the new laboratories concern mismatches between claimed console output and the executable driver code. Scores may be adjusted for deadlines, late submissions, or an oral/code defense.
