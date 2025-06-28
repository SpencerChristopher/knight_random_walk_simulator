# Knight Random Walk Simulator

This project implements a Monte Carlo simulation to estimate the expected number of distinct squares a knight visits after `n` random moves on an infinite chessboard. It features parallel processing for efficiency, memory-efficient tracking, graceful error handling, and statistical confidence reporting.

## Project Structure

The project is structured to ensure modularity, maintainability, and clear separation of concerns:

```
knight_random_walk_simulator/
├── src/
│   ├── __pycache__/                  # Python bytecode cache
│   ├── .gitignore                    # Git ignore file for source directory
│   ├── knight_random_walk_simulator.py  # Contains the KnightSimulator class (core simulation logic)
│   ├── cli.py                        # Handles all Command Line Interface (CLI) logic, argument parsing, and visualization
│   ├── main.py                       # Minimal entry point for the application, calls cli.py
│   └── requirements.txt              # Lists Python dependencies for the project
├── README.md                         # This file: project overview, structure, and usage
└── LICENSE                           # Apache 2.0 License file
```

- `knight_random_walk_simulator.py`: Encapsulates the core simulation logic within the `KnightSimulator` class, including the knight's movement and distinct square tracking.
- `cli.py`: Manages the command-line interface. It parses user arguments, orchestrates the simulation using `KnightSimulator`, processes the results, and generates visualizations.
- `main.py`: Serves as the primary entry point for the application, simply invoking the CLI module.
- `requirements.txt`: Specifies all necessary Python packages required to run the project.

## Installation

1.  **Navigate to the project root directory:**
    ```bash
    cd C:\Users\chris\PycharmProjects\knight_random_walk_simulator
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r src/requirements.txt
    ```

## Usage

To run the simulation from the command line, navigate to the project root directory and execute `main.py` with desired arguments. The CLI is handled by `src/cli.py`.

```bash
python src/main.py --help
```

Example usage:

```bash
python src/main.py --simulations 100000 --moves 100 --output my_simulation_plot.png
```

- `--simulations`: Number of simulations to run (default: 1,000,000)
- `--moves`: Number of moves per simulation (default: 50)
- `--output`: Output file name for the histogram plot (default: `simulation_results.png`)

After execution, a histogram visualizing the distribution of distinct squares visited will be saved to the specified output file, and key statistics will be printed to the console.
