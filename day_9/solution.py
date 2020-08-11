from intcode_computer import IntcodeComputer, parse_program

INPUT_FILE = './inputs/task_9_input.txt'


def solution():
    from pathlib import Path
    input_file = Path(INPUT_FILE)

    # parse the sequence of commands and put the value as the computer input
    num_sequence = parse_program(input_file)
    computer = IntcodeComputer(program=num_sequence)
    computer.send_input_data(1)
    # set the input value that we want to pass to the Input command
    computer.run_program()
    return computer.output_buffer.value


if __name__ == '__main__':
    import os
    os.chdir('..')

    print(solution())
