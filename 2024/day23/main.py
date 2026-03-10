import timeit 
from pathlib import Path
from itertools import combinations

def preprocess(input_lines: list[int]):
    connections, computers = set(), set()
    for line in input_lines.split('\n'):
        a, b = line.strip().split('-')
        connections.update([(a, b), (b, a)])
        computers.update([a, b])

    return [connections, computers]

class Connections:
    def __init__(self, input):
        self.connections, self.computers = input

    def find_triples(self):
        return sum({(a, b), (b, c), (c, a)} < self.connections
                   and 't' in (a + b + c)[::2]
                   for a, b, c in combinations(self.computers, 3))

    def find_networks(self):
        self.networks = [{c} for c in self.computers]
        for network in self.networks:
            for c in self.computers:
                if all((c, n) in self.connections for n in network): network.add(c)
        return ','.join(sorted(max(self.networks, key = len)))

def first(input):
    connections = Connections(input)
    return connections.find_triples()

def second(input):
    connections = Connections(input)
    return connections.find_networks()

if __name__ == "__main__":
    path = "C:/Users/Ellis/Visual Studio Code Projects/Advent Of Code/2024/day23"

    example = Path(path + '/example.txt').read_text()

    input = Path(path + '/input.txt').read_text()

    print("Part 1 - Example input              (7):", first(preprocess(example)))

    start = timeit.default_timer()
    print("Part 1 - Actual input                  :", first(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input    (co,de,ka,ta):", second(preprocess(example)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input                  :", second(preprocess(input)))
    print(f"Time taken: {timeit.default_timer()-start}s")