from pathlib import Path

def preprocess(input_lines: list[int]):
    money = [int(n) for n in input_lines.split('\n')]
    return money

def first(money: list[int]) -> int:
    for first_money in money:
        second_money = 2020 - first_money
        if second_money in money:
            return first_money * second_money

def second(money: list[int]) -> int:
    for first_money in money:
        for second_money in money:
            if first_money is not second_money:
                third_money = 2020 - first_money - second_money
                if third_money in money:
                    return first_money * second_money * third_money


if __name__ == "__main__":
    data_path_example = Path('2020/day01/example01.txt')
    data_path_input = Path('2020/day01/input01.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(preprocess(data)))
    print(second(preprocess(data)))

    