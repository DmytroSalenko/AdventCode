# --- Day 2: 1202 Program Alarm ---
from enum import Enum
import abc


class OpCode(Enum):
    """Enum with opcode number to avoid using literals"""
    ADD = 1
    MULT = 2
    TERM = 99


class Command(metaclass=abc.ABCMeta):
    def __init__(self, opcode, param_1, param_2, result_addr, memory):
        self.opcode = opcode
        self.param_1 = param_1
        self.param_2 = param_2
        self.result_addr = result_addr
        self.memory = memory

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass


class AddCommand(Command):
    """Implementation of the addition command"""

    COMMAND_LENGTH = 4

    def execute(self, *args, **kwargs):
        first_addend = self.memory[self.param_1]
        second_addend = self.memory[self.param_2]
        result = first_addend + second_addend

        self.memory[self.result_addr] = result


class MultCommand(Command):
    """Implementation of the multiplication command"""

    COMMAND_LENGTH = 4

    def execute(self, *args, **kwargs):
        first_factor = self.memory[self.param_1]
        second_factor = self.memory[self.param_2]
        result = first_factor * second_factor

        self.memory[self.result_addr] = result


class CommandProducer:
    def __init__(self, memory):
        self.memory = memory

    def _get_next_command(self):
        """Yield successive n-sized chunks from self.sequence."""
        for i in range(0, len(self.memory), 4):
            result = self.memory[i:i + 4]
            yield *tuple(result),

    def command_generator(self):
        """Generate a list of command objects depending of the command code of
        each"""
        for (opcode, addr_1, addr_2, results_addr) in self._get_next_command():
            if opcode == OpCode.ADD.value:
                yield AddCommand(opcode, addr_1, addr_2, results_addr,
                                 self.memory)
            elif opcode == OpCode.MULT.value:
                yield MultCommand(opcode, addr_1, addr_2, results_addr,
                                  self.memory)
            elif opcode == OpCode.TERM.value:
                return


class Computer:
    """
    Basically, this is the implementation of the Command design pattern.
    The object of this class is responsible for creating of the command list and
    executing each command
    """
    def __init__(self, memory):
        self.memory = memory
        self.command_producer = CommandProducer(memory)
        self.commands = []

    def generate_commands(self):
        for command in self.command_producer.command_generator():
            self.commands.append(command)

    def run_program(self):
        for command in self.commands:
            command.execute()

    def get_memory_state(self):
        return self.memory


def parse_program(puzzle_input_file):
    """Parse the list of values from the input file"""
    sequence = []
    with open(puzzle_input_file, 'r') as puzzle_input:
        for line in puzzle_input:
            sequence.extend([int(x) for x in line.split(',')])
    return sequence


def solution(input_file_name):
    # parse the sequence of commands and replace two elements with values
    # according to the task
    program = parse_program(input_file_name)
    program[1] = 12
    program[2] = 2
    # do the calculation
    computer = Computer(memory=program)
    computer.generate_commands()
    computer.run_program()
    result = computer.get_memory_state()
    return result[0]


if __name__ == '__main__':
    input_file = 'task_2_input.txt'
    puzzle_result = solution(input_file)
    print(puzzle_result)
