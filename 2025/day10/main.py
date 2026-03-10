import os
import timeit
import numpy as np
# from sympy import symbols, Eq, solve
from math import prod
from pprint import pprint
from pathlib import Path
from itertools import chain, pairwise, product, combinations as comb, starmap, permutations as perm
from functools import reduce

def preprocess(input_lines: list[int]):
    lines = [[string for string in line.split(' ')] for line in input_lines.split('\n')]

    machines = []
    for line in lines:
        # goal = [True if light == '#' else False for light in line[0][1:-1]]
        goal = [0 if light == '.' else 1 for light in line[0][1:-1]]
        buttons = [[int(b) for b in button[1:-1].split(',')] for button in line[1:-1]]
        energy = [int(number) for number in line[-1][1:-1].split(',')]
        machines.append([goal, buttons, energy])
    return machines

def find_first_combination(machine):
    goal, buttons, _ = machine
    len_sequence = 0

    while _:
        len_sequence += 1

        for combination in comb(buttons, len_sequence):
            presses = list(chain.from_iterable(combination))
            lights = [presses.count(i) % 2 for i in range(len(goal))]

            if lights == goal:
                return len_sequence

def gaussian_elimination(machine):
    _, buttons, goal = machine
    global new_update
    
    def find_max(buttons_dict, lights_dict):
        for button in buttons_dict:
            if button['actual'] == None:
                button['min'] = 0
                button['max'] = min(lights_dict[b]['target'] for b in button['button'])

        return buttons_dict

    def find_min(buttons_dict, lights_dict):
        for i, light in enumerate(lights_dict):
            if not light['done']:
                total = sum([buttons_dict[l]['max'] for l in light['light']])
                for l in light['light']:
                    other = total - buttons_dict[l]['max']
                    buttons_dict[l]['min'] = max(buttons_dict[l]['min'], light['target'] - other)

        return buttons_dict
    
    def remove_double_lights(buttons_dict, lights_dict):
        for first, second in comb(lights_dict, 2):
            if first['light'] == second['light'] and first['target'] == second['target']:
                remove_button = sorted([first, second], key= lambda b: len(b['original'])).pop(0)
                remove_button['done'] = True
                remove_button['target'] = 0
            
                for button in buttons_dict:
                    if remove_button['id'] in button['button']:
                        button['button'] -= {remove_button['id']}

        # print("double", lights_dict)
        return buttons_dict, lights_dict

    def update(button_index, presses, buttons_dict, lights_dict):
        global new_update
        new_update = True

        button = buttons_dict[button_index]
        button['actual'] = presses

        for l in list(button['button']):
            light = lights_dict[l]

            light['light'] -= {button_index}
            light['equation'][button_index] = 0
            light['target'] -= presses

            if len(light['light']) == 0:
                light['done'] = True
        
        buttons_dict, lights_dict = remove_double_lights(buttons_dict, lights_dict)
        buttons_dict = find_max(buttons_dict, lights_dict)
        buttons_dict = find_min(buttons_dict, lights_dict)
        
        if debugging:
            print('\n--- UPDATE', button_index, '---\nlights')
            pprint([light for light in lights_dict if not light['done']])

            print('\nbuttons_dict')
            pprint(buttons_dict)

        return find_equal_buttons(buttons_dict, lights_dict)

    def find_equal_buttons(buttons_dict, lights_dict):
        for button in buttons_dict:
            if button['min'] == button['max'] and button['actual'] == None:
                return update(button['id'], button['min'], buttons_dict, lights_dict)
        
        return buttons_dict, lights_dict
    
    def find_equal_sets(buttons_dict, lights_dict):
        button_indexes = [button['id'] for button in buttons_dict if button['actual'] == None]

        sets = []
        for i in range(1, len(button_indexes) + 1):
            for combinations in comb(button_indexes, i):
                current_buttons = [buttons_dict[c]['button'].copy() for c in list(combinations)]

                intersection_set = current_buttons[0].copy()
                current_set = current_buttons.pop(0)
                while len(current_buttons) > 0:
                    intersection_set |= current_buttons[0].copy()
                    current_set ^= current_buttons.pop(0)

                if len(current_set) > 0 and current_set == intersection_set:
                    # print(combinations, intersection_set, current_set)
                    sets.append([set(combinations), current_set])
        # print("sets", sets)

        for [f_i, f_s], [s_i, s_s] in comb(sets, 2):
            if not f_i & s_i and not len(f_i) == len(s_i) and f_s == s_s:
                # print([f_i, f_s], [s_i, s_s], f_i & s_i, f_s == s_s)
                large, small = sorted([f_i, s_i], key=lambda x: len(x))
                # print(list((buttons_dict[b]['id'], buttons_dict[b]['max'], buttons_dict[b]['min']) for b in list(small | large)))
                presses = min(buttons_dict[b]['max'] - buttons_dict[b]['min'] for b in list(small | large))
                # print(presses)
                # print(presses)
                for b in small:
                    buttons_dict[b]['max'] -= presses 
                for b in large:
                    buttons_dict[b]['min'] += presses 

                # print(list((buttons_dict[b]['id'], buttons_dict[b]['max'], buttons_dict[b]['min']) for b in list(small | large)))
                buttons_dict, lights_dict = find_equal_buttons(buttons_dict, lights_dict)
                return find_equal_sets(buttons_dict, lights_dict)

        return buttons_dict, lights_dict
    
    def find_proper_subsets(buttons_dict, lights_dict):
        global new_update
        button_indexes = [button['id'] for button in buttons_dict if button['actual'] == None]

        for f, s in comb(button_indexes, 2):
            first, second = buttons_dict[f], buttons_dict[s]
            if second['button'] <= first['button']:
                first, second = second, first

            if first['button'] <= second['button']:
                for button in [button for button in buttons_dict if button['id'] not in [f, s]]:
                    if first['button'] <= button['button']:
                        break
                new_update = True
                print(first, second)
                presses = min(first['max'] - first['min'], second['max'] - second['min'])
                first['max'] -= presses
                second['min'] += presses

        return buttons_dict, lights_dict

    def find_next_combination(buttons_dict, lights_dict):
        lights = [light['light'] for light in lights_dict if not light.get('done')]
        print(lights)

        for i in range(2, len(lights) + 1):
            for combination in comb(range(len(lights)), i):
                current_buttons = [lights[c].copy() for c in list(combination)]
                current_set = current_buttons.pop(0)
                while len(current_buttons) > 0:
                    current_set ^= current_buttons.pop(0)

                if len(current_set) == 1:
                    return combination
        return None
        
        return None

    target = goal.copy()
    buttons_dict = [{'id': i, 'button': set(b for b in button)} for i, button in enumerate(buttons)]
    for i, button in enumerate(buttons_dict):
        button['min'] = 0
        button['max'] = min(target[b] for b in button['button'])
        button['actual'] = None
        button['original'] = button['button'].copy()
    
    lights_dict = [{'id': i, 'light': set(b for b, button in enumerate(buttons) if i in button)} for i in range(len(goal))]
    for i, light in enumerate(lights_dict):
        light['done'] = False
        light['equation'] = [1 if i in button else 0 for button in buttons]
        light['target'] = target[i]
        light['goal'] = target[i]
        light['original'] = light['light'].copy()
    
    buttons_dict, lights_dict = remove_double_lights(buttons_dict, lights_dict)
    
    buttons_dict = find_min(buttons_dict, lights_dict)

    if debugging:
        print('\n--- BEFORE INITIAL ---\nlights')
        pprint([light for light in lights_dict if not light['done']])

        print('\nbuttons_dict')
        pprint(buttons_dict)

    new_update = True
    while new_update:
        new_update = False

        # print('equal button')
        buttons_dict, lights_dict = find_equal_buttons(buttons_dict, lights_dict)
        # print('equal set')
        buttons_dict, lights_dict = find_equal_sets(buttons_dict, lights_dict)
        # print('subset')
        # buttons_dict, lights_dict = find_proper_subsets(buttons_dict, lights_dict)
        # combination = find_next_combination(buttons_dict, lights_dict)
        # print(list(combination) if combination != None else None)

    if True:
        # print('\n\n--- AFTER INITIAL ---\nlights')
        # pprint([light for light in lights_dict])

        print('\nbuttons_dict')
        pprint(buttons_dict)

        # if combination == None:
        #     #brute_force()
        #     pass

    actual = [button['actual'] for button in buttons_dict]
    if None in actual:
        return brute_force(buttons_dict, lights_dict)

    # , lights, '- buttons', buttons_dict, '- goal', target)
    return sum(actual)

