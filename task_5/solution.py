# --- Day 5: Sunny with a Chance of Asteroids ---
from enum import Enum
import abc
import inspect

from task_2 import Command, CommandProducer, Computer, parse_sequence


class OpCodeExtended(Enum):
    """Additional set of instructions for the OpCode class"""
    ADD = 1
    MULT = 2
    INPUT = 3
    OUTPUT = 4
    TERM = 99


class ParameterModes(Enum):
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
        """This property returns either sel.value as the number or the value
         stored in the memory at address of `value` depending on the
         parameter mode"""
        if self._mode == ParameterModes.POSITION.value:
            return self._memory[self._value]
        elif self._mode == ParameterModes.IMMEDIATE.value:
            return self._value
        else:
            return None

    def __init__(self, memory, value, mode):
        self._value = value
        self._memory = memory
        self._mode = mode


class ExtendedCommand(Command):
    # default number of command parameters
    COMMAND_LENGTH = 4

    def __init__(self, extended_opcode, param_1_value, param_2_value,
                 result_addr, memory):
        # if only opcode is given, fill the string with leading zeroes to the
        # size of command + 1 since opcode takes 2 digits
        opcode_string = f'%0{self.COMMAND_LENGTH + 1}d' % extended_opcode
        op_code = int(opcode_string[-2:])
        if param_1_value is not None:
            param_1_mode = int(opcode_string[-3])
            param_1 = CommandParameter(memory, param_1_value, param_1_mode)
        else:
            param_1 = None

        if param_1_value is not None:
            param_2_mode = int(opcode_string[-4])
            param_2 = CommandParameter(memory, param_2_value, param_2_mode)
        else:
            param_2 = None

        super().__init__(op_code, param_1, param_2, result_addr, memory)

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass


class ExtendedAddCommand(ExtendedCommand):
    def execute(self, *args, **kwargs):
        first_addend = self.param_1.value
        second_addend = self.param_2.value
        result = first_addend + second_addend

        self.memory[self.result_addr] = result


class ExtendedMultCommand(ExtendedCommand):
    def execute(self, *args, **kwargs):
        first_factor = self.param_1.value
        second_factor = self.param_2.value
        result = first_factor * second_factor

        self.memory[self.result_addr] = result


class InputCommand(ExtendedCommand):
    COMMAND_LENGTH = 2

    def __init__(self, extended_opcode, store_addr, memory, input_buffer):
        self.input_buffer = input_buffer
        self.store_address = store_addr

        super().__init__(extended_opcode,
                         param_1_value=None,
                         param_2_value=None,
                         memory=memory,
                         result_addr=None)

    def execute(self, *args, **kwargs):
        self.memory[self.store_address] = self.input_buffer.value


class OutputCommand(ExtendedCommand):
    COMMAND_LENGTH = 2

    def __init__(self, extended_opcode, value_addr, memory, output_buffer):
        self.output_buffer = output_buffer
        self.value_addr = value_addr

        super().__init__(extended_opcode,
                         param_1_value=None,
                         param_2_value=None,
                         memory=memory,
                         result_addr=None)

    def execute(self, *args, **kwargs):
        self.output_buffer.value = self.memory[self.value_addr]


class ExtendedCommandProducer(CommandProducer):
    COMMAND_MAPPING = {
        OpCodeExtended.ADD.value: ExtendedAddCommand,
        OpCodeExtended.MULT.value: ExtendedMultCommand,
        OpCodeExtended.INPUT.value: InputCommand,
        OpCodeExtended.OUTPUT.value: OutputCommand
    }

    def __init__(self, memory, input_buffer, output_buffer):
        self.input_buffer = input_buffer
        self.output_buffer = output_buffer
        self.command_pointer = 0
        super().__init__(memory)

    def _get_next_command(self):
        while True:
            op_code = int(str(self.memory[self.command_pointer])[-2:])
            if op_code == OpCodeExtended.TERM.value:
                return op_code,

            command_length = self.COMMAND_MAPPING[op_code].COMMAND_LENGTH
            yield tuple(self.memory[
                  self.command_pointer:self.command_pointer + command_length
                  ])
            self.command_pointer += command_length

    def command_generator(self):
        for command_parameters in self._get_next_command():
            op_code = int(str(command_parameters[0])[-2:])
            if op_code == OpCodeExtended.TERM.value:
                return
            else:
                command_class = self.COMMAND_MAPPING[op_code]

                arglist = inspect.getfullargspec(command_class.__init__)
                buffer_args = {}
                if 'input_buffer' in arglist.args:
                    buffer_args['input_buffer'] = self.input_buffer
                if 'output_buffer' in arglist.args:
                    buffer_args['output_buffer'] = self.output_buffer

                yield command_class(*command_parameters,
                                    self.memory,
                                    **buffer_args)


class ExtendedComputer(Computer):
    @property
    def input_buffer(self):
        return self._input_buffer.value

    @input_buffer.setter
    def input_buffer(self, value):
        self._input_buffer.value = value

    @property
    def output_buffer(self):
        return self._output_buffer.value

    def __init__(self, memory, input_buffer=None, output_buffer=None):
        super().__init__(memory)
        self._output_buffer = OutputBuffer(output_buffer)
        self._input_buffer = InputBuffer(input_buffer)
        self.command_producer = ExtendedCommandProducer(memory,
                                                        self._input_buffer,
                                                        self._output_buffer)

    def run_program(self):
        for command in self.command_producer.command_generator():
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



