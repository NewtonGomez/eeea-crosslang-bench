import os
import sys
import time
import numpy as np
import pandas as pd

# Import eeea modules
from eeea_py.algorithms.EES import explicit_exploration
from eeea_py.benchmarks.unimodal import sphere_function

# Base configuration for the benchmark (identical to R)
runs = 30  # 30 independent runs
dim = 10  # Dimensions
lb = np.repeat(-5.12, dim)  # Lower bound
ub = np.repeat(5.12, dim)  # Upper bound

# Default parameters extracted from the original R code for EES
n = 30  # Population size
tol = 0.01  # Error tolerance
K = 5  # Consecutive generations
maxiter = 100  # Maximum iteration limit

# List to temporarily store the results
results_list = []

print("Starting benchmark for Explicit Exploration Strategy (Python)...")

# Execution loop
for i in range(1, runs + 1):
    # Start high-precision timer
    start_time = time.perf_counter()

    # Execute algorithm
    best_individuals = explicit_exploration(
        fitness_fun=sphere_function,
        dim=dim,
        lb=lb,
        ub=ub,
        n=n,
        tol=tol,
        K=K,
        maxiter=maxiter,
    )

    # Stop timer
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    # Extract the best fitness
    # Since the function returns a sorted matrix, best_individuals[0] is the best individual
    best_individual = best_individuals[0]
    best_fitness = sphere_function(best_individual)

    # Record into the list
    results_list.append(
        {
            "Algorithm": "ExplicitExploration",
            "Run": i,
            "Time_Seconds": execution_time,
            "Best_Fitness": best_fitness,
        }
    )

# Convert to DataFrame and save
results = pd.DataFrame(results_list)

# Ensure the data directory exists
data_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data")
)
os.makedirs(data_path, exist_ok=True)

# Export to CSV
save_path = os.path.join(data_path, "results_py.csv")
results.to_csv(save_path, index=False)

print(f"Success! Python data has been saved to: {save_path}")