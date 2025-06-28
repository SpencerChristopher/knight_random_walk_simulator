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


class KnightSimulator:
    """
    A class to simulate the random walk of a knight on an infinite chessboard
    and analyze the results.
    """

    # All 8 possible L-shaped knight moves, precomputed for efficiency
    _KNIGHT_MOVES: Tuple[Tuple[int, int], ...] = (
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
    )

    def __init__(self):
        self.all_results = None  # To store raw simulation results for plotting

    def _simulate_knight_walk(self, n_moves: int) -> int:
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
        for _ in range(n_moves):
            move = random.choice(self._KNIGHT_MOVES)
            position = (position[0] + move[0], position[1] + move[1])
            visited.add(position)
        return len(visited)

    def run_simulations(
            self,
            n_simulations: int = 1_000_000,
            n_moves: int = 50
    ) -> dict:
        """
        Runs a specified number of knight walk simulations in parallel.

        This method uses multiprocessing to distribute the simulations across
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
            n_workers = max(1, min(cpu_count(), n_simulations // 1000 if n_simulations >= 1000 else 1))
            with Pool(n_workers) as pool:
                chunksize = max(1, n_simulations // (n_workers * 4))
                results_iterator = pool.imap_unordered(
                    self._simulate_knight_walk, repeat(n_moves, n_simulations), chunksize=chunksize
                )
                self.all_results = np.fromiter(results_iterator, dtype=int, count=n_simulations)

            mean = np.mean(self.all_results)
            std = np.std(self.all_results)
            conf_width = 1.96 * (std / np.sqrt(n_simulations))
            return {
                'mean': mean,
                'std_dev': std,
                'confidence_interval': (mean - conf_width, mean + conf_width),
                'min': int(np.min(self.all_results)),
                'max': int(np.max(self.all_results))
            }
        except Exception as e:
            print(f"An unexpected error occurred during simulation: {str(e)}")
            return {'error': f"Simulation failed due to an unexpected error: {str(e)}"}



