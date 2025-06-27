from knight_random_walk_simulator import run_simulations

if __name__ == "__main__":
    # Configure your simulation
    results = run_simulations(
        n_simulations=2_000_000,
        n_moves=50
    )
    print(f"Average distinct squares: {results['mean']:.2f}")