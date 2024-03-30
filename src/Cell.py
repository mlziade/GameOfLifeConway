class Cell:

    def __init__(self, x_pos: int, y_pos: int, value: int):
        self.x_pos = x_pos
        self.y_pos = y_pos
        if value not in [0,1]:
            raise ValueError('VALUE MUST BE EITHER 0 OR 1')
        self.value = int

    def get_position(self) -> list:
        return [self.x_pos, self.y_pos]
    
    def get_value(self) -> int:
        return self.value