import abc
from enum import Enum, unique

from intcode_computer.command_parameters import CommandParameter


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
    ADJUST_REL_BASE = 9
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


class ExtendedCommand(Command):
    """Extension for the Command class. Supports argument modes"""
    COMMAND_LENGTH = 4  # default number of command parameters
    OPCODE_LENGTH = 2

    def __init__(self, delegate, extended_opcode, param_1_value, param_2_value,
                 result_addr):
        self.delegate = delegate
        # if only opcode is given, fill the string with leading zeroes to the
        # size of command + 1 since opcode takes 2 digits
        opcode_sting_len = self.COMMAND_LENGTH + self.OPCODE_LENGTH - 1
        opcode_string = f'%0{opcode_sting_len}d' % extended_opcode

        op_code = int(opcode_string[-self.OPCODE_LENGTH:])
        command_param_values = [param_1_value, param_2_value, result_addr]

        param_objects = self._generate_parameter_objects(opcode_string,
                                                         command_param_values)

        super().__init__(op_code, *param_objects, None)

    def _generate_parameter_objects(self, opcode_string, parameters):
        """A function to generate CommandParameter objects from the given
        parameter values and parameter modes"""
        param_mode_list = list(opcode_string[:-self.OPCODE_LENGTH])
        param_mode_list.reverse()
        param_mode_iterator = iter(param_mode_list)

        param_objects = []

        for param_value in parameters:
            if param_value is not None:
                mode = next(param_mode_iterator)
                param_objects.append(
                    CommandParameter(self.delegate,
                                     param_value,
                                     int(mode))
                )
            else:
                param_objects.append(None)

        return param_objects

    @abc.abstractmethod
    def execute(self, *args, **kwargs):
        pass


class AddCommand(ExtendedCommand):
    def execute(self, *args, **kwargs):
        first_addend = self.param_1.value
        second_addend = self.param_2.value
        result = first_addend + second_addend
        # store the result in Computer memory
        self.result_addr.value = result


class MultiplyCommand(ExtendedCommand):
    def execute(self, *args, **kwargs):
        first_factor = self.param_1.value
        second_factor = self.param_2.value
        result = first_factor * second_factor
        # store the result in Computer memory
        self.result_addr.value = result


class InputCommand(ExtendedCommand):
    COMMAND_LENGTH = 2

    def __init__(self, delegate, extended_opcode, result_addr):
        super().__init__(delegate,
                         extended_opcode,
                         param_1_value=None,
                         param_2_value=None,
                         result_addr=result_addr)

    def execute(self, *args, **kwargs):
        # notify subscribers that input is requested
        self.delegate.input_buffer.request_input()
        # at this point subscribers should already put data to the
        # input_buffer
        self.result_addr.value = \
            self.delegate.input_buffer.value


class OutputCommand(ExtendedCommand):
    COMMAND_LENGTH = 2

    def __init__(self, delegate, extended_opcode, result_addr):
        super().__init__(delegate,
                         extended_opcode,
                         param_1_value=None,
                         param_2_value=None,
                         result_addr=result_addr)

    def execute(self, *args, **kwargs):
        output_value = self.result_addr.value
        self.delegate.output_buffer.value = \
            output_value
        self.delegate.output_history.append(output_value)


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
            self.result_addr.value = 1
        else:
            self.result_addr.value = 0


class EqualsCommand(ExtendedCommand):
    def execute(self, *args, **kwargs):
        if self.param_1.value == self.param_2.value:
            self.result_addr.value = 1
        else:
            self.result_addr.value = 0


class AdjustRelativeBaseCommand(ExtendedCommand):
    COMMAND_LENGTH = 2

    def __init__(self, delegate, extended_opcode, param_1_value):
        super().__init__(delegate,
                         extended_opcode,
                         param_1_value=param_1_value,
                         param_2_value=None,
                         result_addr=None)

    def execute(self, *args, **kwargs):
        self.delegate.relative_base += self.param_1.value
