from pathlib import Path
from pprint import pprint

dirs = []
all_sums = []

def preprocess(input_lines: list[int]):
    commands = input_lines.split("\n")
    partial_commands = []

    for command in commands:
        partial_command = command.split(" ")
        partial_commands.append(partial_command)

    while ["$", "cd", ".."] in partial_commands:
        partial_commands.remove(["$", "cd", ".."])

    while ["$", "cd", "/"] in partial_commands:
        partial_commands.remove(["$", "cd", "/"])

    while ["$", "ls"] in partial_commands:
        partial_commands.remove(["$", "ls"])

    while partial_commands is not None and len(partial_commands) > 0:
        partial_commands = make_dir(partial_commands)

    length = len(dirs)
    for index in range(0, length):
        mirrored_index = length - index - 1
        calculate_dir(dirs[mirrored_index])

    dir_sum = 0
    for index in range(1, len(dirs[0])):
        dir_sum += int(dirs[0][index][0])
    all_sums.append(dir_sum)
    print(dir_sum, "  \t", dirs[0][0], "     \t", dirs[0])


    all_sums.sort()
    pprint(all_sums)
    print("len sums", len(all_sums))
    return all_sums
    
    
def make_dir(partial_commands):
    for index in range(len(partial_commands)):
        length_commands = len(partial_commands) - index - 1
        if partial_commands[length_commands][1] == "cd":
            dirs.insert(0, partial_commands[length_commands:])
            partial_commands = partial_commands[:length_commands]
            return partial_commands


def calculate_dir(dir):
    # dir_sum = 0
    # for index in range(1, len(dir)):
    #     if dir[index][0] == "dir":
    #         next_dir_sum = find_next_dir(dir[index])
    #         dir[index] = [next_dir_sum, ""]
    # for index in range(1, len(dir)):
    #         dir_sum += int(dir[index][0])
    # return dir_sum
    dir_sum = 0
    for index in range(1, len(dir)):
        if dir[index][0] == "dir":
            next_dir_sum = find_next_dir(dir[index])
            dir[index] = [next_dir_sum, ""]
            dir_sum += next_dir_sum
        else:
            dir_sum += int(dir[index][0])
    return dir_sum


def find_next_dir(dir):
    for index in range(len(dirs) - 1, -1, -1):
        if dirs[index][0][2] == dir[1]:
            dir_sum = calculate_dir([dirs[index]][0])
            print(dir_sum, "  \t", dirs[index][0], "    \t", dirs[index])
            dirs[index][0] = ["", "", "been"]
            all_sums.append(dir_sum)
            return dir_sum


def first(all_sums):
    total_sum = 0
    for sum in all_sums:
        if sum <= 100000:
            total_sum += sum
    return total_sum
   

def second(all_sums):
    return None
    for sum in all_sums:
        if sum > 8000000:
            return sum

if __name__ == "__main__":
    data_path_example = Path('2022/day07/example.txt')
    data_path_input = Path('2022/day07/input.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(preprocess(data)))
    #print(second(preprocess(data)))
    