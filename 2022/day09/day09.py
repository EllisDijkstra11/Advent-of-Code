from pathlib import Path
import string
from tokenize import String

def preprocess(input_lines: list[int]):
    commands = input_lines.split("\n")
    split_commands = []
    for command in commands:
        direction, distance = command.split(" ")
        split_commands.append([direction, distance])
    return split_commands


def first(commands):
    head_position = (0, 0)
    tail_position = (0, 0)
    all_tail_positions = [(0, 0)]
    for command in commands:
        direction, distance = command
        for _ in range(int(distance)):
            head_position, tail_position = calculate_move(0, head_position, tail_position, direction)
            all_tail_positions.append(tail_position)
    return len(set(all_tail_positions))
    

def second(commands):
    rope_positions = [(0, 0)] * 10
    all_tail_positions = [(0, 0)]
    for command in commands:
        direction, distance = command
        for _ in range(int(distance)):
            for index in range(len(rope_positions) - 1):
                first_rope_position, second_rope_position = calculate_move(index, rope_positions[index], rope_positions[index + 1], direction)

                rope_positions[index] = first_rope_position
                rope_positions[index + 1] = second_rope_position

                if index == (len(rope_positions) - 2):
                    all_tail_positions.append(second_rope_position)
                    
    return len(set(all_tail_positions))


def calculate_move(index, head_position, tail_position, direction):
    if (index == 0):
        head_position = move_rope(head_position, direction)

    distance_head_tail_x = head_position[0] - tail_position[0]
    distance_head_tail_y = head_position[1] - tail_position[1]
    distance_head_tail = abs(distance_head_tail_x) + abs(distance_head_tail_y)
    
    if distance_head_tail > 2:
        tail_position = head_position
        distance_head_tail_x = -distance_head_tail_x
        distance_head_tail_y = -distance_head_tail_y


    if distance_head_tail_x == -2:
        tail_position = move_rope(tail_position, "L")
    if distance_head_tail_x == 2:
        tail_position = move_rope(tail_position, "R")
    if distance_head_tail_y == -2:
        tail_position = move_rope(tail_position, "U")
    if distance_head_tail_y == 2:
        tail_position = move_rope(tail_position, "D")

    return head_position, tail_position


def move_rope(rope_position, direction):
    if direction == "L":
        x = rope_position[0] - 1
        y = rope_position[1]
    if direction == "R":
        x = rope_position[0] + 1
        y = rope_position[1]
    if direction == "U":
        x = rope_position[0]
        y = rope_position[1] - 1
    if direction == "D":
        x = rope_position[0]
        y = rope_position[1] + 1
    return (x, y)


if __name__ == "__main__":
    data_path_example = Path('2022/day09/example.txt')
    data_path_input = Path('2022/day09/input.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(preprocess(example_data)))
    print(first(preprocess(data)))
    print(second(preprocess(example_data)))
    print(second(preprocess(data)))
    