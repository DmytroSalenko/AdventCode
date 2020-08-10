from enum import Enum
from collections import defaultdict

from utils import ObserverMixin
from intcode_computer import IntcodeComputer, parse_program


class PaintColors(Enum):
    BLACK = 0
    WHITE = 1


class RobotDirections(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 3
    DOWN = 4


class RobotOutputState(Enum):
    COLOR = 0
    DIRECTION = 1


class EmergencyHullPaintingRobotControl(ObserverMixin):
    @property
    def robot_position(self):
        return self._robot_current_position

    @robot_position.setter
    def robot_position(self, value):
        self._robot_current_position = value

    @property
    def robot_direction(self):
        return self._robot_current_direction

    @robot_direction.setter
    def robot_direction(self, value):
        self._robot_current_direction = value

    @property
    def panels_tracker(self):
        return self._panels_tracker

    def __init__(self, computer, program):
        self._computer = computer
        self._program = program
        self._panels_tracker = defaultdict(
            lambda: {'times_painted': 0, 'color': PaintColors.BLACK.value}
        )
        self._robot_current_direction = RobotDirections.UP.value
        self._robot_current_position = {'x': 0, 'y': 0}
        self._robot_output_state = RobotOutputState.COLOR.value

    def run_program(self):
        self._computer.load_program(self._program)
        self.subscribe(self._computer.input_buffer, self.provide_input)
        self.subscribe(self._computer.output_buffer, self.get_output)

        self._computer.run_program()

    def provide_input(self, value):
        color = self.check_current_panel_color()
        self._computer.send_input_data(color)

    def get_output(self, output):
        if self._robot_output_state == RobotOutputState.COLOR.value:
            color = output
            self.update_panel_state(color)
        else:
            turn_direction = output
            self.update_robot_position(turn_direction)
        self.switch_robot_output_state()

    def switch_robot_output_state(self):
        if self._robot_output_state == RobotOutputState.COLOR.value:
            self._robot_output_state = RobotOutputState.DIRECTION.value
        else:
            self._robot_output_state = RobotOutputState.COLOR.value

    def check_current_panel_color(self):
        position = self.robot_position
        current_coordinates = (position['x'], position['y'])
        color = self._panels_tracker[current_coordinates]['color']
        return color

    def update_robot_position(self, turn_direction):
        current_position = self.robot_position
        facing_direction = self.robot_direction

        if facing_direction in (RobotDirections.LEFT.value,
                                RobotDirections.RIGHT.value):
            updated_position, updated_direction = \
                self._update_vertical_position(current_position,
                                               facing_direction,
                                               turn_direction
            )
        else:
            updated_position, updated_direction = \
                self._update_horizontal_position(current_position,
                                                 facing_direction,
                                                 turn_direction
            )
        self.robot_position = updated_position
        self.robot_direction = updated_direction

    def _update_vertical_position(self, current_position, facing_direction,
                                  turn_direction):
        updated_position = current_position
        if facing_direction == RobotDirections.LEFT.value:
            if turn_direction == RobotDirections.LEFT.value:
                updated_position['y'] -= 1
                updated_direction = RobotDirections.DOWN.value
            else:
                updated_position['y'] += 1
                updated_direction = RobotDirections.UP.value
        else:
            if turn_direction == RobotDirections.LEFT.value:
                updated_position['y'] += 1
                updated_direction = RobotDirections.UP.value
            else:
                updated_position['y'] -= 1
                updated_direction = RobotDirections.DOWN.value
        return updated_position, updated_direction

    def _update_horizontal_position(self, current_position, facing_direction,
                                    turn_direction):
        updated_position = current_position
        if facing_direction == RobotDirections.UP.value:
            if turn_direction == RobotDirections.LEFT.value:
                updated_position['x'] -= 1
                updated_direction = RobotDirections.LEFT.value
            else:
                updated_position['x'] += 1
                updated_direction = RobotDirections.RIGHT.value
        else:
            if turn_direction == RobotDirections.LEFT.value:
                updated_position['x'] += 1
                updated_direction = RobotDirections.RIGHT.value
            else:
                updated_position['x'] -= 1
                updated_direction = RobotDirections.LEFT.value
        return updated_position, updated_direction

    def update_panel_state(self, color):
        position = self.robot_position
        coordinates = (position['x'], position['y'])
        self._panels_tracker[coordinates]['times_painted'] += 1
        self._panels_tracker[coordinates]['color'] = color


if __name__ == '__main__':
    input_file = '../task_11/task_11_input.txt'
    program = parse_program(input_file)
    computer = IntcodeComputer(program=None)
    robot_controller = EmergencyHullPaintingRobotControl(computer, program)
    robot_controller.run_program()
    print(len(robot_controller.panels_tracker))
