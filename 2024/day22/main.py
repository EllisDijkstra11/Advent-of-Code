import timeit 
import pprint
import functools
from pathlib import Path
from collections import defaultdict, deque

def preprocess(input_lines: list[int]):
    return [int(n) for n in input_lines.split('\n')]

class Secrets:
    def __init__(self, input):
        self.secrets = input
        self.new_secrets = []
        self.differences = deque([], 4)
        self.bananas = defaultdict(int)
    
    def get_new_secrets(self):
        return sum(self.new_secrets)

    def get_bananas(self):
        return max(self.bananas.values())
    
    def find_all_secrets(self, repeats):
        for secret in self.secrets:
            current_bananas = set()
            for _ in range(repeats):
                new_secret = self.find_next_secret(secret)

                current_prize = secret % 10
                new_prize = new_secret % 10
                difference = new_prize - current_prize
            
                self.differences.append(difference)

                if len(self.differences) == 4 and tuple(self.differences) not in current_bananas:
                    self.bananas[tuple(self.differences)] += new_prize
                    current_bananas.add(tuple(self.differences))
                
                secret = new_secret

            self.new_secrets.append(secret)

    def find_next_secret(self, secret):
        prune = 16777216

        secret = ((secret * 64) ^ secret) % prune
        secret = ((secret // 32) ^ secret) % prune
        secret = ((secret * 2048) ^ secret) % prune

        return secret

def first(input):
    secrets = Secrets(input)
    secrets.find_all_secrets(2000)
    return secrets.get_new_secrets()

def second(input):
    secrets = Secrets(input)
    secrets.find_all_secrets(2000)
    return secrets.get_bananas()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day22"

    example_one = Path(path + '/example_one.txt').read_text()
    example_two = Path(path + '/example_two.txt').read_text()

    input = Path(path + '/input.txt').read_text()

    print("Part 1 - Example input  (37327623):", first(preprocess(example_one)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input        (23):", second(preprocess(example_two)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s")