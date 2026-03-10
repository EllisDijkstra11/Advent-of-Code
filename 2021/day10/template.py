from pathlib import Path
import timeit 

def preprocess(input_lines: list[int]):
    return input_lines.split('\n')

class Syntax:

    def __init__(self, syntax):
        self.syntax = syntax
        self.opening_characters = "([{<"
        self.closing_characters = ")]}>"
        self.wrong_characters = []
        self.unfinished_characters = []
    
    def remove_corrupted_chunks(self):
        for syntax in self.syntax:
            current_syntax = syntax
            current_order = []
            wrong = False

            while current_syntax:
                current_character = current_syntax[:1]
                current_syntax = current_syntax[1:]
                if current_character in self.opening_characters:
                    current_order.append(current_character)
                else:
                    previous_character = current_order.pop()
                    previous_character_index = self.opening_characters.index(previous_character)
                    if not self.closing_characters[previous_character_index] == current_character:
                        self.wrong_characters.append(current_character)
                        wrong = True
            
            if not wrong:
                self.unfinished_characters.append(current_order)
        
    
    def find_wrong_character_values(self):
        sum = 0
        for character in self.wrong_characters:
            if character == ")":
                sum += 3
            elif character == "]":
                sum += 57
            elif character == "}":
                sum += 1197
            elif character == ">":
                sum += 25137
            else: 
                print("You screwed up", character)
        
        return sum
    
    def finish_character_values(self):
        sums = []

        for values in self.unfinished_characters:
            sum = 0
            for character in reversed(values):
                sum *= 5
                if character == "(":
                    sum += 1
                elif character == "[":
                    sum += 2
                elif character == "{":
                    sum += 3
                elif character == "<":
                    sum += 4
                else: 
                    print("You screwed up", character)
            
            sums.append(sum)
        
        sums.sort()
        return sums[int((len(sums) + 0) / 2)]

def first(syntax):
    syntax = Syntax(syntax)
    syntax.remove_corrupted_chunks()
    return syntax.find_wrong_character_values()

def second(syntax):
    syntax = Syntax(syntax)
    syntax.remove_corrupted_chunks()
    return syntax.finish_character_values()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2021/day10"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input     (26397):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input    (288957):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Too low                  : 2138262343")
    print("Part 2 - Too low                  : 2163962486")
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")