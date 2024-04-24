class Board:
    def __init__(self, board):
        self.board = board

    def __str__(self):
        upper_lines = f'\n╔═══{"╤═══"*2}{"╦═══"}{"╤═══"*2}{"╦═══"}{"╤═══"*2}╗\n'
        middle_lines = f'╟───{"┼───"*2}{"╫───"}{"┼───"*2}{"╫───"}{"┼───"*2}╢\n'
        lower_lines = f'╚═══{"╧═══"*2}{"╩═══"}{"╧═══"*2}{"╩═══"}{"╧═══"*2}╝\n'
        board_string = upper_lines
        for index, line in enumerate(self.board):
            row_list = []
            for square_no, part in enumerate([line[:3], line[3:6], line[6:]], start=1):
                row_square = '|'.join(str(item) for item in part)
                row_list.extend(row_square)
                if square_no != 3:
                    row_list.append('║')

            row = f'║ {" ".join(row_list)} ║\n'
            row_empty = row.replace('0', ' ')
            board_string += row_empty

            if index < 8:
                if index % 3 == 2:
                    board_string += f'╠═══{"╪═══"*2}{"╬═══"}{"╪═══"*2}{"╬═══"}{"╪═══"*2}╣\n'
                else:
                    board_string += middle_lines
            else:
                board_string += lower_lines
        return board_string
    
    def find_empty_cell(self): # method that finds the empty cells in the sudoku board, self as a parameter, representing the instance of the class
        for row, contents in enumerate(self.board):
            try:
                col = contents.index(0)
                return row, col
            except ValueError:
                pass
        return None

    def valid_in_row(self, row, num): # checks if the number is not already present in that row
        return num not in self.board[row]

    def valid_in_col(self, col, num): # check whether the value at the current position in the 2D list is not equal to the provided num
        return all(
            self.board[row][col] != num
            for row in range(9)
        )

    def valid_in_square(self, row, col, num): # method that checks if a number can be inserted in the 3x3 square.    
        row_start = (row // 3) * 3 # ensure that the starting row index for each 3x3 block is a multiple of 3 
        col_start = (col // 3) * 3 # ensure that the starting row index for each 3x3 block is a multiple of 3
        for row_no in range(row_start, row_start + 3):
            for col_no in range(col_start, col_start + 3): # iterate over a sequence of three elements
                if self.board[row_no][col_no] == num:
                    return False
        return True

    def is_valid(self, empty, num): # This method checks if a given number is a valid choice for an empty cell in the sudoku board by validating its compatibility with the row, column, and 3x3 square of the specified empty cell.
        row, col = empty
        valid_in_row = self.valid_in_row(row, num) # Check if the number is valid for insertion in the specified row and column, square
        valid_in_col = self.valid_in_col(col, num)
        valid_in_square = self.valid_in_square(row, col, num)
        return all([valid_in_row, valid_in_col, valid_in_square])
    
    def solver(self): # method that attempts to solve the sudoku in-place, meaning it would modify the existing sudoku board rather than creating a new one.
        if (next_empty := self.find_empty_cell()) is None: # (:=) By using the walrus operator, you can combine the assignment and the conditional check into a single line
            return True
        else:
            for guess in range(1, 10):
                if self.is_valid(next_empty, guess):
                    row, col = next_empty # this is called unpack tuple :/

