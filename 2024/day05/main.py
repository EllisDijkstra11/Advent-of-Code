from pathlib import Path
import timeit 

def preprocess(input_lines: list[int]):
    orders, updates = input_lines.split('\n\n')
    orders = [[int(n) for n in order.split('|')] for order in orders.split('\n')]
    updates = [[int(n) for n in update.split(',')] for update in updates.split('\n')]
    return [orders, updates]

class Printer:
    def __init__(self, input):
        self.orders, self.updates = input

    def find_correct_updates(self):
        sum = 0
        for update in self.updates:
            correct = self.is_correct_update(update)

            if correct == True:
                sum += update[int(len(update)/2)]
        
        return sum
    
    def find_incorrect_updates(self):
        sum = 0
        for update in self.updates:
            correct = self.is_correct_update(update)

            if not correct == True:
                for page in update:
                    if correct.count(page) == int(len(update)/2):
                        sum += page
                        break
        return sum
    
    def is_correct_update(self, update):
        second_pages = []

        for order in self.orders:
            if order[0] in update and order[1] in update:
                second_pages.append(order[1])
        
        for index, page in enumerate(update):
            if not second_pages.count(page) == index:
                return second_pages
        
        return True

def first(input):
    printer = Printer(input)
    return printer.find_correct_updates()

def second(input):
    printer = Printer(input)
    return printer.find_incorrect_updates()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day05"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input       (143):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input       (123):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")