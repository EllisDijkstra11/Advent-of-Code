from pathlib import Path
import timeit
from operator import mul
from functools import reduce

def preprocess(input_lines):
    return input_lines.split('\n')[0]

class Packet:
    def __init__(self, input):
        self.packets = input
        self.version = self.hex_encoding[self.find_decimal(self.packets[:3])]
        self.type_ID = self.hex_encoding[self.find_decimal(self.packets[3:6])]
        self.length_ID = self.packets[6]
        self.packets = self.packets[7:]


class Hexadecimal:
    def __init__(self, input):
        self.hex_encoding = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
        self.binary_encoding = ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111", "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"]
        self.version_sum = 0

        self.packets = ""
        for character in input:
            self.packets += self.binary_encoding[self.hex_encoding.index(character)]

    def unpack_packets(self, packets, index):
        # print("packets", packets[index:])
        version = self.hex_encoding[self.find_decimal(packets[index:index + 3])]
        self.version_sum += int(version)
        type_ID = self.hex_encoding[self.find_decimal(packets[index + 3:index + 6])]
        index += 6
        # print(version, type_ID, packets[index:])

        if type_ID == "4":
            # print("literal number")
            return self.is_literal_value(packets, index)
        
        length_ID = packets[index]
        index += 1
        # print(length_ID, packets[index:], index)

        if length_ID == "0":
            sub_packets = []
            sub_packets_length = self.find_decimal(packets[index:index + 15])
            # print(sub_packets_length)

            index += 15
            sub_packets_length += index
            # print(index, sub_packets_length, packets[index:])
            while index < sub_packets_length and index < len(packets) - 11:
                value, index = self.unpack_packets(packets, index)
                sub_packets.append(value)
                # print(value, index)

            value = self.find_value(type_ID, sub_packets)
            return [value, index]
        
        else:
            sub_packets = []
            count = 0
            number_of_sub_packets = self.find_decimal(packets[index:index + 11])

            index += 11
            while count < number_of_sub_packets:
                value, index = self.unpack_packets(packets, index)
                sub_packets.append(value)
                count += 1

            value = self.find_value(type_ID, sub_packets)
            return [value, index]

    def find_decimal(self, binary):
        decimal = 0

        for index in range(len(binary)):
            if binary[index] == "1":
                decimal += 2 ** (len(binary) - index - 1)
        
        return decimal

    def is_literal_value(self, packets, index):
        current_number = ""
        while index < len(packets):
            # print(packets[index:])
            if packets[index] == "1":
                current_number += packets[index + 1:index + 5]
            else:
                current_number += packets[index + 1:index + 5]
                return [self.find_decimal(current_number), index + 5]
            
            index += 5
    
    def find_value(self, type_ID, sub_packets):
        if len(sub_packets) == 1:
            return sub_packets[0]
        
        match type_ID:
            case "0":
                return sum(sub_packets)
            case "1":
                return reduce(mul, sub_packets)
            case "2":
                return min(sub_packets)
            case "3":
                return max(sub_packets)
            case "5":
                return 1 if sub_packets[0] > sub_packets[1] else 0
            case "6":
                return 1 if sub_packets[0] < sub_packets[1] else 0
            case "7":
                return 1 if sub_packets[0] == sub_packets[1] else 0


def first(input):
    hexadecimal = Hexadecimal(input)
    hexadecimal.unpack_packets(hexadecimal.packets, 0)
    return hexadecimal.version_sum

def second(input):
    hexadecimal = Hexadecimal(input)
    return hexadecimal.unpack_packets(hexadecimal.packets, 0)[0]


if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2021/day16"

    data_path_example_one = Path(path + '/example_one.txt')
    data_path_example_two = Path(path + '/example_two.txt')
    data_path_example_three = Path(path + '/example_three.txt')
    data_path_example_four = Path(path + '/example_four.txt')

    data_path_input = Path(path + '/input.txt')

    example_data_one = data_path_example_one.read_text()
    example_data_two = data_path_example_two.read_text()
    example_data_three = data_path_example_three.read_text()
    example_data_four = data_path_example_four.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input        (16):", first(preprocess(example_data_one)))
    print("Part 1 - Example input        (12):", first(preprocess(example_data_two)))
    print("Part 1 - Example input        (23):", first(preprocess(example_data_three)))
    print("Part 1 - Example input        (31):", first(preprocess(example_data_four)))


    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    # print("Part 2 - Example input        (36):", second(preprocess(example_data_one)))
    # print("Part 2 - Example input       (103):", second(preprocess(example_data_two)))
    # print("Part 2 - Example input      (3509):", second(preprocess(example_data_three)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")