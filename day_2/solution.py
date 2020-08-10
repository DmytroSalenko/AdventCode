# --- Day 2: 1202 Program Alarm ---
from intcode_computer import IntcodeComputer, parse_program


def solution(input_file_name):
    # parse the sequence of commands and replace two elements with values
    # according to the task
    program = parse_program(input_file_name)
    program[1] = 12
    program[2] = 2
    # do the calculation
    computer = IntcodeComputer(program=program)
    computer.run_program()
    result = computer.get_memory_state()
    return result[0]


if __name__ == '__main__':
    input_file = 'task_2_input.txt'
    puzzle_result = solution(input_file)
    print(puzzle_result)
