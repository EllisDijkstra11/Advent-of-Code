from pathlib import Path
from tokenize import String
import re
import string

def preprocess(input_lines: list[int]):
    seats = input_lines.split('\n')
    seat_IDs = []
    for seat in seats:
        row = 0
        column = 0
        for index in range(7):
            current_rows = 128 // (2 ** (index + 1))
            if seat[index] == "B":
                row += current_rows
            #print(index, current_rows, row)
        for index in range(7, 10):
            current_columns = 8 // (2 ** (index - 6))
            if seat[index] == "R":
                column += current_columns
        seat_ID = (row) * 8 + column
        seat_IDs.append(seat_ID)
    return seat_IDs

def first(seat_IDs):
    return max(seat_IDs)


def second(seat_IDs):
    sum_seats = 0
    range_seats = max(seat_IDs) - min(seat_IDs)
    total_seats = (min(seat_IDs) + max(seat_IDs)) * (range_seats//2) + (min(seat_IDs) + range_seats // 2)
    for seat_ID in seat_IDs:
        total_seats -= seat_ID
        sum_seats += seat_ID
    return total_seats

if __name__ == "__main__":
    data_path_example = Path('2020/day05/example05.txt')
    data_path_input = Path('2020/day05/input05.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(preprocess(data)))
    print(second(preprocess(data)))
    