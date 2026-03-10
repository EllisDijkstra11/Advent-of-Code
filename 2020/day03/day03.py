from pathlib import Path
import string

def preprocess(input_lines: list[int]):
    all_slopes = []
    horizontal_slopes = input_lines.split('\n')
    for horizontal_slope in horizontal_slopes:
        all_slopes.append(horizontal_slope)
    return all_slopes

def first(slopes):
    return travel_map(slopes, 3, 1)

def second(slopes):
    first_course = travel_map(slopes, 1, 1)
    second_course = travel_map(slopes, 3, 1)
    third_course = travel_map(slopes, 5, 1)
    fourth_course = travel_map(slopes, 7, 1)
    fifth_course = travel_map(slopes, 1, 2)
    return first_course * second_course * third_course * fourth_course * fifth_course

def travel_map(slopes, dx, dy):
    total_trees = 0
    x = 0
    y = 0
    while y in range(0, len(slopes)):
        x = x % len(slopes[y])
        if slopes[y][x] == "#":
            total_trees += 1
        x += dx
        y += dy
    return total_trees

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
    data_path_example = Path('2020/day03/example03.txt')
    data_path_input = Path('2020/day03/input03.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(preprocess(data)))
    print(second(preprocess(data)))
    