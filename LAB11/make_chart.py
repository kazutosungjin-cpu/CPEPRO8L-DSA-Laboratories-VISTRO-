"""Builds comparison_chart.png and results_table.md from benchmark_results.csv"""
import csv
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

data = defaultdict(dict)
conds, sizes, algs = [], set(), []
with open("benchmark_results.csv") as f:
    for r in csv.DictReader(f):
        if r["condition"] not in conds: conds.append(r["condition"])
        if r["algorithm"] not in algs: algs.append(r["algorithm"])
        sizes.add(int(r["n"]))
        if r["status"] == "OK":
            data[(r["algorithm"], r["condition"])][int(r["n"])] = float(r["median_seconds"]) * 1000
sizes = sorted(sizes)

fig, axes = plt.subplots(2, 2, figsize=(12, 9))
for ax, c in zip(axes.flat, conds):
    for a in algs:
        d = data[(a, c)]
        ax.plot(sorted(d), [d[k] for k in sorted(d)], marker="o", label=a)
    ax.set_title(f"{c} data"); ax.set_xlabel("n"); ax.set_ylabel("median ms")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.grid(True, alpha=.3)
axes[0][0].legend(fontsize=8)
fig.suptitle("Median runtime vs input size (log-log)")
fig.tight_layout(); fig.savefig("comparison_chart.png", dpi=130)

with open("results_table.md", "w") as f:
    for c in conds:
        f.write(f"\n**{c}** (median ms)\n\n| Algorithm | " + " | ".join(f"n={n}" for n in sizes) + " |\n")
        f.write("|---|" + "---:|" * len(sizes) + "\n")
        for a in algs:
            f.write(f"| {a} | " + " | ".join(
                f"{data[(a,c)][n]:.2f}" if n in data[(a,c)] else "skipped" for n in sizes) + " |\n")
