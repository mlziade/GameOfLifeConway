import time
import json
import os
from datetime import datetime
from statistics import median

def check_cell(x_pos: int, y_pos: int, cell_state: bool, grid: set[tuple[int, int]]) -> bool:    
    # Count neighbors
    total = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # Skip the cell itself
            neighbor_pos = (x_pos + i, y_pos + j)
            if neighbor_pos in grid:
                total += 1

    if cell_state == False:     
        # Dead cell with exactly 3 neighbors becomes alive
        if total == 3:
            return True
        # Otherwise remains dead
        return False
    
    else:  # cell_state == 1
        # Live cell with 2 or 3 neighbors survives
        if total == 2 or total == 3:
            return True
        # Otherwise dies
        return False
    
def print_grid(grid: set[tuple[int, int]]) -> None:
    """
    Prints the current state of the Game of Life grid.
    Live cells are represented by '■' characters, dead cells by spaces.
    """
    if not grid:
        print("Empty grid")
        return
    
    # Find the boundaries of the grid
    min_x = min(x for x, _ in grid)
    max_x = max(x for x, _ in grid)
    min_y = min(y for _, y in grid)
    max_y = max(y for _, y in grid)
    
    # Add some padding
    min_x -= 2
    max_x += 2
    min_y -= 2
    max_y += 2
    
    # Print the grid
    print("\n" + "-" * (max_x - min_x + 3))  # Border
    for y in range(min_y, max_y + 1):
        print("|", end="")
        for x in range(min_x, max_x + 1):
            if (x, y) in grid:
                print("■", end="")
            else:
                print(" ", end="")
        print("|")
    print("-" * (max_x - min_x + 3))  # Border
    print(f"Live cells: {len(grid)}")
     
def load_patterns() -> dict:
    """Load patterns from JSON file."""
    try:
        with open('patterns.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: patterns.json not found. Using empty pattern.")
        return {"patterns": {}}

def test_build_initial_grid(pattern_id: str) -> tuple[set[tuple[int, int]], dict]:
    """
    Load a pattern from JSON file and return the grid and pattern info.
    Returns tuple of (grid_set, pattern_info).
    """
    patterns_data = load_patterns()
    patterns = patterns_data.get("patterns", {})
    
    if pattern_id in patterns:
        pattern_info = patterns[pattern_id]
        cells = pattern_info["cells"]
        grid = {tuple(cell) for cell in cells}
        return grid, pattern_info
    else:
        # Default empty grid
        grid = set()
        pattern_info = {
            "name": "Empty Grid",
            "description": "Default empty grid with no live cells",
            "cells": []
        }
        return grid, pattern_info

def save_game_log(initial_grid: set[tuple[int, int]], rounds: int, total_time: float, round_times: list[float], pattern_info: dict) -> None:
    """
    Saves game statistics to a JSON file in the logs folder.
    """
    if not round_times:
        return
    
    # Create timestamp for filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"game_log_{timestamp}.json"
    filepath = os.path.join("logs", filename)
    
    # Calculate statistics
    round_times_ms = [t * 1000 for t in round_times]  # Convert to milliseconds
    
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "initial_grid": {
            "pattern_name": pattern_info["name"],
            "pattern_description": pattern_info["description"],
            "live_cells": len(initial_grid),
            "cells": list(initial_grid)
        },
        "game_stats": {
            "total_rounds": rounds,
            "total_time_seconds": round(total_time, 4),
            "total_time_ms": round(total_time * 1000, 2)
        },
        "round_timings": {
            "fastest_round_ms": round(min(round_times_ms), 2),
            "slowest_round_ms": round(max(round_times_ms), 2),
            "median_round_ms": round(median(round_times_ms), 2),
            "average_round_ms": round(sum(round_times_ms) / len(round_times_ms), 2),
            "all_round_times_ms": [round(t, 2) for t in round_times_ms]
        }
    }
    
    # Save to file
    with open(filepath, 'w') as f:
        json.dump(log_data, f, indent=2)
    
    print(f"Game log saved to: {filepath}")
    
def start_game() -> None:
    # The grid is a set of cells, with the key being a tuple of the x and y position of the cell
    # The middle of the grid is at (0, 0)
    grid: set[tuple[int, int]] = set()

    # Start testing grid
    grid, pattern_info = test_build_initial_grid("p3")
    
    # Store initial grid and timing information
    initial_grid = grid.copy()
    round_times = []
    round_count = 0
    game_start_time = time.time()

    # Start the game loop
    while True:
        # If the grid is empty, break the loop
        if len(grid) == 0:
            print("Grid is empty")
            break
        
        round_count += 1

        # Get the start time of the state
        state_start_time = time.time()

        # Create a set to store the cells that have already been checked
        # So we don't check the same cell multiple times
        checked_cells = set()

        # Create a auxiliary grid
        aux_grid = set()

        # Iterate over the alive cells and its 8 neighbors
        for cell in grid:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    # Current cell position being checked
                    current_cell_pos = (cell[0] + i, cell[1] + j)

                    # Check if the current cell position is already checked
                    # If it is, skip it
                    if current_cell_pos in checked_cells:
                        continue
                    else:
                        # Check the current cell
                        new_state = check_cell(
                            x_pos = current_cell_pos[0],
                            y_pos = current_cell_pos[1],
                            cell_state = current_cell_pos in grid, # False if the cell is not in the grid
                            grid = grid,
                        )

                        # If it is alive, add the current cell to the auxiliary grid,
                        if new_state:
                            aux_grid.add(current_cell_pos)

                        # Add the current cell to the checked cells set
                        checked_cells.add(current_cell_pos)

        # Update the grid with the new state
        grid = aux_grid

        # Visualize the grid
        print_grid(grid)

        state_end_time = time.time()
        state_spent_time = state_end_time - state_start_time
        round_times.append(state_spent_time)
        print(f"State spent time: {state_spent_time * 1000:.2f} miliseconds")
    
    # Calculate total game time and save log
    game_end_time = time.time()
    total_game_time = game_end_time - game_start_time
    
    # Save the game log
    save_game_log(initial_grid, round_count, total_game_time, round_times, pattern_info)

def main():
    start_game()
    pass

if __name__ == '__main__':
    main()
