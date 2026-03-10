from pathlib import Path
import timeit 
import pprint

def preprocess(input_lines: list[int]):
    papers, lines = input_lines.strip().split('\n\n')
    
    marks = papers.split("\n")
    dots = []
    for mark in marks:
        dots.append([int(n) for n in mark.split(",")])

    folds = lines.split("\n")
    instructions = []
    for fold in folds:
        instruction = fold.split(" ")
        print(instruction)
        instructions.append(instruction[-1].split("="))
    return [dots, instructions]

class Paper:
    def __init__(self, input):
        self.dots, self.instructions = input
        self.new_dots = set()

    def fold_paper(self, instruction):
        if instruction[0] == 'x':
            fold = int(instruction[1])
            for dot in self.dots:
                x, y = dot
                if x > fold:
                    x = fold - x + fold
                self.new_dots.add((x, y))
        else:
            fold = int(instruction[1])
            for dot in self.dots:
                x, y = dot
                if y > fold:
                    y = fold - y + fold
                self.new_dots.add((x, y))
    
    def execute_instructions(self, n):
        for index in range(n):
            self.new_dots = set()
            self.fold_paper(self.instructions[index])
            self.dots = list(self.new_dots)
    
    def visualise_paper(self):
        max_x, max_y = 0, 0
        for dot in self.dots:
            x, y = dot
            max_x = max(max_x, x + 1)
            max_y = max(max_y, y + 1)
        
        paper = [["." for _ in range(max_x)] for _ in range(max_y)]

        for dot in self.dots:
            x, y = dot
            paper[y][x] = "#"
        
        for line in paper:
            print(line)
        pprint.pprint(paper)
    
    def get_dots(self):
        return len(self.new_dots)

def first(input):
    paper = Paper(input)
    paper.execute_instructions(1)
    return paper.get_dots()

def second(input):
    paper = Paper(input)
    paper.execute_instructions(len(paper.instructions))
    return paper.visualise_paper()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2021/day13"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input          ():", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input          ():", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")