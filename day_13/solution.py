from enum import Enum, IntEnum, unique

from collections import defaultdict, deque
from intcode_computer import IntcodeComputer, parse_program
from utils import ObserverMixin

INPUT_FILE = './inputs/task_13_input.txt'


@unique
class TileID(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    H_PADDLE = 3
    BALL = 4


class OutputState(IntEnum):
    X_POS = 0
    Y_POS = 1
    TILE_ID = 2


class TileScreen(ObserverMixin):
    @property
    def output_state(self):
        return self._program_output_state[0]

    @property
    def blocks(self):
        return self._blocks

    def __init__(self, computer, program):
        self._computer = computer
        self._program = program
        self._blocks = defaultdict(lambda: TileID.EMPTY.value)
        self._program_output_state = deque(map(int, OutputState))
        self._x_buffer = None
        self._y_buffer = None

    def switch_output_state(self):
        self._program_output_state.rotate(-1)

    def run_program(self):
        self._computer.load_program(self._program)
        self.subscribe(self._computer.output_buffer, self.get_output)
        self._computer.run_program()

    def get_output(self, value):
        if self.output_state == OutputState.X_POS.value:
            self._x_buffer = value
        elif self.output_state == OutputState.Y_POS.value:
            self._y_buffer = value
        else:
            self._blocks[(self._x_buffer, self._y_buffer)] = value

        self.switch_output_state()


def solution():
    from pathlib import Path
    input_file = Path(INPUT_FILE)

    program = parse_program(input_file)
    computer = IntcodeComputer(program=None)
    screen = TileScreen(computer, program)
    screen.run_program()
    return len([x for x in screen.blocks.values() if x == TileID.BLOCK.value])


if __name__ == '__main__':
    import os
    os.chdir('..')

    print(solution())