def mess():
        
    def brute_force4(buttons, lights, target):
        options = {str(b): [] for b in set([b for button in lights for b in button])}
        lights = [set(str(l) for l in light) for light in lights]

        for o in options.keys():
            for l, t in zip(lights, target):
                if o in l:
                    options[o] += [[t, l - set(o)]]
        
        for light in lights:
            print(options)
        while _:
            pass
        pass

    def find_echelon_form(buttons_dict, lights_dict):
        unpressed_buttons = [button['id'] for button in buttons_dict if button['actual'] == None]
        for button in buttons_dict:
            if button['actual'] == None:
                pass
        # reorder_matrix = zip(matrix, target)
        
        # print(reorder_matrix)
        pass

    # find_echelon_form(buttons_dict, lights_dict)
    return 0
    while len(lights) > 0:
        print(lights)
        combination = find_next_pressed(lights)
        print(combination, lights)

        if combination == None:
            brute_force(buttons, lights, target)
        elif len(combination) == 1:
            next = combination[0]
            presses = target.pop(next)
            button = lights.pop(next)

            total += presses
            for o, other in enumerate(lights):
                if button in other:
                    target[o] -= presses
                    lights[o] -= button

        elif len(combination) == 2:
            print(combination)
            f, s = combination[0], combination[1]
            if f <= s:
                target[s] -= target[f]
                lights[s] -= lights[f]
            elif s <= f:
                target[f] -= target[s]
                lights[f] -= lights[s]

    print(lights)

    return total

