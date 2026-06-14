#' Benchmark Script for ExplicitExploration (EES)
#'
#' This script runs a comparative benchmark for the ExplicitExploration 
#' algorithm using the native sphere objective function from the EEEA package,
#' with a specified maximum iteration constraint.

# Install and load the EEEA package from the global mirror
if (!requireNamespace("EEEA", quietly = TRUE)) {
    install.packages("EEEA", repos = "https://cloud.r-project.org")
}
library(EEEA)

# Base configuration for the benchmark
runs <- 30  # 30 independent runs
dimensions <- 10
lower_bound <- rep(-5.12, dimensions)
upper_bound <- rep(5.12, dimensions)
max_iterations <- 100  # Maximum iteration limit

# Data frame to store results
results <- data.frame(
    Algorithm = character(),
    Run = integer(),
    Time_Seconds = numeric(),
    Best_Fitness = numeric(),
    stringsAsFactors = FALSE
)

cat("Starting benchmark for ExplicitExploration (EES)...\n")

# Execution loop for ExplicitExploration
for (i in 1:runs) {
    start_time <- Sys.time()

    # Run algorithm with the maxiter parameter included
    res_ee <- ExplicitExploration(
        fun = sphere,
        lower = lower_bound,
        upper = upper_bound,
        maxiter = max_iterations
    )

    end_time <- Sys.time()
    execution_time <- as.numeric(difftime(end_time, start_time, units = "secs"))

    # Extract the best result based on the source code (the minimum of vector Y)
    best_val <- min(res_ee$Y)

    # Record in the data frame
    results <- rbind(
        results,
        data.frame(
            Algorithm = "ExplicitExploration",
            Run = i,
            Time_Seconds = execution_time,
            Best_Fitness = best_val
        )
    )
}

# Save results in the data folder
save_path <- "data/results_r.csv"
write.csv(results, save_path, row.names = FALSE)
cat("Success! EES data has been saved to:", save_path, "\n")