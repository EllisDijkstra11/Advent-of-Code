from pathlib import Path
from tokenize import String
import re
import string

def preprocess(input_lines: list[int]):
    all_passports = []
    passports = input_lines.split('\n\n')
    for passport in passports:
        split_passport = re.split('\n| |:', passport)
        #split_passport = split_passport.split(' ')
        all_passports.append(split_passport)
    return all_passports

def first(passports):
    valid_passports = 0
    for passport in passports:
        passport_is_valid = True
        if "byr" not in passport:
            passport_is_valid = False
        if "iyr" not in passport:
            passport_is_valid = False
        if "eyr" not in passport:
            passport_is_valid = False
        if "hgt" not in passport:
            passport_is_valid = False
        if "hcl" not in passport:
            passport_is_valid = False
        if "ecl" not in passport:
            passport_is_valid = False
        if "pid" not in passport:
            passport_is_valid = False
        if passport_is_valid:
            valid_passports += 1
    return valid_passports

def second(passports):
    valid_passports = 0
    for passport in passports:
        passport_is_valid = True
        if "byr" not in passport:
            passport_is_valid = False
        if "iyr" not in passport:
            passport_is_valid = False
        if "eyr" not in passport:
            passport_is_valid = False
        if "hgt" not in passport:
            passport_is_valid = False
        if "hcl" not in passport:
            passport_is_valid = False
        if "ecl" not in passport:
            passport_is_valid = False
        if "pid" not in passport:
            passport_is_valid = False
        if not passport_is_valid:
            continue
        for information in range(0, len(passport)//2):
            index = passport[information * 2]
            value = passport[information * 2 + 1]
            if index == "byr":
                if int(value) < 1920 or int(value) > 2002:
                    passport_is_valid = False
            if index == "iyr":
                if int(value) < 2010 or int(value) > 2020:
                    passport_is_valid = False
            if index == "eyr":
                if int(value) < 2020 or int(value) > 2030:
                    passport_is_valid = False
            if index == "hgt":
                if (value[len(value) - 2] + value[len(value) - 1]) == "cm":
                    if value[2] != "c":
                        height = int(value[0] + value[1] + value[2])
                        if height < 150 or height > 193:
                            passport_is_valid = False
                    else:
                        passport_is_valid = False
                elif (value[len(value) - 2] + value[len(value) - 1]) == "in":
                    if value[1] != "i":
                        height = int(value[0] + value[1])
                        if height < 59 or height > 76:
                            passport_is_valid = False
                    else:
                        passport_is_valid = False
                else:
                    passport_is_valid = False
            if index == "hcl":
                letters = list(string.ascii_lowercase)
                letters.remove("a")
                letters.remove("b")
                letters.remove("c")
                letters.remove("d")
                letters.remove("e")
                letters.remove("f")
                if len(value) != 7:
                    passport_is_valid = False
                else:
                    for letter in value:
                        if letter in letters:
                            passport_is_valid = False
                            continue
            if index == "ecl":
                colours = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
                if value not in colours:
                    passport_is_valid = False
            if index == "pid":
                if len(value) != 9:
                    passport_is_valid = False
        if passport_is_valid:
            valid_passports += 1

    return valid_passports


if __name__ == "__main__":
    data_path_example = Path('2020/day04/example04.txt')
    data_path_input = Path('2020/day04/input04.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(preprocess(data)))
    print(second(preprocess(data)))
    