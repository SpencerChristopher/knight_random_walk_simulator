import argparse
import matplotlib.pyplot as plt
import numpy as np
from knight_random_walk_simulator import KnightSimulator

def main():
    parser = argparse.ArgumentParser(
        description="Run a Monte Carlo simulation of a knight's random walk."
    )
    parser.add_argument(
        "--simulations",
        type=int,
        default=1_000_000,
        help="Number of simulations to run (default: 1,000,000)"
    )
    parser.add_argument(
        "--moves",
        type=int,
        default=50,
        help="Number of moves per simulation (default: 50)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="simulation_results.png",
        help="Output file name for the histogram plot (default: simulation_results.png)"
    )

    args = parser.parse_args()

    simulator = KnightSimulator()
    results = simulator.run_simulations(
        n_simulations=args.simulations,
        n_moves=args.moves
    )

    if 'error' in results:
        print(f"Error: {results['error']}")
        return

    print("\n--- Simulation Results ---")
    print(f"Mean distinct squares visited: {results['mean']:.2f}")
    print(f"Standard deviation: {results['std_dev']:.2f}")
    print(f"95% Confidence Interval: ({results['confidence_interval'][0]:.2f}, {results['confidence_interval'][1]:.2f})")
    print(f"Minimum distinct squares visited: {results['min']}")
    print(f"Maximum distinct squares visited: {results['max']}")

    # Generate and save histogram
    plt.figure(figsize=(10, 6))
    plt.hist(simulator.all_results, bins=50, edgecolor='black', alpha=0.7)
    plt.title(f"Distribution of Distinct Squares Visited (N={args.simulations}, M={args.moves})")
    plt.xlabel("Number of Distinct Squares Visited")
    plt.ylabel("Frequency")
    plt.grid(axis='y', alpha=0.75)
    plt.savefig(args.output)
    print(f"Histogram saved to {args.output}")

if __name__ == "__main__":
    main()
