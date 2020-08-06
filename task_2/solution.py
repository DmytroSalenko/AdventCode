# --- Day 2: 1202 Program Alarm ---
from enum import Enum
import abc


class OpCode(Enum):
    """Enum with opcode number to avoid using literals"""
    ADD = 1
    MULT = 2
    TERM = 99


class Command(metaclass=abc.ABCMeta):
    def __init__(self, opcode, addr_1, addr_2, result_addr):
        self.opcode = opcode
        self.addr_1 = addr_1
        self.addr_2 = addr_2
        self.result_addr = result_addr

    @abc.abstractmethod
    def execute(self, sequence):
        pass


class AddCommand(Command):
    """Implementation of the addition command"""
    def execute(self, sequence):
        first_addend = sequence[self.addr_1]
        second_addend = sequence[self.addr_2]
        result = first_addend + second_addend

        sequence[self.result_addr] = result


class MultCommand(Command):
    """Implementation of the multiplication command"""
    def execute(self, sequence):
        first_addend = sequence[self.addr_1]
        second_addend = sequence[self.addr_2]
        result = first_addend * second_addend

        sequence[self.result_addr] = result


class CommandProducer:
    def __init__(self, sequence):
        self.sequence = sequence

    def _chunks(self, n=4):
        """Yield successive n-sized chunks from self.sequence."""
        for i in range(0, len(self.sequence), n):
            result = self.sequence[i:i + n]
            yield *tuple(result),

    def produce_commands(self):
        """Generate a list of command objects depending of the command code of
        each"""
        for (opcode, addr_1, addr_2, results_addr) in self._chunks():
            if opcode == OpCode.ADD.value:
                yield AddCommand(opcode, addr_1, addr_2, results_addr)
            elif opcode == OpCode.MULT.value:
                yield MultCommand(opcode, addr_1, addr_2, results_addr)
            elif opcode == OpCode.TERM.value:
                return


class CommandInvoker:
    """
    Basically, this is the implementation of the Command design pattern.
    The object of this class is responsible for creating of the command list and
    executing each command
    """
    def __init__(self, sequence):
        self.sequence = sequence
        self.command_producer = CommandProducer(sequence)
        self.commands = []

    def generate_commands(self):
        for command in self.command_producer.produce_commands():
            self.commands.append(command)

    def execute_commands(self):
        for command in self.commands:
            command.execute(self.sequence)

    def get_result_sequence(self):
        return self.sequence


def parse_sequence(puzzle_input_file):
    """Parse the list of values from the input file"""
    sequence = []
    with open(puzzle_input_file, 'r') as puzzle_input:
        for line in puzzle_input:
            sequence.extend([int(x) for x in line.split(',')])
    return sequence


def solution(input_file_name):
    # parse the sequence of commands and replace two elements with values
    # according to the task
    num_sequence = parse_sequence(input_file)
    num_sequence[1] = 12
    num_sequence[2] = 2
    # do the calculation
    command_invoker = CommandInvoker(sequence=num_sequence)
    command_invoker.generate_commands()
    command_invoker.execute_commands()
    result = command_invoker.get_result_sequence()
    return result[0]


if __name__ == '__main__':
    input_file = 'task_2_input.txt'
    puzzle_result = solution(input_file)
    print(puzzle_result)
