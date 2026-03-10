from pathlib import Path
from pprint import pprint 
import timeit

def preprocess(input_lines: list[int]):
    alineas = input_lines.split("\n\n")

    maps = []
    for alinea in alineas:
        maps.append(alinea.splitlines())

    for map in maps:
        del(map[0])

    numbers = []
    for map in maps:
        lines = []
        for line in map:
            lines.append(line.split(" "))
        numbers.append(lines)

    seeds = numbers[0][0]
    del(numbers[0])
    results = []

    for seed in seeds:
        results.append(int(seed))
      
    seeds = results.copy()

    return([seeds] + [numbers])


def first(numbers):
    seeds = numbers[0]
    maps = numbers[1]
    
    results = []

    index = 0
    while index < len(maps):
        for seed in seeds:
            found = False
            for number in maps[index]:
                destination = int(number[0])
                source = int(number[1])
                source_range = int(number[2])
                if not found and seed >= source and seed < source + source_range:
                    results.append(destination + seed - source)
                    found = True

            if not found:
                results.append(seed)

        seeds = results.copy()
        results = []
        index += 1
    
    return(min(seeds))


def second (numbers):
    seeds = numbers[0]
    maps = numbers[1]
    
    results = []

    index = 0
    while index < len(seeds):
        results.append([seeds[index], seeds[index + 1]])

        index += 2
    
    seeds = results.copy()
    results = []

    index = 0
    while index < len(maps):
        for seed in seeds:
            seed_source = seed[0]
            seed_range = seed[1]
            seed_end = seed_source + seed_range
            found = False
            for number in maps[index]:
                map_destination = int(number[0])
                map_source = int(number[1])
                map_range = int(number[2])
                map_end = map_source + map_range
                if not found and seed_source >= map_source:
                    if seed_end < map_end: # if the seed lies completely in the map
                        results.append([map_destination + seed_source - map_source, seed_range])
                        found = True
                    elif seed_source < map_end: # if the first part of the seed lies in the map
                        results.append([map_destination + seed_source - map_source, map_end - seed_source])
                        seeds.append([map_end , seed_end - map_end])
                        found = True
                elif not found and seed_end > map_source:
                    if seed_end < map_end: # if the last part of the seed lies in the map
                        results.append([map_destination, seed_end - map_source])
                        seeds.append([seed_source, map_source - seed_source])
                        found = True
                    elif seed_source < map_source: # if the middle part of the seed lies in the map
                        seeds.append([seed_source, map_source - seed_source])
                        results.append([map_destination, map_range])
                        seeds.append([map_end + 1, seed_end - map_end])
                        found = True

            if not found:
                results.append(seed)

        seeds = results.copy()
        results = []
        index += 1
    
    for seed in seeds:
        results.append(seed[0])
    
    return(min(results))


if __name__ == "__main__":
    path = "2023/day05"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')
    data_path_Jeroen = Path(path + '/inputJeroen.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    Jeroens_data = data_path_Jeroen.read_text()
    print("Part 1 - Example input : ", first(preprocess(example_data)))
    print("Part 1 - Actual input  : ", first(preprocess(data)))
    print("Part 2 - Example input : ", second(preprocess(example_data)))
    start = timeit.default_timer()
    print("Part 2 - Actual input  : ", second(preprocess(data)))
    print(f"Time taken: {timeit.default_timer()-start}s")

    print("Part 2 - Jeroen's input: ", second(preprocess(Jeroens_data)))

    