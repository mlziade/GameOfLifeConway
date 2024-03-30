from cell import Cell
import copy
import os
from random import randint
import time

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
      for i, line in enumerate(file):
         aux_array = []
         for j, chars in enumerate(line):
            if chars in ["0","1"]:
               aux_cell = Cell(i,j,int(chars))
               aux_array.append(aux_cell)
         matrix.append(aux_array)
   return matrix

# Creates a matrix of determined size with Cells of random value of 0 or 1 'and returns it
def create_random_matrix(x_size: int, y_size: int):
   matrix = []
   for i in range(x_size):
      aux_array = []
      for j in range(y_size):
         aux_cell = Cell(i,j,randint(0,1))
         aux_array.append(aux_cell)
      matrix.append(aux_array)
   return matrix

def create_center_square_matrix(x_size: int, y_size: int):
   matrix = create_empty_matrix(x_size, y_size)
   matrix[x_size][y_size].switch_value()

# Function to verify whether a populated cell will update to unpopulated or not
# Return True if it will be unpopulated
def verify_populated_cell(matrix, x_pos: int, y_pos: int) -> bool:
   aux_sum = 0 
   for i in range(-1,1):
      for j in range(-1,1):
         try:
            aux_sum += matrix[x_pos + i][y_pos + j].get_value()
         except IndexError:
            pass
         if aux_sum > 3: return False
   if 2 <= aux_sum <= 3:
      return True
   return False

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

   def __init__(self, x_size: int, y_size: int, random: bool, path_input_file: str):
      if x_size <= 0 or y_size <= 0:
         raise ValueError('BOARD DIMENSION MUST BE A POSITIVE NUMBER')
      self.x_size = x_size
      self.y_size = y_size
      if random == True:
         self.matrix = create_random_matrix(x_size, y_size)
         print("Random board created successfully")
      elif path_input_file == "":
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
      print()
   
   def update_board(self):
      aux_board = copy.deepcopy(self)
      for x_pos in range(self.x_size):
         for y_pos, current_cell in enumerate(self.matrix[x_pos]): 
            if aux_board.matrix[x_pos][y_pos].is_populated():
               if verify_populated_cell(aux_board.matrix, x_pos, y_pos): current_cell.switch_value()
            else:
               if verify_unpopulated_cell(aux_board.matrix, x_pos, y_pos): current_cell.switch_value()
   
   def life(self, cycles: int):
      for _ in range(cycles):
         os.system(command)
         self.update_board()
         self.print_board()
         time.sleep(1)

if __name__ == '__main__':
   command = 'cls' #for windows
   board1 = Board(40,40, True, "")
   board1.print_board()
   board1.life(1000)