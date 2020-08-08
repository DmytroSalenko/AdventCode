# --- Day 5: Sunny with a Chance of Asteroids ---
from enum import Enum, unique
import abc

from task_2 import Command, Computer, parse_sequence


@unique
class OpCodeExtended(Enum):
    """Additional set of instructions for the OpCode class"""
    ADD = 1
    MULT = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    TERM = 99


class ParameterModes(Enum):
    """Thus Enum contains different modes for the Command object parameters"""
    POSITION = 0
    IMMEDIATE = 1


class Buffer(metaclass=abc.ABCMeta):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __init__(self, value=None):
        self._value = value


class InputBuffer(Buffer):
    pass


class OutputBuffer(Buffer):
    pass


class CommandParameter:
    """The objects of this class are intended to be stored in the Command
    object as the command arguments and utilized in the execute() method"""
    @property
    def value(self):
        """This property returns either self.value as the number or the value
         stored in the memory at address of `value` depending on the
         parameter mode"""
        if self._mode == ParameterModes.POSITION.value:
            return self._memory[self._value]
        elif self._mode == ParameterModes.IMMEDIATE.value:
            return self._value
        else:
            raise ValueError('Unknown argument mode')

    def __init__(self, memory, value, mode):
        self._value = value
        self._memory = memory
        self._mode = mode


class ExtendedCommand(Command):
    """Extension for the Command class. Supports argument modes"""
    # default number of command parameters
    COMMAND_LENGTH = 4

    def __init__(self, delegate, extended_opcode, param_1_value, param_2_value,
                 result_addr):
        self.delegate = delegate
        # if only opcode is given, fill the string with leading zeroes to the
        # size of command + 1 since opcode takes 2 digits
        opcode_string = f'%0{self.COMMAND_LENGTH + 1}d' % extended_opcode
        op_code = int(opcode_string[-2:])
        if param_1_value is not None:
            param_1_mode = int(opcode_string[-3])
            param_1 = CommandParameter(self.delegate.memory, param_1_value,
                                       param_1_mode)
        else:
            param_1 = None

        if param_1_value is not None:
            param_2_mode = int(opcode_string[-4])
            param_2 = CommandParameter(self.delegate.memory, param_2_value,
                                       param_2_mode)
        else:
            param_2 = None
        super().__init__(op_code, param_1, param_2, result_addr, None)

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass


class ExtendedAddCommand(ExtendedCommand):
    def execute(self, *args, **kwargs):
        first_addend = self.param_1.value
        second_addend = self.param_2.value
        result = first_addend + second_addend
        # store the result in Computer memory
        self.delegate.memory[self.result_addr] = result


class ExtendedMultCommand(ExtendedCommand):
    def execute(self, *args, **kwargs):
        first_factor = self.param_1.value
        second_factor = self.param_2.value
        result = first_factor * second_factor
        # store the result in Computer memory
        self.delegate.memory[self.result_addr] = result


class InputCommand(ExtendedCommand):
    COMMAND_LENGTH = 2

    def __init__(self, delegate, extended_opcode, result_addr):
        super().__init__(delegate,
                         extended_opcode,
                         param_1_value=None,
                         param_2_value=None,
                         result_addr=result_addr)

    def execute(self, *args, **kwargs):
        self.delegate.memory[self.result_addr] = self.delegate.input_buffer


class OutputCommand(ExtendedCommand):
    COMMAND_LENGTH = 2

    def __init__(self, delegate, extended_opcode, result_addr):
        super().__init__(delegate,
                         extended_opcode,
                         param_1_value=None,
                         param_2_value=None,
                         result_addr=result_addr)

    def execute(self, *args, **kwargs):
        self.delegate.output_buffer = self.delegate.memory[self.result_addr]


# ---- Command classes for the Part 2 of the task ------
class JumpIfTrueCommand(ExtendedCommand):
    COMMAND_LENGTH = 3

    def __init__(self, delegate, extended_opcode, param_1_value, param_2_value):
        super().__init__(delegate,
                         extended_opcode,
                         param_1_value,
                         param_2_value,
                         result_addr=None)

    def execute(self,  *args, **kwargs):
        if self.param_1.value != 0:
            self.delegate.command_pointer = self.param_2.value


