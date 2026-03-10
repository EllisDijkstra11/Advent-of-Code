from pathlib import Path
from pprint import pprint 
import timeit
import functools
string_sum = 0

def preprocess(input_lines: list[int]):
    lines = input_lines.splitlines()     
    springs = []

    for line in lines:
        springs.append(line.split(" "))
    return springs


def first(lines):
    total_sum = 0
    for line in lines:
        unknown_springs, known_springs_string = line

        known_springs = known_springs_to_list(known_springs_string)

        global string_sum
        string_sum = 0

        unknown_springs = list(unknown_springs)
        fill_strings(unknown_springs, known_springs)
        total_sum += string_sum

    return total_sum


def second(lines):
    total_sum = 0
    for line in lines:
        unknown_springs_folded, known_springs_string = line

        known_springs = tuple(known_springs_to_list(known_springs_string) * 5)

        unknown_springs = ""
        for index in range(5):
            unknown_springs += unknown_springs_folded
            if index < 4:
                unknown_springs += "?"
        
        total_sum += find_amount_of_configurations(unknown_springs, known_springs)

    return total_sum


def known_springs_to_list(known_springs_string):
        known_springs = []
        current_number = 0

        for spring in known_springs_string:
            if spring.isnumeric():
                current_number = current_number * 10 + int(spring)
            elif current_number != 0:
                known_springs.append(current_number)
                current_number = 0
        
        if current_number > 0:
            known_springs.append(current_number)
        
        return known_springs


def fill_strings(unknown_springs, known_springs):
    index = 0
    if "?" in unknown_springs:
        index += 1
        index_unknown_spring = unknown_springs.index("?")

        if index_unknown_spring != -1:
            unknown_springs_dot = unknown_springs.copy()
            unknown_springs_dot[index_unknown_spring] = "."
            boolean = check_possibility_string(unknown_springs_dot, known_springs)
            if (boolean):
                fill_strings(unknown_springs_dot, known_springs)
                # print(".", index, index_unknown_spring, possibilities)


            unknown_springs_hashtag = unknown_springs.copy()
            unknown_springs_hashtag[index_unknown_spring] = "#"

            boolean = check_possibility_string(unknown_springs_hashtag, known_springs)
            if (boolean):
                fill_strings(unknown_springs_hashtag, known_springs)
                # print("#", index, index_unknown_spring, possibilities)


def check_possibility_string(unknown_springs, known_springs):
    current_spring_length = 0
    all_spring_lengths = []
    found_question_mark = False

    # print(unknown_springs, known_springs)

    for spring in unknown_springs:
        if not found_question_mark:
            #print("spring", spring, all_spring_lengths)
            if spring == "?":
                found_question_mark = True
            elif spring == "#":
                current_spring_length += 1

            elif spring == "." and current_spring_length > 0:
                all_spring_lengths.append(current_spring_length)
                current_spring_length = 0
        
    if current_spring_length != 0 and not found_question_mark:
        all_spring_lengths.append(current_spring_length)

    # print(all_spring_lengths)
    for index in range(len(all_spring_lengths)):
        if index >= len(known_springs):
            return False
        elif all_spring_lengths[index] != known_springs[index]:
            return False
    
    if len(all_spring_lengths) == len(known_springs) and not "?" in unknown_springs:
        global string_sum
        string_sum += 1
        # print("string_sum", string_sum)

    return True      


@functools.cache
def find_amount_of_configurations(unknown_springs, known_springs):
    if not known_springs:
        if not "#" in unknown_springs:
            return 1
        
        return 0
    
    elif not unknown_springs:
        return 0

    next_unknown_spring = unknown_springs[0]
    next_known_spring = known_springs[0]

    def hashtag():
        this_spring = unknown_springs[:next_known_spring]
        this_spring = this_spring.replace("?", "#")

        if this_spring != next_known_spring * "#":
            return 0
        
        if len(unknown_springs) == next_known_spring:
            if len(known_springs) == 1:
                return 1
            
            return 0
        
        if unknown_springs[next_known_spring] in ".?":
            return find_amount_of_configurations(unknown_springs[next_known_spring + 1:], known_springs[1:])
        
        return 0
    
    def dot():
        return find_amount_of_configurations(unknown_springs[1:], known_springs)

    if next_unknown_spring == "#":
        sum = hashtag()

    elif next_unknown_spring == ".":
        sum = dot()
    
    elif next_unknown_spring == "?":
        sum = hashtag() + dot()

    return sum


if __name__ == "__main__":
    path = "2023/day12"

    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()
    data = data_path_input.read_text()

    print("Part 1 - Example input : ", first(preprocess(example_data)))
    start = timeit.default_timer()
    print("Part 1 - Actual input  : ", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s, \n")

    print("Part 2 - Example input : ", second(preprocess(example_data)))
    start = timeit.default_timer()
    print("Part 2 - Actual input  : ", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")
    