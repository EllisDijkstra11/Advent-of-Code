from pathlib import Path
from pprint import pprint 
import timeit

def preprocess(input_lines: list[int]):
    lines = input_lines.split(",")

    return lines

def first(lines):
    total_sum = 0
    for input in lines:
        current_sum = 0
        for character in input:
            current_sum = ((current_sum + ord(character)) * 17) % 256
        total_sum += current_sum
    return total_sum


def second(lines):
    total_sum = 0
    all_boxes = {}
    for index in range(256):
        all_boxes[index] = []
    for input in lines:
        current_box = 0
        for character in input:
            if character in "-=":
                break

            current_box = ((current_box + ord(character)) * 17) % 256
            
        if "=" in input:
            lens = input.split("=")
            found = False
            if len(all_boxes[current_box]) > 0:
                for lenses in all_boxes[current_box]:
                    if lens[0] in lenses:
                        lenses[1] = lens[1]
                        found = True
                        break
            if not found:
                all_boxes[current_box] = all_boxes[current_box] + [lens]
        elif "-" in input:
            for lenses in all_boxes[current_box]:
                if input[:-1] in lenses:
                    all_boxes[current_box].remove(lenses)
                    break

    for box in range(len(all_boxes)):
        if len(all_boxes[box]) > 0:
            for lens in range(len(all_boxes[box])):
                total_sum += (box + 1) * (lens + 1) * int(all_boxes[box][lens][1])

    return total_sum


if __name__ == "__main__":
    path = "2023/day15"

    data_path_example_one = Path(path + '/example_one.txt')
    data_path_example_two = Path(path + '/example_two.txt')

    data_path_input = Path(path + '/input.txt')

    example_data_one = data_path_example_one.read_text()
    example_data_two = data_path_example_two.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example one input   ():", first(preprocess(example_data_one)))
    print("Part 1 - Example two input   ():", first(preprocess(example_data_two)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example two input   ():", second(preprocess(example_data_two)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")
    