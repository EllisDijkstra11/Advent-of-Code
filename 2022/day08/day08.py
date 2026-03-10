from pathlib import Path
import string
from tokenize import String

def preprocess(input_lines: list[int]):
    all_trees = input_lines.split("\n")
    return all_trees


def tree_visible_edge(all_trees, x, y):
    #print("\n", x, y, all_trees[x], all_trees)
    number_horizontal = len(all_trees)
    number_vertical = len(all_trees[0])

    if x == 0 or y == 0 or x == number_vertical - 1 or y == number_horizontal - 1:
        return True

    number_horizontal = len(all_trees)
    number_vertical = len(all_trees[0])
    if tree_visible_row_edge(0, x, x, y, all_trees) or tree_visible_row_edge(x + 1, number_horizontal, x, y, all_trees):
        return True
    
    if tree_visible_column_edge(0, y, x, y, all_trees) or tree_visible_column_edge(y + 1, number_horizontal, x, y, all_trees):
        return True

    return False


def tree_visible_row_edge(x_low, x_high, x, y, all_trees):
    for index in range(x_low, x_high):
        tree = int(all_trees[y][x])
        other_tree = int(all_trees[y][index])
        if tree <= other_tree:
            return False

    return True


def tree_visible_column_edge(y_low, y_high, x, y, all_trees):
    for index in range(y_low, y_high):
        tree = int(all_trees[y][x])
        other_tree = int(all_trees[index][x])
        if int(all_trees[index][x]) >= int(all_trees[y][x]):
            return False
    return True      


def first(all_trees):
    trees_visible = 0
    number_horizontal = len(all_trees)
    number_vertical = len(all_trees[0])

    x = 0
    y = 0
    while y < number_vertical:
        while x < number_horizontal:
            if tree_visible_edge(all_trees, x, y):
                trees_visible += 1
            x += 1
        x = 0
        y += 1
    return trees_visible

def tree_visible_row(first_x, second_x, step_size, x, y, all_trees):
    visible_trees = 0
    highest_tree = 0
    for index in range(first_x, second_x, step_size):
        tree = int(all_trees[y][x])
        other_tree = int(all_trees[y][index])
        visible_trees += 1
        if other_tree >= tree:
            return visible_trees
        highest_tree = other_tree
    return visible_trees


def tree_visible_column(first_y, second_y, step_size, x, y, all_trees):
    visible_trees = 0
    highest_tree = 0
    for index in range(first_y, second_y, step_size):
        tree = int(all_trees[y][x])
        other_tree = int(all_trees[index][x])
        visible_trees += 1
        if other_tree >= tree:
            return visible_trees
        highest_tree = other_tree
    return visible_trees


def tree_visible_hut(all_trees, x, y):
    #print("\n", x, y, all_trees[x], all_trees)
    number_horizontal = len(all_trees)
    number_vertical = len(all_trees[0])

    if x == 0 or y == 0 or x == number_vertical - 1 or y == number_horizontal - 1:
        return 0

    first_trees_visible = tree_visible_row(x - 1, -1, -1, x, y, all_trees)
    second_trees_visible = tree_visible_row(x + 1, number_horizontal, 1, x, y, all_trees)
    third_trees_visible = tree_visible_column(y - 1, -1, -1, x, y, all_trees)
    fourth_trees_visible = tree_visible_column(y + 1, number_horizontal, 1, x, y, all_trees)
   
    print([x, y], first_trees_visible, second_trees_visible, third_trees_visible, fourth_trees_visible)
    if 0 in (first_trees_visible, second_trees_visible, third_trees_visible, fourth_trees_visible):
        return 0

    return first_trees_visible * second_trees_visible * third_trees_visible * fourth_trees_visible

def second(all_trees):
    scenic_score = 0
    highest_scenic_score = 0
    number_horizontal = len(all_trees)
    number_vertical = len(all_trees[0])

    x = 0
    y = 0
    while y < number_vertical:
        while x < number_horizontal:
            scenic_score = tree_visible_hut(all_trees, x, y)
            if scenic_score > highest_scenic_score:
                highest_scenic_score = scenic_score
            x += 1
        x = 0
        y += 1
    return highest_scenic_score

if __name__ == "__main__":
    data_path_example = Path('2022/day08/example.txt')
    data_path_input = Path('2022/day08/input.txt')
    example_data = data_path_example.read_text()
    data = data_path_input.read_text()
    print(first(preprocess(example_data)))
    print(first(preprocess(data)))
    print(second(preprocess(example_data)))
    print(second(preprocess(data)))
    