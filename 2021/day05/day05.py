from pathlib import Path
import timeit 

def preprocess(input_lines: list[int]):
    lines = input_lines.split('\n')
    vents = []
    for line in lines:
        coordinates = line.split(' -> ')
        vent = []
        for coordinate in coordinates:
            x,y = coordinate.split(',')
            vent.append([int(x), int(y)])
        vents.append(vent)
    return vents

class Vents:
    def __init__(self, vents):
        self.vents = vents
        self.straightVents = []
        self.field = []
        self.findDimensions()
    
    def findDimensions(self):
        max_x = 0
        max_y = 0
        for vents in self.vents:
            for vent in vents:
                max_x = max(max_x, vent[0])
                max_y = max(max_y, vent[1])
        
        self.createField(max_x + 1, max_y + 1)
    
    def createField(self, max_x, max_y):
        self.field = [[0 for _ in range(max_x)] for _ in range(max_y)]
    
    def findStraightVents(self):
        for vent in self.vents:
            if vent[0][0] == vent[1][0]:
                self.straightVents.append(vent)
            elif vent[0][1] == vent[1][1]:
                self.straightVents.append(vent)

    def placeVents(self, vents):
        for vent in vents:
            x = vent[0][0]
            y = vent[0][1]
            x_smaller = x < vent[1][0]
            y_smaller = y < vent[1][1]
            for _ in range(self.findVentLength(vent)):
                self.field[y][x] += 1

                if x < vent[1][0] and x_smaller:
                    x += 1
                elif x > vent[1][0]:
                    x -= 1

                if y < vent[1][1] and y_smaller:
                    y += 1
                elif y > vent[1][1]:
                    y -= 1
        
    def findVentLength(self, vent):
        diff_x = abs(vent[1][0] - vent[0][0]) + 1
        diff_y = abs(vent[1][1] - vent[0][1]) + 1
        return max(diff_x, diff_y)
        
    def findCrossingVents(self):     
        count = 0
        for row in self.field:
            count += sum(field >= 2 for field in row)
        return count


def first(vents):
    vents = Vents(vents)
    vents.findStraightVents()
    vents.placeVents(vents.straightVents)
    return vents.findCrossingVents()

def second(vents):
    vents = Vents(vents)
    vents.placeVents(vents.vents)
    return vents.findCrossingVents()

if __name__ == "__main__":
    path = "2021/day05"

    data_path_example = Path(path + '/example.txt')

    data_path_input = Path(path + '/input.txt')

    example_data = data_path_example.read_text()

    data = data_path_input.read_text()

    print("Part 1 - Example input         (5):", first(preprocess(example_data)))

    start = timeit.default_timer()
    print("Part 1 - Actual input             :", first(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s\n")

    print("Part 2 - Example input          ():", second(preprocess(example_data)))
    
    start = timeit.default_timer()
    print("Part 2 - Actual input             :", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")