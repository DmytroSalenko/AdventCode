# --- Day 2: 1202 Program Alarm Part Two---
from intcode_computer import IntcodeComputer, parse_program

DESIRED_RESULT = 19690720


def run_the_magic_program(input_sequence, noun, verb):
    # create a copy of input_sequence to make sure we don't change the
    # original one
    input_sequence_copy = input_sequence.copy()
    input_sequence_copy[1] = noun
    input_sequence_copy[2] = verb

    command_invoker = IntcodeComputer(program=input_sequence_copy)
    command_invoker.run_program()
    return command_invoker.get_memory_state()[0]


def solution(input_sequence, desired_result=DESIRED_RESULT):
    for noun in range(100):
        for verb in range(100):
            program_result = run_the_magic_program(input_sequence, noun, verb)

            if program_result == desired_result:
                return (100 * noun) + verb
    # if we reach this point then we haven't found the solution
    raise Exception("The solutions hasn't been found")


if __name__ == '__main__':
    input_file = '../inputs/task_2_part_2_input.txt'
    num_sequence = parse_program(input_file)
    result = solution(num_sequence)
    print(result)

