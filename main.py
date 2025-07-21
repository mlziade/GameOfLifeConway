import time
import json
import os
import argparse
import asyncio
from datetime import datetime
from statistics import median
from typing import Coroutine, Any

async def check_cell(x_pos: int, y_pos: int, cell_state: bool, grid: set[tuple[int, int]]) -> bool:    
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
    Live cells are represented by '*' characters, dead cells by spaces.
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
                print("*", end="")
            else:
                print(" ", end="")
        print("|")
    print("-" * (max_x - min_x + 3))  # Border
    print(f"Live cells: {len(grid)}")
     
async def load_patterns() -> dict:
    """Load patterns from JSON file."""
    try:
        # Use asyncio.to_thread for file I/O to avoid blocking
        def _read_file():
            with open('patterns.json', 'r') as f:
                return json.load(f)
        return await asyncio.to_thread(_read_file)
    except FileNotFoundError:
        print("Warning: patterns.json not found. Using empty pattern.")
        return {"patterns": {}}

async def load_grid_pattern(pattern_id: str) -> tuple[set[tuple[int, int]], dict]:
    """
    Load a pattern from JSON file and return the grid and pattern info.
    Returns tuple of (grid_set, pattern_info).
    """
    patterns_data = await load_patterns()
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

async def save_game_log(initial_grid: set[tuple[int, int]], rounds: int, total_time: float, round_times: list[float], pattern_info: dict, max_rounds: int = None) -> None:
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
            "max_rounds_limit": max_rounds,
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
    
    # Save to file using async I/O
    def _write_file():
        with open(filepath, 'w') as f:
            json.dump(log_data, f, indent=2)
    await asyncio.to_thread(_write_file)
    
    print(f"Game log saved to: {filepath}")
    
async def start_game(pattern_id: str = "p3", save_logs: bool = False, max_rounds: int = None) -> None:
    # The grid is a set of cells, with the key being a tuple of the x and y position of the cell
    # The middle of the grid is at (0, 0)
    grid: set[tuple[int, int]] = set()

    # Start testing grid
    grid, pattern_info = await load_grid_pattern(pattern_id)
    
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
        
        # Check if we've reached the maximum rounds
        if max_rounds is not None and round_count >= max_rounds:
            print(f"Reached maximum rounds limit: {max_rounds}")
            break
        
        round_count += 1

        # Get the start time of the state
        state_start_time = time.time()

        # Create a set to store the cells that need to be checked
        # So we don't check the same cell multiple times
        cells_to_check = set()

        # Collect all cells that need to be checked (alive cells and their neighbors)
        for cell in grid:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    current_cell_pos = (cell[0] + i, cell[1] + j)
                    cells_to_check.add(current_cell_pos)

        # Create async tasks for parallel cell checking
        async def check_single_cell(cell_pos: tuple[int, int]) -> tuple[tuple[int, int], bool]:
            new_state = await check_cell(
                x_pos=cell_pos[0],
                y_pos=cell_pos[1],
                cell_state=cell_pos in grid,
                grid=grid,
            )
            return cell_pos, new_state

        # Execute all cell checks in parallel
        tasks = [check_single_cell(cell_pos) for cell_pos in cells_to_check]
        results = await asyncio.gather(*tasks)

        # Build the new grid from results
        aux_grid = {cell_pos for cell_pos, new_state in results if new_state}

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
    if save_logs:
        await save_game_log(initial_grid, round_count, total_game_time, round_times, pattern_info, max_rounds)
    else:
        print("Log saving disabled.")

async def main():
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument(
        "--pattern", 
        type=str, 
        default="p3",
        help="Pattern to use (default: p3). Available: p1-p12"
    )
    parser.add_argument(
        "--logs",
        type=str,
        choices=["true", "false"],
        default="false",
        help="Enable or disable saving game logs to files (default: false)"
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=None,
        help="Maximum number of rounds to run (default: unlimited)"
    )
    
    args = parser.parse_args()
    
    # Display selected pattern info
    patterns_data = await load_patterns()
    patterns = patterns_data.get("patterns", {})
    
    if args.pattern in patterns:
        pattern_info = patterns[args.pattern]
        print(f"Starting with pattern: {pattern_info['name']}")
        print()
    else:
        print(f"Warning: Pattern '{args.pattern}' not found. Defaulting to pattern p3.")
        args.pattern = "p3"
    
    await start_game(args.pattern, args.logs == "true", args.rounds)

if __name__ == '__main__':
    asyncio.run(main())