def brute_force(buttons_dict, lights_dict):
    # print("\n---BRUTE FORCE---")
    for button in buttons_dict:
        # button['range'] = button['max'] - button['min'] + 1
        button['range'] = list(range(button['min'], button['max'] + 1))
    
    # pprint(buttons_dict)
    def generate_combinations(buttons_dict, lights_dict):

        def filter_combinations(combination):
            for lights in lights_dict:
                light, target = lights['original'], lights['goal']
                presses = [combination[l] if combination[l] != None else 0 for l in light]

                if target < sum(presses):
                    # print('b', combination, light, target) if combination[0] == 10 else False
                    return 'break'
                
            for lights in lights_dict:
                light, target = lights['original'], lights['goal']
                presses = [combination[l] for l in light]
                
                if not None in presses and target != sum(presses):
                    # print('c', combination, light, target, max(light), len(combination), sum(combination[l] for l in light)) if combination[0] == 10 else False
                    return 'continue'
            
            # print('t', combination) if combination[0] == 10 else False
            return True
        
        def final_combinations(combination):
            for light in lights_dict:
                if light['goal'] != sum(combination[l] for l in light['light']):
                    print('happens')
                    return False
            
            return True

        print('# of options:', prod(button['max'] - button['min'] for button in buttons_dict))
        # print(ranges)
        # pprint(buttons_dict)

        combinations = [[b['actual'] for b in buttons_dict]]
        options = {b['id']: [light['light'] - {b['id']} for light in lights_dict if b['id'] in light['light']] for b in buttons_dict if b['actual'] == None}
        
        # sorted_buttons = sorted(buttons_dict.copy(), key= lambda r: len(r['range']), reverse=True)
        # while any(None in combinations[0]):
        #     current_button = sorted_buttons.pop()

        # sorted_indexes = [button['id'] for button in sorted(buttons_dict.copy(), key= lambda r: len(r['range']), reverse=True)]
        index = next(button['id'] for button in sorted(buttons_dict.copy(), key=lambda b: len(b['range'])) if len(button['range']) > 1)
        while None in combinations[0]:
            new_combinations = []
            index = min(options.key(), key=lambda b: min(options[b], key=lambda c: len(c)) * len(buttons_dict[b]['range'])).key()
            possible_values = tuple(buttons_dict[index]['range'])

            for x in combinations:
                for y in possible_values:
                    new = x.copy()
                    new[index] = y
                    match filter_combinations(new):
                        case True:
                            new_combinations.append(new)
                        case 'continue':
                            continue
                        case 'break':
                            break
            combinations = new_combinations.copy()
            if len(combinations) == 0:
                return None
            
            del options[index]
            options = {key: [v - {index} if index in v and len(v) > 1 else v for v in value] for key, value in options.items()}
 
        combinations = [combination for combination in combinations if final_combinations(combination)]
        return combinations
    
        # WORKING
        # WORKING, but generates all in-between options too
        combinations = [[b['actual'] for b in buttons_dict]]
        
        # sorted_buttons = sorted(buttons_dict.copy(), key= lambda r: len(r['range']), reverse=True)
        # while any(None in combinations[0]):
        #     current_button = sorted_buttons.pop()

        sorted_indexes = next(button['id'] for button in sorted(buttons_dict.copy(), key=lambda b: len(b['range'])) if len(button['range']) > 1)
        sorted_indexes = [button['id'] for button in sorted(buttons_dict.copy(), key= lambda r: len(r['range']), reverse=True)]
        while None in combinations[0]:
            new_combinations = []
            index = next(index for index in sorted_indexes if combinations[0][index] == None)
            possible_values = tuple(buttons_dict[index]['range'])

            for x in combinations:
                for y in possible_values:
                    new = x.copy()
                    new[index] = y
                    match filter_combinations(new):
                        case True:
                            new_combinations.append(new)
                        case 'continue':
                            continue
                        case 'break':
                            break
            combinations = new_combinations.copy()
            if len(combinations) == 0:
                return None
 
        combinations = [combination for combination in combinations if final_combinations(combination)]
        return combinations

        # Mess
        combinations = [[]]
        for button in buttons_dict:
            new_combinations = []
            possible_values = tuple(button['range'])

            for x in combinations:
                for y in possible_values:
                    # print(x + [y])

                    match filter_combinations(x + [y]):
                        case True:
                        # print(True, y)
                            new_combinations.append(x + [y])
                        case 'continue':
                        # print(new_combinations)
                            continue
                        case 'break':
                            # print(False, y)
                            break
            combinations = new_combinations.copy()
 
        combinations = [combination for combination in combinations if final_combinations(combination)]
        return combinations
            
    
    # print(possible_presses, lights)
    # total_presses = [[p for p in range(0, presses)] for presses in max_presses]
    # print(list(product(*possible_presses)))
    # combinations = starmap(filter_combinations, product(possible_presses))
    # combinations = (presses for presses in list(product(*possible_presses)) if filter_combinations(presses))
    combinations = generate_combinations(buttons_dict, lights_dict)
    # print('\nCombinations:', combinations)
    # pprint(combinations)
    # print('[10, 7, 4, 17, 20, 20, 0]')

    minimum = min(combinations, key=lambda c: sum(c))
    # print(filtered)
    return sum(minimum)

    all_options.sort(key=lambda o: sum(o))
    for presses in all_options:
        # lights = [first + second for first, second in [button * press for button, press in zip(buttons, presses)]]
        lights_dict = [int(p) for p in sum([button[press] for button, press in zip(buttons_dict, presses)])]

        if lights_dict == goal:
            return sum(presses)

