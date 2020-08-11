import math

INPUT_FILE = './inputs/task_1_input.txt'


def calculate_fuel(mass, divisor=3, subtrahend=2):
    """
    Calculate the fuel required based on the mass input
    :param mass: mass input
    :param divisor: divisor as a part of the equation, equals to 3 by default
    :param subtrahend: subtrahend as a part of the equation, equals to 2 by
    default
    :return: calculated amount of fuel
    """
    numeric_mass = int(mass)
    return math.floor(numeric_mass / divisor) - subtrahend


def solution():
    from pathlib import Path
    input_file = Path(INPUT_FILE)

    fuel_sum = 0
    with open(input_file, 'r') as puzzle_input:
        for line in puzzle_input:
            fuel_sum += calculate_fuel(line)
    return fuel_sum


if __name__ == '__main__':
    import os
    os.chdir('..')

    print(solution())
