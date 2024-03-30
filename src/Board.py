from cell import Cell

# Creates a matrix of determined size with Cells of value 0 and returns it
def create_empty_matrix(x_size: int, y_size: int):
   matrix = []
   for i in range(x_size):
      aux_array = []
      for j in range(y_size):
         aux_cell = Cell(i,j,0)
         aux_array.append(aux_cell)
      matrix.append(aux_array)
   return matrix

# Creates a matrix from a txt file and returns it
def creates_board_from_file(path_input_file):
   matrix = []
   with open(path_input_file, "r") as file:
      aux_array = []
      for i, line in enumerate(file):
         for j, chars in enumerate(line):
            aux_cell = Cell(i,j,chars)
            aux_array.append(aux_cell)
         matrix.append(aux_array)
   return matrix

# Function to verify whether a populated cell will update to unpopulated or not
# Return True if it will be unpopulated
def verify_populated_cell(matrix, x_pos: int, y_pos: int) -> bool:
   pass

# Function to verify whether a unpopulated cell will update to populated or not
# Return True if it will be populated
def verify_unpopulated_cell(matrix, x_pos: int, y_pos: int) -> bool:
   aux_sum = 0 
   for i in range(-1,1):
      for j in range(-1,1):
         try:
            aux_sum += matrix[x_pos + i][y_pos + j].get_value()
         except IndexError:
            pass
         if aux_sum > 3: return True
   return False

class Board:

   def __init__(self, x_size: int, y_size: int, path_input_file: str = str()):
      if x_size <= 0 or y_size <= 0:
         raise ValueError('BOARD DIMENSION MUST BE A POSITIVE NUMBER')
      self.x_size = x_size
      self.y_size = y_size
      if path_input_file == str():
         self.matrix = create_empty_matrix(x_size, y_size)
         print("Empty board created successfully")
      else:
         self.matrix = creates_board_from_file(path_input_file)
         print("Board created successfully from a input file")


   # Function that draws a board
   def print_board(self) -> None:
      for i in range(self.x_size):
         for j in range(self.y_size):
            print(self.matrix[i][j].get_value(), end=" ")
         print()
   
   def update_board(self):
      for x_pos in range(self.get_x_pos()):
         for y_pos, current_cell in enumerate(self.matrix[x_pos]): 
            if current_cell.is_populated():
               pass
            else:
               pass

   

if __name__ == '__main__':
   board1 = Board(10,10)
   board1.print_board()
   print(verify_unpopulated_cell(board1.matrix, 0, 0))