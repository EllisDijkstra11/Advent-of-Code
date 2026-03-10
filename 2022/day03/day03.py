from pathlib import Path
import string

def preprocess(input_lines: list[int]):
    backpack = input_lines.split('\n')
    return backpack

def first(backpacks):
    total_points = 0
    for backpack in backpacks:
        total_points = total_points + compare_contents(backpack)
    return total_points

def compare_contents(backpack):
    priority = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    first_items = backpack[:len(backpack)//2]
    second_items = backpack[len(backpack)//2:]
    print(first_items, second_items)
    for first_item in first_items:
        for second_item in second_items:
            if first_item == second_item:
                print(first_item, second_item)
                for letter in range(0, len(priority)):
                    if first_item == priority[letter]:
                        print(first_item, letter + 1)
                        return letter + 1


def second(backpacks):
    total_points = 0
    for index in range(len(backpacks)//3):
        total_points = total_points + compare_badges(backpacks[index * 3], backpacks[index * 3 + 1], backpacks[index * 3 + 2])
    return total_points

def compare_badges(first_backpack, second_backpack, third_backpack):
    priority = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    for first_item in first_backpack:
        for second_item in second_backpack:
            if first_item == second_item:
                for third_item in third_backpack:
                    if first_item == third_item:
                        print(first_backpack, second_backpack, third_backpack)
                        print(first_item, second_item, third_item)
                        for letter in range(0, len(priority)):
                            if first_item == priority[letter]:
                                print(first_item, letter + 1)
                                return letter + 1


if __name__ == "__main__":
    data_path_example = Path('2022/day03/example03.txt')
    data_path_input = Path('2022/day03/input03.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(preprocess(data)))
    print(second(preprocess(data)))
    