class JumpIfFalseCommand(JumpIfTrueCommand):
    COMMAND_LENGTH = 3

    def execute(self, *args, **kwargs):
        if self.param_1.value == 0:
            self.delegate.command_pointer = self.param_2.value


class LessThanCommand(ExtendedCommand):
    def execute(self, *args, **kwargs):
        if self.param_1.value < self.param_2.value:
            self.delegate.memory[self.result_addr] = 1
        else:
            self.delegate.memory[self.result_addr] = 0


class EqualsCommand(ExtendedCommand):
    def execute(self, *args, **kwargs):
        if self.param_1.value == self.param_2.value:
            self.delegate.memory[self.result_addr] = 1
        else:
            self.delegate.memory[self.result_addr] = 0


class ExtendedComputer(Computer):
    COMMAND_MAPPING = {
        OpCodeExtended.ADD.value: ExtendedAddCommand,
        OpCodeExtended.MULT.value: ExtendedMultCommand,
        OpCodeExtended.INPUT.value: InputCommand,
        OpCodeExtended.OUTPUT.value: OutputCommand,
        OpCodeExtended.JUMP_IF_FALSE.value: JumpIfFalseCommand,
        OpCodeExtended.JUMP_IF_TRUE.value: JumpIfTrueCommand,
        OpCodeExtended.LESS_THAN.value: LessThanCommand,
        OpCodeExtended.EQUALS.value: EqualsCommand
    }

    @property
    def input_buffer(self):
        return self._input_buffer.value

    @input_buffer.setter
    def input_buffer(self, value):
        self._input_buffer.value = value

    @property
    def output_buffer(self):
        return self._output_buffer.value

    @output_buffer.setter
    def output_buffer(self, value):
        self._output_buffer.value = value

    @property
    def command_pointer(self):
        return self._command_pointer

    @command_pointer.setter
    def command_pointer(self, value):
        self._command_pointer = value

    def __init__(self, memory, input_buffer=None, output_buffer=None):
        super().__init__(memory)
        self._command_pointer = 0
        self._output_buffer = OutputBuffer(output_buffer)
        self._input_buffer = InputBuffer(input_buffer)

    def _get_next_command(self):
        """
        Generator method to return the required number of arguments for the
        command at self.command_pointer
        :return: op_code if op_code == 99 to indicate the end of program,
        otherwise will return arguments
        """
        while True:
            op_code = int(str(self.memory[self.command_pointer])[-2:])
            if op_code == OpCodeExtended.TERM.value:
                # return op_code if the op_code denotes the end of program
                return op_code,

            command_pointer_stored_value = self.command_pointer

            # get the required number of arguments based on the op_code
            command_length = self.COMMAND_MAPPING[op_code].COMMAND_LENGTH
            yield tuple(self.memory[
                  self.command_pointer:self.command_pointer + command_length
                  ])

            # Check if the command_pointer hasn't been modified by one of the
            # JUMP commands
            if self.command_pointer == command_pointer_stored_value:
                self.command_pointer += command_length

    def command_generator(self):
        """
        Generator method to return a Command object for the execution based
        on op_code and arguments returned by _get_next_command() method
        """
        for command_parameters in self._get_next_command():
            op_code = int(str(command_parameters[0])[-2:])
            if op_code == OpCodeExtended.TERM.value:
                # stop execution if the op_code denotes the end of program
                return
            else:
                command_class = self.COMMAND_MAPPING[op_code]
                yield command_class(self, *command_parameters)

    def run_program(self):
        """
        Subsequently execute commands from the self.memory
        """
        for command in self.command_generator():
            command.execute()


def solution(input_file_name):
    # parse the sequence of commands and replace two elements with values
    # according to the task
    num_sequence = parse_sequence(input_file_name)
    computer = ExtendedComputer(memory=num_sequence)
    # set the input value that we want to pass to the Input command
    computer.input_buffer = 1
    computer.run_program()
    return computer.output_buffer


if __name__ == '__main__':
    input_file = '../task_5/task_5_input.txt'
    puzzle_result = solution(input_file)
    print(puzzle_result)



