import re
import timeit 
import functools
from pathlib import Path
from itertools import permutations
from collections import defaultdict

def preprocess(input_lines):
    return [n for line in input_lines.split('\n') for n in re.findall(r'\d+A', line)]

class Keypad:
    def __init__ (self, input):
        self.codes = input
        self.numeric_keypad = {
              '0': (1, 3),
              '1': (0, 2),
              '2': (1, 2),
              '3': (2, 2),
              '4': (0, 1),
              '5': (1, 1),
              '6': (2, 1),
              '7': (0, 0),
              '8': (1, 0),
              '9': (2, 0),
              'A': (2, 3),
        }
        self.directional_keypad = {
              '^': (1, 0),
              '<': (0, 1),
              'v': (1, 1),
              '>': (2, 1),
              'A': (2, 0),
        }

    def execute_codes(self, repeats):
        total = 0

        for code in self.codes:
            length = self.find_all_presses(code, 0, repeats)
            total += int(code[:3]) * length
        
        return total

    @functools.cache
    def find_all_presses(self, presses, repeats, max_repeats):
        if repeats > max_repeats:
            return len(presses)
        
        keypad = self.numeric_keypad if repeats < 1 else self.directional_keypad
        return sum(self.find_all_presses(self.find_presses(start, target, keypad), repeats + 1, max_repeats) for start, target in zip('A' + presses, presses))

    def find_presses(self, start, target, keypad):
        x, y = keypad[start]
        tx, ty = keypad[target]

        def press(x, y, presses):
            if (x, y) == (tx, ty): yield presses + 'A'
            if x > tx and (x - 1, y) in keypad.values(): yield from press(x - 1, y, presses + '<')
            if y > ty and (x, y - 1) in keypad.values(): yield from press(x, y - 1, presses + '^')
            if y < ty and (x, y + 1) in keypad.values(): yield from press(x, y + 1, presses + 'v')
            if x < tx and (x + 1, y) in keypad.values(): yield from press(x + 1, y, presses + '>')

        return min(press(x, y, ''), key = lambda p: sum( a != b for a, b in zip(p, p[1:])))

def first(input):
    keypad = Keypad(input)
    return keypad.execute_codes(2)

def second(input):
    keypad = Keypad(input)
    return keypad.execute_codes(25)

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day21"

    example = Path(path + '/example.txt').read_text()

    input = Path(path + '/input.txt').read_text()

    print("Part 1 - Example input    (126384):", first(preprocess(example)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s")