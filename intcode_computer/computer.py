from intcode_computer import OpCodeExtended, AddCommand, \
    MultiplyCommand, InputCommand, OutputCommand, JumpIfTrueCommand, \
    JumpIfFalseCommand, LessThanCommand, EqualsCommand, OutputBuffer, \
    InputBuffer


class IntcodeComputer:
    COMMAND_MAPPING = {
        OpCodeExtended.ADD.value: AddCommand,
        OpCodeExtended.MULT.value: MultiplyCommand,
        OpCodeExtended.INPUT.value: InputCommand,
        OpCodeExtended.OUTPUT.value: OutputCommand,
        OpCodeExtended.JUMP_IF_FALSE.value: JumpIfFalseCommand,
        OpCodeExtended.JUMP_IF_TRUE.value: JumpIfTrueCommand,
        OpCodeExtended.LESS_THAN.value: LessThanCommand,
        OpCodeExtended.EQUALS.value: EqualsCommand
    }

    @property
    def input_buffer(self):
        return self._input_buffer

    @property
    def output_buffer(self):
        return self._output_buffer

    @property
    def command_pointer(self):
        return self._command_pointer

    @command_pointer.setter
    def command_pointer(self, value):
        self._command_pointer = value

    @property
    def output_history(self):
        return self._output_history

    def __init__(self, memory, input_buffer=None, output_buffer=None):
        self.memory = memory
        self._command_pointer = 0
        self._output_buffer = OutputBuffer(output_buffer)
        self._input_buffer = InputBuffer(input_buffer)
        self._output_history = []

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

    def set_program(self, program):
        self.memory = program
        self.command_pointer = 0

    def send_input_data(self, data):
        self._input_buffer.value = data

    def get_memory_state(self):
        return self.memory
