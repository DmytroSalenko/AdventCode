# --- Day 1: The Tyranny of the Rocket Equation ---
import math


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


def solution(puzzle_input_file):
    fuel_sum = 0
    with open(puzzle_input_file, 'r') as puzzle_input:
        for line in puzzle_input:
            fuel_sum += calculate_fuel(line)
    return fuel_sum


if __name__ == '__main__':
    input_file = 'task_1_input.txt'
    print(solution(input_file))
