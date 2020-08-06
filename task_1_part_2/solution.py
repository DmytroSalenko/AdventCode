# --- Day 1 Part Two ---
from task_1 import calculate_fuel


def calculate_additional_fuel(initial_fuel):
    """
    Recursively calculate the amount of fuel required to carry the fuel.
    Of course it could be done without the recursion
    but I have decided to show off
    :param initial_fuel: the amount of fuel needed to carry
    :return: the amount of fuel needed for carrying the initial fuel tank
    """
    additional_fuel = calculate_fuel(initial_fuel)
    if additional_fuel <= 0:
        return 0
    else:
        return additional_fuel + calculate_additional_fuel(additional_fuel)


def solution(puzzle_input_file):
    fuel_sum = 0
    with open(puzzle_input_file, 'r') as puzzle_input:
        for line in puzzle_input:
            payload_fuel = calculate_fuel(line)
            fuel_for_fuel = calculate_additional_fuel(payload_fuel)

            fuel_sum += (payload_fuel + fuel_for_fuel)

    return fuel_sum


if __name__ == '__main__':
    input_file = '../task_1/task_1_input.txt'
    print(solution(input_file))

