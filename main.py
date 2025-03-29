import time

def check_cell(x_pos: int, y_pos: int, grid: dict[tuple[int, int], int], bounding_rectangle: list[int]):
    # I can guarantee that any point outside and more than 1 block away from the rectangle bounded by bounding_rectangle is 0
    if x_pos - 1 < bounding_rectangle[0] or x_pos + 1 > bounding_rectangle[1] or y_pos - 1 < bounding_rectangle[2] or y_pos + 1 > bounding_rectangle[3]:
        return 0, bounding_rectangle # Out of bounds
    
    # Count neighbors
    total = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # Skip the cell itself
            neighbor_pos = (x_pos + i, y_pos + j)
            if neighbor_pos in grid and grid[neighbor_pos] == 1:
                total += 1
    
    # Check the state of the cell
    current_state = grid.get((x_pos, y_pos), 0)

    if current_state == 0:     
        # Dead cell with exactly 3 neighbors becomes alive
        if total == 3:
            # Check if we need to expand the bounding box
            if (x_pos == bounding_rectangle[0] or x_pos == bounding_rectangle[1] or 
                y_pos == bounding_rectangle[2] or y_pos == bounding_rectangle[3]):
                # expand the bounding box
                return 1, [bounding_rectangle[0] - 1, bounding_rectangle[1] + 1, bounding_rectangle[2] - 1, bounding_rectangle[3] + 1]
            return 1, bounding_rectangle # Cell becomes alive, no need to expand the bounding box
        return 0, bounding_rectangle # Cell remains dead
    
    else:  # current_state == 1
        # Live cell with 2 or 3 neighbors survives
        if total == 2 or total == 3:
            return 1, bounding_rectangle
        # Otherwise die (underpopulation or overpopulation)
        return 0, bounding_rectangle
    
    
def test_build_initial_grid(type: str) -> dict:
    grid = {}
    match type:
        case "infinite":
            grid = {
                (-1, 0): 1, (0, 1): 1, (1, -1): 1,
                (1, 0): 1, (1, 1): 1
            }
        case "loop":
            grid = {
                (0, -1): 1, (0, 0): 1, (0, 1): 1
            }
        case "chaos": 
            grid = {
                (-1, -1): 1, (-1, 0): 1, (-1, 1): 1,
                (0, 0): 1, (1, -1): 1, (1, 1): 1
            }
        case "sepuku":
            grid = {
                (-1, -1): 1, (-1, 0): 1, (-1, 1): 1,
                (0, -1): 1, (0, 0): 1, (0, 1): 1,
                (1, -1): 1, (1, 0): 1, (1, 1): 1
            }
        case "p3":  # Adding the p3 oscillator case
            grid = {
                (-1, 0): 1,
                (0, -1): 1, (0, 1): 1,
                (1, 0): 1
            }
        case _:
            # Default grid is a 3x3 grid with all cells dead
            grid = {(x, y): 0 for x in range(-1, 2) for y in range(-1, 2)}
    
    return grid, [2, 2, 2, 2]

def print_grid(grid: dict[tuple[int, int], int], bounding_rectangle: list[int]):
    for y in range(bounding_rectangle[2], bounding_rectangle[3] + 1):
        for x in range(bounding_rectangle[0], bounding_rectangle[1] + 1):
            print("O" if grid.get((x, y), 0) == 1 else ".", end="")
        print()
    print()
    
def start_game() -> None:
    # The grid is a dictionary with the key being a tuple of the x and y position of the cell and the value being the state of the cell
    grid: dict[tuple[int, int], int] = {}
   
    # The bounding rectangle defines the area where the cells are allowed to be in
    # The center of the grid is at (0, 0) and the bounding rectangle is defined by the following way:
    # [d, c, b, a] where d is the the x position of the leftmost cell, c is the x position of the rightmost cell, b is the y position of the bottommost cell and a is the y position of the topmost cell
    # The bowding box is always 1 block away from the cells
    # So a 3x3 grid would have a bounding rectangle of [1, 1, 1, 1]
    # It is used to optimize the check_cell function by not checking cells that are outside of the bounding rectangle
    # TODO: Could be optimized further by changing the number of points of the polygon that defines the bounding rectangle
    bounding_rectangle: list[int, int, int, int] = [0, 0, 0, 0]

    # Start testing grid
    grid, bounding_rectangle = test_build_initial_grid("chaos")

    # Start the game loop
    while True:
        # Create a copy to read from while writing to the original grid
        aux_grid = grid.copy()
        # Create a set to store the cells that have already been checked
        checked_cells = set()

        # Iterate over the alive cells
        for cell in aux_grid:
            # If the cell has already been checked, skip it
            if cell in checked_cells:
                continue
            else:
                # Check the cell
                new_state, new_bounds = check_cell(cell[0], cell[1], aux_grid, bounding_rectangle)
                # Update the cell state
                if new_state == 1:
                    grid[cell] = 1
                # Add the cell to the checked set
                checked_cells.add(cell)
                # And its neighbors
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        neighbor_pos = (cell[0] + i, cell[1] + j)
                        if neighbor_pos not in checked_cells:
                            new_state, new_bounds = check_cell(neighbor_pos[0], neighbor_pos[1], aux_grid, bounding_rectangle)
                            if new_state == 1:
                                grid[neighbor_pos] = 1
                            checked_cells.add(neighbor_pos)
            
            bounding_rectangle = new_bounds
        print_grid(grid, bounding_rectangle)
        time.sleep(0.5)

def main():
    start_game()
    pass

if __name__ == '__main__':
    main()