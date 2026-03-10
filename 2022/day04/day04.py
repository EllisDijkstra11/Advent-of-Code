from pathlib import Path
import string
from tokenize import String

def preprocess(input_lines: list[int]):
    pairs = input_lines.split('\n')
    return pairs

def make_sets(pairs, first):
    total_containments = 0
    for pair in pairs:
        elf = pair.split(',')
        first_elf = set()
        second_elf = set()
        first_elf_add = True
        for chores in elf:
            chore = [int(n) for n in chores.split('-')]
            if first_elf_add:
                for index in range(chore[0], chore[1] + 1):
                    first_elf.add(index)
                first_elf_add = False
            else:
                for index in range(chore[0], chore[1] + 1):
                    second_elf.add(index)
        if first:
            if count_containments(first_elf, second_elf):
                total_containments += 1
        else:
            if count_overlap(first_elf, second_elf):
                total_containments += 1
    return total_containments

def count_containments(first_elf, second_elf):
    containments = 0
    for chore in first_elf:
        if chore in second_elf:
            containments += 1
    if containments == len(first_elf):
        return True

    containments = 0
    for chore in second_elf:
        if chore in first_elf:
            containments += 1
    if containments == len(second_elf):
        return True
    return False

def count_overlap(first_elf, second_elf):
    containments = 0
    for chore in first_elf:
        if chore in second_elf:
            containments += 1
    if containments > 0:
        return True

    containments = 0
    for chore in second_elf:
        if chore in first_elf:
            containments += 1
    if containments > 0:
        return True

    return False

def second(backpacks):
    total_points = 0
    for index in range(len(backpacks)//3):
        total_points = total_points + compare_badges(backpacks[index * 3], backpacks[index * 3 + 1], backpacks[index * 3 + 2])
    return total_points

if __name__ == "__main__":
    data_path_example = Path('2022/day04/example04.txt')
    data_path_input = Path('2022/day04/input04.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(make_sets(preprocess(data), True))
    print(make_sets(preprocess(data), False))
    