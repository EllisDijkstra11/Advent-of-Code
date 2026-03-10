from pathlib import Path
from pprint import pprint 


def preprocess(input_lines: list[int]):
    lines = input_lines.splitlines()

    numbers = []
    for line in lines:
        numbers.append(line.split(" "))

    ints = []
    for line in numbers:
        line_ints = []
        for number in line:
            line_ints.append(int(number))
        ints.append(line_ints)
    return ints


def extrapolate_data(numbers):
    all_extrapolated_data = []

    for line in numbers:
        line_index = 0
        all_zeroes = False
        extrapolated_data = [line]

        while not all_zeroes:
            number_index = 1
            differences = []

            while number_index < len(extrapolated_data[line_index]):
                first_number = extrapolated_data[line_index][number_index - 1]
                second_number = extrapolated_data[line_index][number_index]
                difference = second_number - first_number
                differences.append(difference)

                number_index += 1
            
            all_zeroes = True
            for difference in differences:
                if difference != 0:
                    all_zeroes = False
                    break
            
            line_index += 1
            extrapolated_data.append(differences)

        all_extrapolated_data.append(extrapolated_data)

    return all_extrapolated_data
    

def first(extrapolated_data):    
    total_sum = 0

    for data in extrapolated_data:
        differences = [0]
        line_index = len(data) - 2
        while line_index >= 0:
            first_number = data[line_index][-1]
            difference = differences[-1]
            second_number = first_number + difference

            differences.append(second_number)
            line_index -= 1
        
        total_sum += differences[-1]
        
    return total_sum
            

def second(extrapolated_data):
    total_sum = 0

    for data in extrapolated_data:
        differences = [0]
        line_index = len(data) - 2
        while line_index >= 0:
            second_number = data[line_index][0]
            difference = differences[-1]
            first_number = second_number - difference

            differences.append(first_number)
            line_index -= 1
        
        total_sum += differences[-1]
        
    return total_sum


if __name__ == "__main__":
    path = "2023/day09"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print("Part 1 - Example input : ", first(extrapolate_data(preprocess(example_data))))
    print("Part 1 - Actual input  : ", first(extrapolate_data(preprocess(data))))
    print("Part 2 - Example input : ", second(extrapolate_data(preprocess(example_data))))
    print("Part 2 - Actual input  : ", second(extrapolate_data(preprocess(data))))
    