def brute_force2(buttons, goal):
    lights = [set(b for b, button in enumerate(buttons) if i in button) for i in range(len(goal))]
    pprint([1, buttons, lights, goal])
    possible_presses = [list(range(0, min([goal[light] for light in button]) + 1)) for button in buttons]
    print(possible_presses)
    def filter_combinations(presses):
        # print("p", presses)
        for i in range(len(goal)):
            if max(lights[i]) < len(presses) and goal[i] != sum(presses[l] for l in lights[i]):
                return False
            # print(goal, i)
            
            if goal[i] < sum(presses[l] if l < len(presses) else 0 for l in lights[i]):
                return False
        
        return True

    def final_combinations(presses):
        print(presses)
        for g, light in zip(goal, lights):
            if g != sum(presses[l] for l in light):
                print("happens")
                return False
        
        return True
    
    def generate_combinations(possible_presses):
        possible_presses = [tuple(p) for p in possible_presses]

        combinations = [[]]        
        for press in possible_presses:
            combinations = [x + [y] for x in combinations for y in press if filter_combinations(x + [y])]            
        
        combinations = [combination for combination in combinations if sum([c * len(b) for c, b in zip(combination, buttons)]) == sum(goal)]

        return combinations
            
    
    # print(possible_presses, lights)
    # total_presses = [[p for p in range(0, presses)] for presses in max_presses]
    # print(list(product(*possible_presses)))
    # combinations = starmap(filter_combinations, product(possible_presses))
    # combinations = (presses for presses in list(product(*possible_presses)) if filter_combinations(presses))
    combinations = generate_combinations(possible_presses)
    pprint(combinations)
    minimum = min(combinations, key=lambda c: sum(c))
    print(27, 3, 21, 0, 3, 7, 30)
    print(len(combinations))
    # pprint(combinations)
    # minimum = sum(next(c for c in combinations if final_combinations(c)))
    # print(filtered)
    return minimum
    all_options.sort(key=lambda o: sum(o))
    for presses in all_options:
        # lights = [first + second for first, second in [button * press for button, press in zip(buttons, presses)]]
        lights = [int(p) for p in sum([button[press] for button, press in zip(buttons, presses)])]

        if lights == goal:
            return sum(presses)

