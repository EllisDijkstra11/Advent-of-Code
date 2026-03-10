import re
import timeit 
from pathlib import Path

def preprocess(input_lines: list[int]):
    return [int(n) for n in re.findall(r'\d{1,10}', input_lines)]

class CPU:
    def __init__(self, input):
        self.reg_A = input[0]
        self.reg_B = input[1]
        self.reg_C = input[2]
        self.codes = input[3:]
        self.results = []
    
    def find_result(self):
        self.results = []

        index = 0
        while index < len(self.codes):
            opcode = self.codes[index]
            operand = literal_operand = self.codes[index + 1]

            match operand:
                case 4:
                    operand = self.reg_A
                case 5:
                    operand = self.reg_B
                case 6:
                    operand = self.reg_C
                case 7:
                    operand = None
                case _:
                    pass
            
            index += 2

            match opcode:
                case 0:
                    self.reg_A = self.reg_A // (2 ** operand)
                case 1:
                    self.reg_B = self.reg_B ^ literal_operand
                case 2:
                    self.reg_B = operand & 7
                case 3:
                    if self.reg_A != 0:
                        index = literal_operand
                case 4:
                    self.reg_B = self.reg_B ^ self.reg_C
                case 5:
                    self.results.append(operand % 8)
                case 6:
                    self.reg_B = self.reg_A // (2 ** operand)
                case 7:
                    self.reg_C = self.reg_A // (2 ** operand)
                case _:
                    print("This should not be happening")
    
    def find_reg_A(self):
        bits = [str(a) + str(b) + str(c) for a in range(0, 2) for b in range(0, 2) for c in range(0, 2)]

        reg_A = ['']
        new_reg_A = []
        index = 1
        while index <= len(self.codes):
            while reg_A:
                a = reg_A.pop(0)

                for bit in bits:
                    self.results = []
                    self.reg_A = int(a + bit, 2)
                    self.find_result()

                    if self.results and self.results == self.codes:
                        return int(a + bit, 2)
                    elif len(self.results) >= index and self.results == self.codes[-index:]:
                        new_reg_A.append(a + bit)

            reg_A = new_reg_A.copy()
            index += 1
        return None

    def string_result(self):
        return ','.join(str(result) for result in self.results)          

def first(input):
    cpu = CPU(input)
    cpu.find_result()
    return cpu.string_result()

def second(input):
    cpu = CPU(input)
    return cpu.find_reg_A()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day17"

    example = Path(path + '/example.txt').read_text()

    input = Path(path + '/input.txt').read_text()

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input    (117440):", second(preprocess(example)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s")