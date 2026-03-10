from pathlib import Path
from pprint import pprint 

def preprocess(input_lines: list[int]):
    fields = input_lines.split("\n\n")     

    lines = []
    for field in fields:
        lines.append(field.splitlines())
    
    return lines

def first(fields):
    total_sum = 0
    for field in fields:
        sum = find_horizontal_mirror(field)
        total_sum += (sum * 100)
        
        sum = find_vertical_mirror(field, False)
        total_sum += sum

    return total_sum


def second(fields):
    total_sum = 0
    for field in fields:
        sum = find_smudged_horizontal_mirror(field)
        total_sum += (sum * 100)
        
        sum = find_vertical_mirror(field, True)
        total_sum += sum

    return total_sum


def find_horizontal_mirror(field):
    index = 1
    difference = 0
    while index < len(field):

        while index - difference >= 0 and index + difference < len(field) and field[index - 1 - difference] == field[index + difference]:
            difference += 1
        
        if index - difference - 1 == -1 or index + difference == len(field):
            return index # although the index starts at 1, the mirrors start at 1 as well, so index is returned without subtracting 1

        index += 1
        difference = 0
    return 0


def find_vertical_mirror(field, smudged):
    new_field = [""] * len(field[0])

    for index in range(len(field[0])):
        for line in range(len(field)):
            new_field[index] += field[line][index]

    if smudged:
        return find_smudged_horizontal_mirror(new_field)
    
    return find_horizontal_mirror(new_field)


def find_smudged_horizontal_mirror(field):
    index = 1
    difference = 0
    found_false = False
    false_row = []

    while index < len(field):
        # all entries are fine as long as there weren't any mismatches yet
        while (index - difference >= 0 and index + difference < len(field)) and (not found_false or field[index - 1 - difference] == field[index + difference]):
            if field[index - 1 - difference] != field[index + difference]:
                # after the first mismatch, no new mismatches may be made
                found_false = True
                false_row = [field[index - difference - 1], field[index + difference], index]

            difference += 1
        
        # if there was exactly one mismatch, check if the rows differ by one
        if found_false and (index - difference - 1 == -1 or index + difference == len(field)):
            found_false = False
            not_possible = False

            for symbol in range(len(false_row[0])):
                # if you already found a mismatch, no new mismathes may be made
                if found_false and false_row[0][symbol] != false_row[1][symbol]:
                    not_possible = True
                    break
                elif false_row[0][symbol] != false_row[1][symbol]:
                    found_false = True
            
            # if there is only one mismatch, this is the correct index
            if not not_possible and found_false:        
                return false_row[2]

        index += 1
        difference = 0
        found_false = False
        false_row = []
    return 0

if __name__ == "__main__":
    path = "2023/day13"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example one input   (405):", first(preprocess(example_data)))
    print("Part 1 - Actual input             :", first(preprocess(data)))

    print("Part 2 - Example one input   (400):", second(preprocess(example_data)))
    print("Part 2 - Actual input             :", second(preprocess(data)))
