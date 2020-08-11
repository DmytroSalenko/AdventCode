# --- Day 2: 1202 Program Alarm ---
from intcode_computer import IntcodeComputer, parse_program

INPUT_FILE = './inputs/task_2_input.txt'


def solution():
    from pathlib import Path
    input_file = Path(INPUT_FILE)
    # parse the sequence of commands and replace two elements with values
    # according to the task
    program = parse_program(input_file)
    program[1] = 12
    program[2] = 2
    # do the calculation
    computer = IntcodeComputer(program=program)
    computer.run_program()
    result = computer.get_memory_state()
    return result[0]


if __name__ == '__main__':
    import os
    os.chdir('..')

    print(solution())
