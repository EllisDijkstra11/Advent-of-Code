from pathlib import Path
import timeit 

def preprocess(input_lines: list[int]):
    displays = input_lines.split("\n")
    split_displays = []

    for display in displays:
        signal, output = display.split("| ")
        split_displays.append([signal.split(" "), output.split(" ")])
    
    return split_displays

class Displays:
    def __init__(self, displays):
        self.displays = displays
        pass

    def countOutput(self):
        count = 0
        values = [2, 3, 4, 7]

        for display in self.displays:
            for digit in display[1]:
                if len(digit) in values:
                    count += 1

        return count
    
    def decodeDigits(self):
        sum = 0
        for digits in self.displays:
            signal_digits, output_digits = digits
            found_digits = [0] * 10
            counter = 0

            while 0 in found_digits or counter > 20:
                counter += 1
                next_signal_digits = signal_digits.copy()
                for signal_digit in signal_digits:
                    # 1
                    if len(signal_digit) == 2:
                        found_digits[1] = signal_digit
                        next_signal_digits.remove(signal_digit)
                    # 4
                    elif len(signal_digit) == 4:
                        found_digits[4] = signal_digit
                        next_signal_digits.remove(signal_digit)
                    # 7
                    elif len(signal_digit) == 3:
                        found_digits[7] = signal_digit
                        next_signal_digits.remove(signal_digit)
                    # 8
                    elif len(signal_digit) == 7:
                        found_digits[8] = signal_digit
                        next_signal_digits.remove(signal_digit)
                    
                    if found_digits.count(0) < 7:
                        match_one = self.matchDigits(found_digits[1], signal_digit) == 2
                        match_four = self.matchDigits(found_digits[4], signal_digit)

                        # 0, 6, 9
                        if len(signal_digit) == 6:
                            # 9
                            if match_four == 4:
                                found_digits[9] = signal_digit
                                next_signal_digits.remove(signal_digit)

                            elif found_digits[5] != 0:
                                match_five = self.matchDigits(found_digits[5], signal_digit) == 5
                                
                                # 6
                                if match_five:
                                    found_digits[6] = signal_digit
                                    next_signal_digits.remove(signal_digit)
                                # 0
                                else:
                                    found_digits[0] = signal_digit
                                    next_signal_digits.remove(signal_digit)
                            
                        # 2, 3, 5
                        elif len(signal_digit) == 5:
                            # 3
                            if match_one:
                                found_digits[3] = signal_digit
                                next_signal_digits.remove(signal_digit)
                            
                            # 2
                            elif match_four == 2:
                                found_digits[2] = signal_digit
                                next_signal_digits.remove(signal_digit)

                            # 5
                            elif match_four == 3:
                                found_digits[5] = signal_digit
                                next_signal_digits.remove(signal_digit)
                    
                signal_digit = next_signal_digits  

            sum += self.decodeOutput(output_digits, found_digits)
        return sum

    def matchDigits(self, found_digit, signal_digit):
        if found_digit == 0:
            return 0
        
        return len(set(signal_digit) & set(found_digit))

    def decodeOutput(self, output_digits, found_digits):
        sum = 0
        for digit in output_digits:
            for found_digit in found_digits:
                if len(digit) == len(found_digit) and self.matchDigits(found_digit, digit) == len(digit):
                    sum = sum * 10 + found_digits.index(found_digit)
        
        return sum

def first(displays):
    displays = Displays(displays)
    return displays.countOutput()

def second(displays):
    displays = Displays(displays)
    return displays.decodeDigits()

if __name__ == "__main__":
    path = "2021/day08"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input        (26):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input     (61229):", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")