def find_new_joltage_combinations(machine):
    _, buttons, goal = machine

    targets = goal.copy()
    actual_presses = [None for _ in buttons]
    maximum_presses = [min([targets[b] for b in button]) for button in buttons]
    ranges = [[0, p] for p in maximum_presses]
    lights = [[b for b, button in enumerate(buttons) if l in button] for l in range(len(goal))]

    def single_light():
        changes = False
        for l, light in enumerate(lights):
            if len(light) == 1 and targets[l] != None:
                changes = True
                update(l)
        
        return changes
    
    def empty_target():
        changes = False
        for t, target in enumerate(targets):
            if target == 0:
                changes = True
                update(t)

        return changes

    def update(index):
        # print(index)
        pressed = targets[index] if targets[index] != None else 0

        targets[index] = None
        for button in lights[index]:
            ranges[button] = [pressed, pressed]
            actual_presses[button] = pressed

        button = set(b for l in lights[index] for b in buttons[l])# for l in light)
        # button = buttons[lights[index]]
        for other_light in button:
            if targets[other_light] != None:
                # print(targets[other_light], pressed)
                targets[other_light] -= pressed
        
        for l, light in enumerate(lights):
            if index in light:

                actual_presses[l] = 0

    while single_light() or empty_target():
        pass

    def find_min_ranges():
        # print(actual_presses)
        # print(ranges)

        for l, light in enumerate(lights):
            total = sum(maximum_presses[m] for m in light)
            target = targets[l]

            for t in light:
                if ranges[t][0] != ranges[t][1]:
                    ranges[t][0] = min(max(ranges[t][0], target - total + maximum_presses[t]), ranges[t][1])
        
        # print(ranges)
        return ranges
    
    def generate_combinations(possibilities):
        possibilities = [tuple(p) for p in possibilities]

        combinations = [[]]        
        for press in possibilities:
            combinations = [x + [y] for x in combinations for y in press if filter_combinations(x + [y])]            
        
        combinations = [combination for combination in combinations if sum([c * len(b) for c, b in zip(combination, buttons)]) == sum(goal)]

        return combinations
    
    def filter_combinations(presses):
        # print("p", presses)
        for i in range(len(goal)):
            if max(lights[i]) < len(presses) and goal[i] != sum(presses[l] for l in lights[i]):
                return False
            # print(goal, i)
            
            if goal[i] < sum(presses[l] if l < len(presses) else 0 for l in lights[i]):
                return False
        
        return True
    
    def final_combinations(presses):
        # print(presses)
        for g, light in zip(goal, lights):
            if g != sum(presses[l] for l in light):
                print("happens")
                return False
        
        return True

    if all(actual_presses):
        return sum(actual_presses)
    
    possibilities = [list(range(r[0], r[1] + 1)) for r in find_min_ranges()]
    # print(possibilities)
    combinations = sorted(generate_combinations(possibilities), key=lambda c: sum(c))
    # print(len(combinations))
    # pprint(combinations)
    minimum = sum(next(c for c in combinations if final_combinations(c)))
    # print(filtered)
    return minimum
    print(actual_presses)
    return 0
    
    def update_range(info):
        _, presses_light, actual_presses, lights = info
        presses_button = [(p, p) for p in actual_presses]

        for p, presses in enumerate(presses_button):
            if presses == (None, None):
                presses_button[p] = (0, )

        for l, light in enumerate(lights):
            total = sum(p[1] for p in light)
            # for 
            if len(light) == 2:
                f, s = light
                first, second = presses_button[f], presses_button[s]
                missing_presses = goal[l] - actual_presses[l] if actual_presses[l] != None else goal[l]
                presses_button[f] = (missing_presses - second[1], first[1])
                presses_button[s] = (missing_presses - first[1], second[1])
        
        return [presses_button, presses_light, actual_presses, lights]
    
    pprint(info)
    new_info = find_easy_presses(info)
    while info != new_info and not all(actual_presses):
        info = new_info
        new_info = find_easy_presses(info)
    
    if all(actual_presses):
        return sum(actual_presses)
    
    info = update_min_range(info)

    if all(actual_presses):
        return sum(actual_presses)

    presses_button, presses_light, actual_presses, lights = info
    bruteforce_presses = [list(range(presses[0], presses[1] + 1)) for presses in presses_button]

    return find_joltage_combinations(machine, [bruteforce_presses, actual_presses, lights])

    recursion(info)    

