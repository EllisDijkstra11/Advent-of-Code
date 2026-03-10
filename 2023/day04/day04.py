from pathlib import Path
from pprint import pprint 

def preprocess(input_lines: list[int]):
    lines = input_lines.splitlines()
    all_numbers = []
    for line in lines:
        all_numbers.append(line[9:])

    cards = []
    for number in all_numbers:
        winning_numbers, numbers = number.split("|")
        cards.append([winning_numbers, numbers])

    split_cards = []
    for card in cards:
        winning_number, number = card
        split_winning_number = winning_number.split(" ")
        split_numbers = number.split(" ")
        split_cards.append([split_winning_number, split_numbers])

    for card in split_cards:
        winning_number, number = card
        while "" in winning_number:
            winning_number.remove("")
        while "" in number:
            number.remove("")

    return split_cards


def first(cards):
    total_sum = 0
    for card in cards:
        current_sum = 0
        winning_numbers, numbers = card
        for number in numbers:
            if number in winning_numbers:
                if current_sum == 0:
                    current_sum = 1
                else:
                    current_sum *= 2
        total_sum += current_sum
    return total_sum


def second(cards):
    amount_of_cards = []
    for card in cards:
        amount_of_cards.append(1)

    card_index = 0
    while card_index < len(cards):
        current_sum = 0
        winning_numbers, numbers = cards[card_index]
        for number in numbers:
            if number in winning_numbers:
                current_sum += 1
        
        winning_card_index = card_index + 1
        while current_sum > 0:
            amount_of_cards[winning_card_index] += amount_of_cards[card_index]
            winning_card_index += 1
            current_sum -= 1

        card_index += 1

    return sum(amount_of_cards)



if __name__ == "__main__":
    path = "2023/day04"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print("Part 1 - Example input : ", first(preprocess(example_data)))
    print("Part 1 - Actual input  : ", first(preprocess(data)))
    print("Part 2 - Example input : ", second(preprocess(example_data)))
    print("Part 2 - Actual input  : ", second(preprocess(data)))
    