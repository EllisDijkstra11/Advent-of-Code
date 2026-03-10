from pathlib import Path
from pprint import pprint 

def preprocess(input_lines: list[int]):
    lines = input_lines.splitlines()     

    hands = []
    for line in lines:
        hands.append(line.split(" "))
    
    return hands


def first(hands):
    total_sum = 0
    scored_hands = []
    for hand in hands:
        cards_strength, card_count, bet = restructure_hand(hand, False)
        scored_hands.append([find_hand(card_count), cards_strength, bet])
    
    scored_hands.sort()
    
    for hand in scored_hands:
        total_sum += int(hand[2]) * (scored_hands.index(hand) + 1)

    return total_sum


def second(hands):
    total_sum = 0
    scored_hands = []
    for hand in hands:
        cards_strength, card_count, hands, bet = restructure_hand(hand, True)
        scored_hands.append([find_hand(card_count), cards_strength, hands, bet])
    
    scored_hands.sort()
    
    for hand in scored_hands:
        total_sum += int(hand[3]) * (scored_hands.index(hand) + 1)

    
    return total_sum


def restructure_hand(hand, jokers):
    card_strength = []
    if not jokers:
        card_strength = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    else:
        card_strength = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]

    cards, bet = hand

    cards_list = []
    cards_strength = []
    for card in cards:
        cards_list.append([card])
        cards_strength.append(len(card_strength) - card_strength.index(card))

    amount_of_jokers = cards_list.count(["J"])
    
    sorted_cards = []
    card_count = [0]
    for card in card_strength:
        count = 0
        while [card] in cards_list:
            count += 1
            sorted_cards.append(card)
            cards_list.remove([card])
        if count != 0 and (not jokers or card != "J"):
            card_count.append(count)
    
    sorted_cards = ''.join(sorted_cards)
    
    card_count.sort(reverse = True)
    if jokers:
        card_count[0] += amount_of_jokers

    return cards_strength, card_count, cards, bet

def find_hand(card_count):
    if card_count[0] == 5:
        return 6
    elif card_count[0] == 4:
        return 5
    elif card_count[0] == 3:
        if card_count[1] == 2:
            return 4
        else:
            return 3
    elif card_count[0] == 2:
        if card_count[1] == 2:
            return 2
        else:
            return 1
    else:
        return 0


if __name__ == "__main__":
    path = "2023/day07"
    data_path_example = Path(path + '/example.txt')
    data_path_input = Path(path + '/input.txt')
    data_path_Jeroen = Path(path + '/inputJeroen.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    Jeroens_data = data_path_Jeroen.read_text()
    # print("Part 1 - Example input : ", first(preprocess(example_data)))
    # print("Part 1 - Actual input  : ", first(preprocess(data)))
    print("Part 2 - Example input : ", second(preprocess(example_data)))
    print("Part 2 - Actual input  : ", second(preprocess(data)))
    print("Part 2 - Jeroen's input: ", second(preprocess(Jeroens_data)))