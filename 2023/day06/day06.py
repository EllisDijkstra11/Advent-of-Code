from pathlib import Path
from pprint import pprint 

def preprocess(input_lines: list[int]):
    lines = input_lines.splitlines()

    split_lines = []
    for line in lines:
        text, numbers = line.split(":")
        split_lines.append(numbers)
    
    numbers = []
    for line in split_lines:
        numbers.append(line.split(" "))

    for number in numbers:
        while "" in number:
            number.remove("")         

    return(numbers)

def first(numbers):
    total_sum = 1
    times = numbers[0]
    distances = numbers[1]

    index = 0
    while index < len(times):
        races_won = 0
        time = int(times[index])
        record_distance = int(distances[index])
        button_press_length = 0
        while button_press_length <= time:
            if (time - button_press_length) * button_press_length > record_distance:
                races_won += 1
            
            button_press_length += 1
        total_sum *= races_won

        index += 1
    return total_sum


def second (numbers):
    times = ""
    distances = ""

    for index in range(len(numbers[0])):
        times += numbers[0][index]
        distances += numbers[1][index]
    
    time = int(times)
    distance = int(distances)
    
    minimal_button_press_length = 0
    maximal_button_press_length = 0
    button_press_length = 0
    found = False

    while button_press_length <= time and not found:
        if (time - button_press_length) * button_press_length > distance:
            minimal_button_press_length = button_press_length
            found = True

        button_press_length += 1
    
    button_press_length = time
    found = False

    while button_press_length >= 0 and not found:
        if (time - button_press_length) * button_press_length > distance:
            maximal_button_press_length = button_press_length
            found = True
                    
        button_press_length -= 1

    return maximal_button_press_length - minimal_button_press_length + 1


if __name__ == "__main__":
    path = "2023/day06"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print("Part 1 - Example input : ", first(preprocess(example_data)))
    print("Part 1 - Actual input  : ", first(preprocess(data)))
    print("Part 2 - Example input : ", second(preprocess(example_data)))
    print("Part 2 - Actual input  : ", second(preprocess(data)))
    