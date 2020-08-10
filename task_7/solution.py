# --- Day 7: Amplification Circuit ---
import itertools

from utils import ObserverMixin
from intcode_computer import IntcodeComputer, parse_program


class Amplifier(ObserverMixin):
    @property
    def computer(self):
        return self._computer

    @property
    def phase_setting(self):
        return self._phase_setting

    @phase_setting.setter
    def phase_setting(self, value):
        self._phase_setting = value

    @property
    def input_signal(self):
        return self._input_signal

    @input_signal.setter
    def input_signal(self, value):
        self._input_signal = value

    def __init__(self, computer, program, phase_setting=None):
        self._computer = computer
        self._phase_setting = phase_setting
        self._input_signal = 0
        self._program = program
        self._successor = None
        # states of the amplifier
        self._is_phase_setting_provided = False

    def set_successor(self, amp):
        self._successor = amp

    def get_output_signal(self):
        self.computer.load_program(self._program.copy())
        self.subscribe(self.computer.input_buffer, self.provide_amp_data)
        self.computer.run_program()
        self.unsubscribe(self.computer.input_buffer)

        output_signal = self.computer.output_buffer.value

        if self._successor is not None:
            self._successor.input_signal = output_signal
            return self._successor.get_output_signal()
        else:
            return output_signal

    def provide_amp_data(self, value):
        """Observer callback to provide the phase config or input_signal
         when input is requested by the computer"""
        if value:
            if not self._is_phase_setting_provided:
                self.computer.send_input_data(self.phase_setting)
                self._is_phase_setting_provided = True
            else:
                self.computer.send_input_data(self.input_signal)
                self._is_phase_setting_provided = False


def solution(input_file_name):
    program = parse_program(input_file_name)
    computer = IntcodeComputer(program=None)

    amp_A = Amplifier(computer, program)
    amp_B = Amplifier(computer, program)
    amp_C = Amplifier(computer, program)
    amp_D = Amplifier(computer, program)
    amp_E = Amplifier(computer, program)

    # compose the Chain of Responsibility
    amp_A.set_successor(amp_B)
    amp_B.set_successor(amp_C)
    amp_C.set_successor(amp_D)
    amp_D.set_successor(amp_E)

    base_config = [0, 1, 2, 3, 4]    # basic configuration
    amp_list = [amp_A, amp_B, amp_C, amp_D, amp_E]

    signal_outputs = []
    for phase_config in itertools.permutations(base_config, len(base_config)):
        set_phases(amp_list, phase_config)
        signal_outputs.append(amp_A.get_output_signal())

    return max(signal_outputs)


def set_phases(amp_list, config):
    assert len(amp_list) == len(config), \
        'Number of amplifier does not correspond to the configuration provided'

    for index, amp in enumerate(amp_list):
        amp.phase_setting = config[index]


if __name__ == '__main__':
    input_file = '../task_7/task_7_input.txt'
    result = solution(input_file)
    print(result)







