# --- Day 5: Sunny with a Chance of Asteroids ---
from intcode_computer import IntcodeComputer, parse_program


def solution(input_file_name):
    # parse the sequence of commands and replace two elements with values
    # according to the task
    num_sequence = parse_program(input_file_name)
    computer = IntcodeComputer(program=num_sequence)
    # set the input value that we want to pass to the Input command
    computer.send_input_data(1)
    computer.run_program()
    return computer.output_buffer.value


if __name__ == '__main__':
    input_file = '../inputs/task_5_input.txt'
    puzzle_result = solution(input_file)
    print(puzzle_result)