def find_no_new_joltage_combinations(machine):
    _, buttons, goal = machine

    presses_light = goal.copy()
    presses_button = [(0, min([goal[light] for light in button])) for button in buttons]
    actual_presses = [None for _ in goal]
    lights = [[b for b, button in enumerate(buttons) if l in button] for l in range(len(goal))]
    info = [presses_button, presses_light, actual_presses, lights]

    def update(index, info):
        print(1, info)
        presses_button, presses_light, actual_presses, lights = info
        light = lights[index][0]

        presses = presses_button[light][1]
        presses_button[light] = (presses, presses)
        actual_presses[light] = presses

        button = buttons[light]
        print(buttons)
        for other in button:
            print(other)
            presses_light[other] -= presses        

        # for button in presses_button:

        # presses_button = [(0, min([goal[light] for light in button if len(button) > 0 else 0])) for button in buttons]
        
        buttons[light] = []
        for light in lights:
            light = light.remove(button) if button in light else light

        print(2, [presses_button, presses_light, actual_presses, lights])
        return [presses_button, presses_light, actual_presses, lights]

    def find_easy_presses(info):
        presses_button, presses_light, actual_presses, lights = info

        for l, light in enumerate(lights):
            if len(light) == 1:
                info = update(l, info)
                presses_button, presses_light, actual_presses, lights = info
        
        for p, presses in enumerate(presses_button):
            if presses[0] == presses[1] and actual_presses[p] == None:
                info = update(p, info)
                presses_button, presses_light, actual_presses, lights = info
        
        return info
    
    def update_range(info):
        _, presses_light, actual_presses, lights = info
        presses_button = [(p, p) for p in actual_presses]

        for p, presses in enumerate(presses_button):
            if presses == (None, None):
                presses_button[p] = (0, )

        for l, light in enumerate(lights):
            total = sum(p[1] for p in light)
            # for 
            if len(light) == 2:
                f, s = light
                first, second = presses_button[f], presses_button[s]
                missing_presses = goal[l] - actual_presses[l] if actual_presses[l] != None else goal[l]
                presses_button[f] = (missing_presses - second[1], first[1])
                presses_button[s] = (missing_presses - first[1], second[1])
        
        return [presses_button, presses_light, actual_presses, lights]
    
    pprint(info)
    new_info = find_easy_presses(info)
    while info != new_info and not all(actual_presses):
        info = new_info
        new_info = find_easy_presses(info)
    
    if all(actual_presses):
        return sum(actual_presses)
    
    info = update_min_range(info)

    if all(actual_presses):
        return sum(actual_presses)

    presses_button, presses_light, actual_presses, lights = info
    bruteforce_presses = [list(range(presses[0], presses[1] + 1)) for presses in presses_button]

    return find_joltage_combinations(machine, [bruteforce_presses, actual_presses, lights])

    recursion(info)    

