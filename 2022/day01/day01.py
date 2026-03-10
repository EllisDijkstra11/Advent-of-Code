from pathlib import Path

def add_calories(input_lines: list[int]):
    elves = input_lines.split('\n\n')
    calories_list = []
    for elf in elves:
        calories = [int(n) for n in elf.split('\n')]
        calories_sum = sum(calories)
        calories_list.append(calories_sum)
    return calories_list

def first(calories_per_elf: list[int]) -> int:
    return max(calories_per_elf)

def second(calories_per_elf: list[int]) -> int:
    calories_list = []
    for _ in range(3):
        highest_calories = max(calories_per_elf)
        calories_list.append(highest_calories)
        calories_per_elf.remove(highest_calories)
    return sum(calories_list)


if __name__ == "__main__":
    data_path_example = Path('2022/day01/example01.txt')
    data_path_input = Path('2022/day01/input01.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(add_calories(data)))
    print(second(add_calories(data)))

    