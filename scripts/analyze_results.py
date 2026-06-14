import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import mannwhitneyu

# Configure read and save paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DOCS_DIR = os.path.join(BASE_DIR, "..", "results")  # For saving the plots

# Ensure the docs directory exists to save the plots
os.makedirs(DOCS_DIR, exist_ok=True)

r_path = os.path.join(DATA_DIR, "results_r.csv")
py_path = os.path.join(DATA_DIR, "results_py.csv")

# Validate that the files exist before proceeding
if not os.path.exists(r_path) or not os.path.exists(py_path):
    raise FileNotFoundError(
        "Make sure you have previously run benchmark_r.R and benchmark_py.py"
    )

# Load data and identify the language
df_r = pd.read_csv(r_path)
df_r["Language"] = "R"

df_py = pd.read_csv(py_path)
df_py["Language"] = "Python"

# Unify both datasets into a single table to facilitate Seaborn handling
df_total = pd.concat([df_r, df_py], ignore_index=True)

# Display descriptive statistics in the terminal
print("=" * 60)
print(" DESCRIPTIVE METRICS (EXPLICIT EXPLORATION)")
print("=" * 60)
print("\n--- EXECUTION TIME (SECONDS) ---")
# '50%' represents the median value
print(
    df_total.groupby("Language")["Time_Seconds"].describe()[
        ["mean", "50%", "std"]
    ]
)

print("\n--- SOLUTION QUALITY (BEST FITNESS) ---")
print(
    df_total.groupby("Language")["Best_Fitness"].describe()[
        ["mean", "50%", "std"]
    ]
)

# Statistical Tests (Mann-Whitney U)
# This non-parametric test is used because fitness in evolutionary
# algorithms is usually non-normally distributed.
u_stat_t, p_val_t = mannwhitneyu(df_r["Time_Seconds"], df_py["Time_Seconds"])
u_stat_f, p_val_f = mannwhitneyu(df_r["Best_Fitness"], df_py["Best_Fitness"])

print("\n" + "=" * 60)
print(" STATISTICAL HYPOTHESIS TESTS (MANN-WHITNEY U)")
print("=" * 60)
print(
    f"Execution Time -> p-value: {p_val_t:.5f} "
    + (
        "(Significant Difference)"
        if p_val_t < 0.05
        else "(No Significant Difference)"
    )
)
print(
    f"Best Fitness   -> p-value: {p_val_f:.5f} "
    + (
        "(Significant Difference)"
        if p_val_f < 0.05
        else "(No Significant Difference)"
    )
)
print("-" * 60)
print(
    "Note: A p-value less than 0.05 demonstrates with 95% confidence "
    "that the environments perform differently.\n"
)

# Generate and save plots (box plots)
plt.figure(figsize=(12, 5))
sns.set_theme(style="whitegrid")

# Plot 1: Execution times
plt.subplot(1, 2, 1)
sns.boxplot(x="Language", y="Time_Seconds", data=df_total, palette="Set2")
plt.title("Execution Time Comparison\n(Lower is better)")
plt.xlabel("Development Environment")
plt.ylabel("Time (Seconds)")

# Plot 2: Solution quality (fitness)
plt.subplot(1, 2, 2)
sns.boxplot(x="Language", y="Best_Fitness", data=df_total, palette="Set2")
plt.title(
    "Convergence Comparison (Fitness)\n(Closer to 0 is better for Sphere)"
)
plt.xlabel("Development Environment")
plt.ylabel("Best Fitness Found")

plt.tight_layout()

# Save the plot in the docs directory
plot_path = os.path.join(DOCS_DIR, "ees_comparison.png")
plt.savefig(plot_path, dpi=300)
plt.close()

print(f"Success! The comparative plot has been saved to: {plot_path}")