def find_joltage_combinations(machine, info):
    possible_presses, _, lights = info
    _, buttons, goal = machine

    # possible_presses = [list(range(0, min([goal[light] for light in buttons[i]]) + 1)) for i in range(len(buttons))]
    # lights = [[b for b, button in enumerate(buttons) if l in button] for l in range(len(goal))]
    
    def filter_combinations(presses):
        # print("p", presses)
        for i in range(len(goal)):
            if max(lights[i]) < len(presses) and goal[i] != sum(presses[l] for l in lights[i]):
                return False
            # print(goal, i)
            
            if goal[i] < sum(presses[l] if l < len(presses) else 0 for l in lights[i]):
                return False
        
        return True

    def final_combinations(presses):
        # print(presses)
        for g, light in zip(goal, lights):
            if g != sum(presses[l] for l in light):
                print("happens")
                return False
        
        return True
    
    def generate_combinations(possible_presses):
        possible_presses = [tuple(p) for p in possible_presses]

        combinations = [[]]        
        for press in possible_presses:
            combinations = [x + [y] for x in combinations for y in press if filter_combinations(x + [y])]            
        
        combinations = [combination for combination in combinations if sum([c * len(b) for c, b in zip(combination, buttons)]) == sum(goal)]

        return combinations
            
    
    # print(possible_presses, lights)
    # total_presses = [[p for p in range(0, presses)] for presses in max_presses]
    # print(list(product(*possible_presses)))
    # combinations = starmap(filter_combinations, product(possible_presses))
    # combinations = (presses for presses in list(product(*possible_presses)) if filter_combinations(presses))
    combinations = sorted(generate_combinations(possible_presses), key=lambda c: sum(c))
    print(len(combinations))
    # pprint(combinations)
    minimum = sum(next(c for c in combinations if final_combinations(c)))
    # print(filtered)
    return minimum
    all_options.sort(key=lambda o: sum(o))
    for presses in all_options:
        # lights = [first + second for first, second in [button * press for button, press in zip(buttons, presses)]]
        lights = [int(p) for p in sum([button[press] for button, press in zip(buttons, presses)])]

        if lights == goal:
            return sum(presses)

def find_joltage_two_combination(machine):
    _, index_buttons, goal = machine

    joltages = np.array([0 for _ in goal])
    buttons = [np.array([1 if i in button else 0 for i in range(len(joltages))]) for button in index_buttons]
    possible_presses = [[buttons[i] * p for p in range(0, min([goal[light] for light in index_buttons[i]]) + 1)] for i in range(len(index_buttons))]

    print(possible_presses)
    # total_presses = [[p for p in range(0, presses)] for presses in max_presses]

    all_options = list(filter(lambda o: sum([max(option) for option in o]) > min(goal), product(*possible_presses)))
    all_options.sort(key=lambda o: sum(o))
    for presses in all_options:
        # lights = [first + second for first, second in [button * press for button, press in zip(buttons, presses)]]
        lights = [int(p) for p in sum([button[press] for button, press in zip(buttons, presses)])]

        if lights == goal:
            return sum(presses)

