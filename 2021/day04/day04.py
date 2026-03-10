from pathlib import Path
import timeit
import re
from pprint import pprint

def preprocess(input_lines: list[int]):
    boards = input_lines.split('\n\n')
    called_numbers = boards.pop(0).split(',')
    called_numbers = [int(n) for n in called_numbers]

    split_boards = []
    for board in boards:
        rows = board.split('\n')
        current_board = []

        for row in rows:
            numbers = re.split('  | ', row)

            if numbers[0] == '':
                numbers = numbers[1:]
            
            numbers = [int(n) for n in numbers]
            current_board.append(numbers)

        split_boards.append(current_board)
    return [called_numbers, split_boards]

class Board:
    def __init__(self, board):
        self.board = board
        self.win = False
        self.total = 0

    def getTotal(self):
        return self.total

    def getWin(self):
        return self.win
    
    def drawnNumber(self, drawn_number):
        for row_index, row in enumerate(self.board):
            for number_index, number in enumerate(row):

                if number == drawn_number:
                    self.board[row_index][number_index] = 99

    def checkWin(self):
        if self.checkRows() or self.checkColumns():
            self.win = True
    
    def checkRows(self):
        for row in self.board:
            if self.checkRow(row):
                return True
        
        return False

    def checkRow(self, row):
        for number in row:
            if number != 99:
                return False
        
        return True
    
    def checkColumns(self):
        for column in range(len(self.board[0])):
            if self.checkColumn(column):
                return True

        return False

    def checkColumn(self, column):
        for row in range(len(self.board)):
            if self.board[row][column] != 99:
                return False
        
        return True

    def findTotal(self):
        for row in self.board:
            for number in row:
                if number != 99:
                    self.total += number

def first(input):
    called_numbers, split_boards = input
    boards = []
    for board in split_boards:
        boards.append(Board(board))

    while len(called_numbers) > 0:
        current_number = called_numbers.pop(0)
        for board in boards:
            board.drawnNumber(current_number)
            board.checkWin()
            if board.getWin():
                board.findTotal()
                return board.getTotal() * current_number
            

def second(input):
    called_numbers, split_boards = input
    boards = []
    for board in split_boards:
        boards.append(Board(board))

    while len(called_numbers) > 0:
        current_number = called_numbers.pop(0)
        for board in boards:
            board.drawnNumber(current_number)
            board.checkWin()
    
        if len(boards) == 1 and boards[0].win:
            board.findTotal()
            return board.getTotal() * current_number
        boards = list(filter(lambda x: x.win == False, boards))  

if __name__ == "__main__":
    path = "2021/day04"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input      (4512):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input      (1924):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")