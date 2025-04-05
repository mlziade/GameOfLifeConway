import time

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
     
def test_build_initial_grid(type: str) -> set[tuple[int, int]]:
    match type:
        case "p1":
            # Glider pattern
            grid = {
                (0, 0), (1, 1), (2, 2), (2, 1), (1, 2)
            }
        case "p2":
            # Blinker pattern
            grid = {
                (0, 0), (1, 0), (2, 0)
            }
        case "p3":
            # Toad pattern
            grid = {
                (0, 0), (1, 0), (2, 0), (3, 1), (4, 1), (5, 1)
            }
        case _:
            # Default grid is a 3x3 grid with all cells dead
            grid = set()
    
    return grid
    
def start_game() -> None:
    # The grid is a set of cells, with the key being a tuple of the x and y position of the cell
    # The middle of the grid is at (0, 0)
    grid: set[tuple[int, int]] = set()

    # Start testing grid
    grid = test_build_initial_grid("p3")

    # Start the game loop
    while True:
        # If the grid is empty, break the loop
        if len(grid) == 0:
            print("Grid is empty")
            break

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
        print(f"State spent time: {state_spent_time * 1000:.2f} miliseconds")

def main():
    start_game()
    pass

if __name__ == '__main__':
    main()