def find_lowest_combination(count, min_count, presses, machine):
    _, buttons, joltages = machine

    if count >= min_count:
        return min_count
    
    if presses == joltages:
        return count

    if any([press for press, joltage in zip(presses, joltages) if press > joltage]):
        return min_count
    
    for button in buttons:
        current_presses = presses.copy()
        
        for light in button:
            current_presses[light] += 1

        min_count = find_lowest_combination(count + 1, min_count, current_presses, machine)
    
    return min_count

    while _:
        len_sequence += 1

        for combination in comb(buttons, len_sequence):
            presses = list(chain.from_iterable(combination))
            lights = [presses.count(i) % 2 for i in range(len(goal))]

            if lights == goal:
                return [len_sequence, presses]

def third(machine):
    goal, buttons, costs = machine
    
    energy = sum([press * cost for press, cost in zip(presses, costs)])
    if energy >= min_energy:
        return min_energy
    
    lights = [press % 2 for press in presses]
    if lights == goal:
        return energy

    for button in buttons:
        current_presses = presses.copy()
        for light in button:
            current_presses[light] += 1
            min_energy = find_lowest_combination(min_energy, current_presses, machine)
    
    return min_energy

    lights = []
    for i in range(len(goal)):
        if presses.count(i) % 2 == 1:
            lights.append(i)
    
    if goal == lights:
        return True

    return False

def first(input):
    total = 0

    for machine in input:
        total += find_first_combination(machine)
    
    return total

def test():
    machine = preprocess('[.##...##.] (1,3,6) (0,2,6,7,8) (0,5,7,8) (2,5,7) (3,4,5,6,7,8) (0,1,2,3,5,6,7) (1,2,3,4,6) (2,3,4,5) (0,1,3,5,6,7,8) {34,37,37,191,163,206,188,203,180}')
    print(machine)
    _, buttons, goal = machine[0]
    print(buttons, goal)
    print(brute_force2(buttons, goal))

def second(input):
    # test()
    # return 0
    total = []
    i = 1


    for machine in input:
        print('\n', i, "of", len(input), ":", machine)
        # total += find_joltage_combination(machine)
        total.append(gaussian_elimination(machine))
        # total += find_new_joltage_combinations(machine)
        # total += find_lowest_combination(0, float('inf'), [0 for _ in machine[0]], machine)
        i += 1
    
    pprint([f'{i}: {t}' for i, t in enumerate(total)])
    return sum(t if t != None else 0 for t in total)

if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__))

    example = Path(path + '/example.txt').read_text()
    input = Path(path + '/input.txt').read_text()

    second_part = True
    debugging = not True
    low = []
    high = []
    unknown = []

    def string_format(part, example, input, prev_answers):
        print(f"{str('Part ' + part + ' - Example input').ljust(25)} {str('('+ str(example[0]) + ')').rjust(15)}: {example[1]}")

        if not debugging:
            low, high, unknown = prev_answers
            final_answer = input[0] is not None

            print(f"{str('Part ' + part + ' - Too low').ljust(41)}: {max(low)}") if low and not final_answer else False
            [print(f"{str('Part ' + part + ' - Wrong answer').ljust(41)}: {u}") for u in unknown] if unknown and not final_answer else False

            print(f"{str('Part ' + part + ' - Actual input').ljust(25)} {str('('+ str(input[0]) + ')').rjust(15)}: {input[1]}") if final_answer \
                else print(f"{str('Part ' + part + ' - Actual input').ljust(41)}: {input[1]}") 

            print(f"{str('Part ' + part + ' - Too high').ljust(41)}: {min(high)}") if high and not final_answer else False
            print("\n")

    f_example = [7, first(preprocess(example))]
    f_input = [None, None]
    if not debugging:
        start = timeit.default_timer()
        f_input = [538, first(preprocess(input))]
        print(f"Time taken: {timeit.default_timer()-start}s")
    string_format(part='1', example=f_example, input=f_input, prev_answers=[low, high, unknown])

    if second_part:
        # s_example = [33, second(preprocess(example))]
        s_input = [None, None]
        if not debugging:
            start = timeit.default_timer()
            s_input = [None, second(preprocess(input))]
            print(f"Time taken: {timeit.default_timer()-start}s")
        string_format(part='2', example=s_example, input=s_input, prev_answers=[low, high, unknown])
