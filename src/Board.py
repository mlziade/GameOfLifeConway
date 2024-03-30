from Cell import Cell

def create_matrix(x_size: int, y_size: int):
   matrix = []
   for i in range(x_size):
      aux_array = []
      for j in range(y_size):
         aux_cell = Cell(i,j,0)
         aux_array.append(aux_cell)
      matrix.append(aux_array)
   return matrix

class Board:

   def __init__(self, x_size: int, y_size: int):
      if x_size <= 0 or y_size <= 0:
         raise ValueError('X AND Y MUST BE A POSITIVE NUMBER')
      self.x_size = x_size
      self.y_size = y_size
      self.matrix = create_matrix(x_size, y_size)

   def update_board():
      pass

   def print_board(self)  -> None:
      for i in range(self.x_size):
         for j in range(self.y_size):
            print(self.matrix[i][j].value, end=" ")
         print()
   
   
board1 = Board(10,10)
board1.print_board()