from pathlib import Path


def preprocess(input_lines: list[int]):
    all_passwords = []
    passwords = input_lines.split('\n')
    for password_instance in passwords:
        occurrence, letter, password = password_instance.split(' ')
        min_occurrence, max_occurrence = occurrence.split('-')
        letter = letter.replace(":", "")
        all_passwords.append((int(min_occurrence), int(max_occurrence), letter, password))
    return all_passwords


def first(password_info):
    valid_passwords = 0
    for min_occurrence, max_occurrence, letter, password in password_info:
        occurrence = password.count(letter)
        if min_occurrence <= occurrence and occurrence <= max_occurrence:
            valid_passwords += 1
    return valid_passwords


def second(password_info):
    valid_passwords = 0
    for first_occurrence, second_occurrence, letter, password in password_info:
        if (password[first_occurrence - 1] == letter) ^ (password[second_occurrence - 1] == letter):
            valid_passwords += 1
    return valid_passwords


if __name__ == "__main__":
    data_path_example = Path('2020/day02/example02.txt')
    data_path_input = Path('2020/day02/input02.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(preprocess(data)))
    print(second(preprocess(data)))





























































# from pathlib import Path


# def preprocess(input_lines: list[int]):
#     all_passwords = []
#     passwords = input_lines.split('\n')
#     for password_instance in passwords:
#         occurrence, letter, password = password_instance.split(' ')
#         min_occurrence, max_occurrence = occurrence.split('-')
#         letter = letter.replace(":", "")
#         all_passwords.append((min_occurrence, max_occurrence, letter, password))
#         # all_passwords.append(min_occurrence)
#         # all_passwords.append(max_occurrence)
#         # all_passwords.append(letter)
#         # all_passwords.append(password)
#     return all_passwords


# def first(password_info):
#     valid_passwords = 0
#     for index in range(0, len(password_info)//4):
#         occurrence = 0
#         for password_letter in password_info[index * 4 + 3]:
#             if password_letter == password_info[index * 4 + 2]:
#                 occurrence += 1
#         if int(password_info[index * 4]) <= occurrence and occurrence <= int(password_info[index * 4 + 1]):
#             valid_passwords += 1
#     return valid_passwords


# def second(password_info):
#     valid_passwords = 0
#     for index in range(0, len(password_info)//4):
#         occurrence = 0
#         if password_info[index * 4 + 3][int(password_info[index * 4]) - 1] == password_info[index * 4 + 2]:
#             occurrence += 1
#         if password_info[index * 4 + 3][int(password_info[index * 4 + 1]) - 1] == password_info[index * 4 + 2]:
#             occurrence += 1
#         if occurrence == 1:
#             valid_passwords += 1
#     return valid_passwords


# if __name__ == "__main__":
#     data_path_example = Path('2020/day02/example02.txt')
#     data_path_input = Path('2020/day02/input02.txt')
#     example_data = data_path_example.read_text()
#     data = data_path_input.read_text()
#     print(first(preprocess(data)))
#     print(second(preprocess(data)))

    