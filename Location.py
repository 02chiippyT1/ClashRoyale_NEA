

class Location:

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return f'({self.row},{self.col})'

