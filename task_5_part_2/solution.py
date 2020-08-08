from task_2 import parse_sequence
from task_5 import ExtendedComputer


def solution(input_file_name):
    # parse the sequence of commands and replace two elements with values
    # according to the task
    num_sequence = parse_sequence(input_file_name)
    computer = ExtendedComputer(memory=num_sequence)
    # set the input value that we want to pass to the Input command
    computer.input_buffer.put_data(5)
    computer.run_program()
    return computer.output_buffer.buffer[-1]


if __name__ == '__main__':
    input_file = '../task_5_part_2/task_5_part_2_input.txt'
    puzzle_result = solution(input_file)
    print(puzzle_result)