from pathlib import Path
from pprint import pprint 


def preprocess(input_lines: list[int]):
    fields = input_lines.split("\n")
    return fields


def first(fields):
    for row in fields:
        if "S" in row:
            row_length = len(row)
            location = row.index("S")
            priority_queue = [[row * row_length + location, "S", 0]]
        if "E" in row:
            location = row.index("E")
            graph_target = row * row_length + location
    visited = []


    while len(priority_queue) > 0:
        current_node = priority_queue.pop(0)

        if current_node[1] != graph_target:
            if current_node not in visited:
                visited.append(current_node)
                for next_node in get_neighbours(current_node, row_length):
                    if next_node not in visited:
                        gscore = manhattan_distance(graph_target)
                        fscore = current_node.get_distance() + 1
                        score = gscore + fscore
                        next_node.set_score(score)
                        if next_node not in priority_queue:
                            next_node.set_parent(current_node)
                            next_node.set_score(score)
                            next_node.set_distance(fscore)
                            bisect.insort_left(priority_queue, next_node)
                        elif next_node.distance < current_node.distance:
                            next_node.set_parent(current_node)
                            next_node.set_score(score)
                            next_node.set_distance(fscore)
                            priority_queue.remove(next_node)
                            bisect.insort_left(priority_queue, next_node)
                
def manhattan_distance(self, other):
    x_distance = abs(self.position[0] - other.position[0])
    y_distance = abs(self.position[1] - other.position[1])
    return x_distance + y_distance

def get_neighbours(current_node, fields):
    row_length = len(fields[0])
    alphabet = "SabcdefghijklmnopqrstuvwxyzE"

    neighbours = [current_node - 1, current_node + 1, current_node - row_length, current_node + row_length]
    relevant_neighbours = []
    for neighbour in neighbours:
        if abs(alphabet.index(current_node[1]) - alphabet.index(fields[neighbour])) <= 1:
            relevant_neighbours.append(neighbour, fields[neighbour], current_node[2] + 1)

    return relevant_neighbours
    

def second(commands):
    pass

if __name__ == "__main__":
    path = "2022/day12"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(preprocess(example_data)))
    print(first(preprocess(data)))
    print(second(preprocess(example_data)))
    print(second(preprocess(data)))
    