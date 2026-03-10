from pathlib import Path

def preprocess(input_lines: list[int]):
    moves = input_lines.split('\n')
    return moves

def first(moves):
    total_points = 0
    for move in moves:
        current = move.split(" ")
        if current[1] == "X":
            total_points += 1
            if current[0] == "A":
                total_points += 3
            elif current[0] == "C":
                total_points += 6
        elif current[1] == "Y":
            total_points += 2
            if current[0] == "B":
                total_points += 3
            elif current[0] == "A":
                total_points += 6
        else:
            total_points += 3
            if current[0] == "C":
                total_points += 3
            elif current[0] == "B":
                total_points += 6

    return total_points

def second(moves):
    total_points = 0
    for move in moves:
        current = move.split(" ")
        if current[0] == "A":
            if current[1] == "X":
                total_points += 3
            elif current[1] == "Y":
                total_points += 4
            else:
                total_points += 8
            print(total_points)
        elif current[0] == "B":
            if current[1] == "X":
                total_points += 1
            elif current[1] == "Y":
                total_points += 5
            else:
                total_points += 9
        else:
            if current[1] == "X":
                total_points += 2
            elif current[1] == "Y":
                total_points += 6
            else:
                total_points += 7

    return total_points


if __name__ == "__main__":
    data_path =  Path('day02/example02.txt')
    example_data = data_path.read_text()
    data = data_path.read_text()
    print(first(preprocess(data)))
    print(second(preprocess(data)))

    