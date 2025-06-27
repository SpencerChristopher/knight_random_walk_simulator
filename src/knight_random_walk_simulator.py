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
import numpy as np
from typing import Tuple, Set

# All 8 possible L-shaped knight moves, precomputed for efficiency
KNIGHT_MOVES: Tuple[Tuple[int, int], ...] = (
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
)


def simulate_knight_walk(n_moves: int) -> int:
    """
    Simulates one complete random walk of the knight.

    Args:
        n_moves: Number of moves to simulate

    Returns:
        Number of distinct squares visited
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
        n_moves: int = 50,
        confidence_interval: float = 0.95
) -> dict:
    try:
        n_workers = min(cpu_count(), n_simulations // 1000)
        with Pool(n_workers) as pool:
            # FIX: Use tuples for starmap or switch to map
            results = pool.starmap(simulate_knight_walk, [(n_moves,)] * n_simulations)
            # OR: results = pool.map(simulate_knight_walk, [n_moves] * n_simulations)

        mean = np.mean(results)
        std = np.std(results)
        conf_width = 1.96 * (std / np.sqrt(n_simulations))
        return {
            'mean': mean,
            'std_dev': std,
            'confidence_interval': (mean - conf_width, mean + conf_width),
            'min': min(results),
            'max': max(results)
        }
    except Exception as e:
        print(f"Simulation failed: {str(e)}")
        return {'error': str(e)}



