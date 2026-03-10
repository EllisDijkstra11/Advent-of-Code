from pathlib import Path
from pprint import pprint 


def preprocess(input_lines: list[int]):
    pairs = input_lines.split("\n\n")
    return pairs


def first(pairs):
    right_ordered = 0
    index = 1
    for pair in pairs:
        first, second = pair.split("\n")
        biggest = check_list(eval(first), eval(second))

        if biggest == eval(second):
            right_ordered += index

        index += 1

    return right_ordered


def second(pairs):
    index_two = 1
    index_six = 2
    two = [[2]]
    six = [[6]]

    for pair in pairs:
        first, second = pair.split("\n")
        biggest = check_pairs(first)
        if biggest == two:
            index_two += 1
            index_six += 1
        elif biggest == six:
            index_six += 1

        biggest = check_pairs(second)
        if biggest == two:
            index_two += 1
            index_six += 1
        elif biggest == six:
            index_six += 1
    
    return index_two * index_six



def check_pairs(other):
    two = [[2]]
    six = [[6]]

    biggest = check_list(eval(other), two)
    if biggest == two:
        return two
    else:
        biggest = check_list(eval(other), six)
        if biggest == six:
            return six



def check_list(first, second):
    index = 0
    biggest = None
    if type(first) == list:
        len_first = len(first)
    else:
        len_first = 1
    
    if type(second) == list:
        len_second = len(second)
    else:
        len_second = 1


    while biggest == None:
        if index == len_first and index == len_second:
            return None
        elif index == len_first:
            return second
        elif index == len_second:
            return first

        if type(first[index]) == int and type(second[index]) == int:
            biggest = check_int(first[index], second[index])
        elif type(first[index]) == list and type(second[index]) == list:
            biggest = check_list(first[index], second[index])
        elif type(first[index]) == list:
            biggest = check_list(first[index], [second[index]])
        else:
            biggest = check_list([first[index]], second[index])
        
        if biggest == first[index]:
            return first
        elif biggest == second[index]:
            return second
        elif biggest == [first[index]]:
            return first
        elif biggest == [second[index]]:
            return second
    
        index += 1


def check_int(first, second):
    if first > second:
        return first
    elif first < second:
        return second
    else:
        return None


if __name__ == "__main__":
    path = "2022/day13"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(preprocess(example_data)))
    print(first(preprocess(data)))
    print(second(preprocess(example_data)))
    print(second(preprocess(data)))
    