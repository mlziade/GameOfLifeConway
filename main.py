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
        if len(grid) == 0:
            print("Empty grid")
            break

        # Get the start time of the state
        state_start_time = time.time()

        # Create a set to store the cells that have already been checked
        # So we don't check the same cell multiple times
        checked_cells = set()

        # Create a auxiliary grid so i can create the next grid state from the last one
        aux_grid = set()

        # Iterate over the alive cells
        for cell in grid:
            # If the cell has already been checked, skip it
            if cell in checked_cells:
                continue
            else:
                # Check the cell
                new_state = check_cell(
                    x_pos = cell[0], 
                    y_pos = cell[1],
                    cell_state = True,
                    grid = grid,
                )

                # Add the cell to the auxiliary grid if it is alive
                if new_state:
                    aux_grid.add(cell)

                # Check the neighbors of the cell if they are not already checked
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        neighbor_pos = (cell[0] + i, cell[1] + j)
                        if neighbor_pos in checked_cells:
                            continue
                        else:
                            # Check the neighbor cell
                            new_state = check_cell(
                                x_pos = neighbor_pos[0],
                                y_pos = neighbor_pos[1],
                                cell_state = neighbor_pos in grid, # False if the cell is not in the grid
                                grid = grid,
                            )

                            # Add the neighbor cell to the auxiliary grid if it is alive
                            if new_state:
                                aux_grid.add(neighbor_pos)

                            # Add the neighbor cell to the checked cells set
                            checked_cells.add(neighbor_pos)

                # Add the cell to the checked cells set
                checked_cells.add(cell)

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
