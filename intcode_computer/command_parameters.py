from enum import Enum


class ParameterModes(Enum):
    """Thus Enum contains different modes for the Command object parameters"""
    POSITION = 0
    IMMEDIATE = 1


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

    @value.setter
    def value(self, value):
        """value of the argument cant be set only if it is in the POSITION
        mode (e.g a result_addr parameter)"""
        if self._mode == ParameterModes.POSITION.value:
            self._memory[self._value] = value
        else:
            raise ValueError('Trying to set a value of the immediate argument')

    def __init__(self, memory, value, mode):
        self._value = value
        self._memory = memory
        self._mode = mode