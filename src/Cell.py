class Cell:

    def __init__(self, x_pos: int, y_pos: int, value: int):
        self.x_pos = x_pos
        self.y_pos = y_pos
        if value not in [0,1]:
            raise ValueError('CELL VALUE MUST BE EITHER 0 OR 1')
        self.value = value

    def get_position(self) -> tuple:
        return (self.x_pos, self.y_pos)

    def get_x_pos(self) -> int:
        return self.x_pos

    def get_x_pos(self) -> int:
        return self.x_pos
    
    def get_value(self) -> int:
        return self.value
    
    def is_populated(self) -> bool:
        return True if self.value == 1 else False
    
    def switch_value(self) -> None:
        if self.value == 1: value = 0
        elif self.value == 0: value = 1
