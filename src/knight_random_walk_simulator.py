"""
Monte Carlo simulation to estimate the expected number of distinct squares
a knight visits after n random moves on an infinite chessboard.

Key Features:
- Parallel processing for speed
- Memory-efficient tracking
- Graceful error handling
- Statistical confidence reporting
"""

import random
from multiprocessing import Pool, cpu_count
from itertools import repeat
import numpy as np
from typing import Tuple, Set

# All 8 possible L-shaped knight moves, precomputed for efficiency
KNIGHT_MOVES: Tuple[Tuple[int, int], ...] = (
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
)


def simulate_knight_walk(n_moves: int) -> int:
    """
    Simulates a single random walk of a knight on an infinite chessboard.

    The walk starts at (0, 0). In each step, the knight chooses one of the 8
    possible moves at random. The function tracks the number of distinct
    squares visited during the walk.

    Args:
        n_moves: The total number of moves to simulate in the walk.

    Returns:
        The number of distinct squares visited by the knight.
    """
    position = (0, 0)
    visited: Set[Tuple[int, int]] = {position}
    #iterating move count
    for _ in range(n_moves):
        # Randomly select one of the 8 possible moves
        move = random.choice(KNIGHT_MOVES)
        # Update position
        position = (position[0] + move[0], position[1] + move[1])
        # Track unique positions
        visited.add(position)

    return len(visited)


def run_simulations(
        n_simulations: int = 1_000_000,
        n_moves: int = 50
) -> dict:
    """
    Runs a specified number of knight walk simulations in parallel.

    This function uses multiprocessing to distribute the simulations across
    multiple CPU cores, significantly speeding up the computation. It collects
    the results and computes key statistical measures.

    Args:
        n_simulations: The total number of simulations to run.
        n_moves: The number of moves for each individual simulation.

    Returns:
        A dictionary containing the simulation results, including:
        - 'mean': The average number of distinct squares visited.
        - 'std_dev': The standard deviation of the results.
        - 'confidence_interval': A tuple with the 95% confidence interval.
        - 'min': The minimum number of distinct squares visited.
        - 'max': The maximum number of distinct squares visited.
        - 'error': An error message, if the simulation failed.

    """
    if n_simulations <= 0 or n_moves < 0:
        return {'error': "Number of simulations and moves must be positive."}
    try:
        # Ensure at least one worker, and not more than available CPUs
        n_workers = max(1, min(cpu_count(), n_simulations // 1000 if n_simulations >= 1000 else 1))
        
        # For memory efficiency, process results as they complete using an iterator
        with Pool(n_workers) as pool:
            # Calculate a chunk size to balance overhead and memory usage.
            # This distributes the simulations into larger batches for each worker.
            chunksize = max(1, n_simulations // (n_workers * 4))

            # Use imap_unordered with itertools.repeat to avoid creating large lists in memory.
            # np.fromiter efficiently builds a NumPy array from the iterator.
            results_iterator = pool.imap_unordered(
                simulate_knight_walk, repeat(n_moves, n_simulations), chunksize=chunksize
            )
            results = np.fromiter(results_iterator, dtype=int, count=n_simulations)

        mean = np.mean(results)
        std = np.std(results)
        # Using 1.96 for a 95% confidence interval
        conf_width = 1.96 * (std / np.sqrt(n_simulations))
        return {
            'mean': mean,
            'std_dev': std,
            'confidence_interval': (mean - conf_width, mean + conf_width),
            'min': int(np.min(results)),
            'max': int(np.max(results))
        }
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"An unexpected error occurred during simulation: {str(e)}")
        return {'error': f"Simulation failed due to an unexpected error: {str(e)}"}



