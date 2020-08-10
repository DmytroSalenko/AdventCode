from intcode_computer import IntcodeComputer, parse_program
from day_11 import PaintColors, EmergencyHullPaintingRobotControl


class HullPaintDisplay:
    """Class responsible for collecting and displaying the hull panel data"""
    def __init__(self, panel_list):
        self.panel_dict = panel_list
        self.screen_size = None
        self.row_num = 0
        self.col_num = 0
        self.pixel_list = []

    def calculate_screen_size(self):
        """Get the screen size based on the min and max panel
        coordinates"""
        min_x = min(self.panel_dict.keys(), key=lambda t: t[0])[0]
        min_y = min(self.panel_dict.keys(), key=lambda t: t[1])[1]
        max_x = max(self.panel_dict.keys(), key=lambda t: t[0])[0]
        max_y = max(self.panel_dict.keys(), key=lambda t: t[1])[1]

        self.screen_size = {'min_x': min_x, 'min_y': min_y, 'max_x': max_x,
                            'max_y': max_y}

    def initialize_screen(self):
        """Initialize screen pixels with empty spaces based on screen size"""
        self.row_num = self.screen_size['max_y'] - self.screen_size['min_y'] + 1
        self.col_num = self.screen_size['max_x'] - self.screen_size['min_x'] + 1

        for row in range(self.row_num):
            self.pixel_list.append([' '] * self.col_num)

    def translate_x_coordinates(self, x_coordinate):
        """Translate hull panel coordinates into screen column """
        return x_coordinate + abs(self.screen_size['min_x'])

    def translate_y_coordinates(self, y_coordinate):
        """Translate hull panel coordinates into screen row """
        return y_coordinate + abs(self.screen_size['min_y'])

    def render_screen(self):
        for panel_coordinates in self.panel_dict.keys():
            col = self.translate_x_coordinates(panel_coordinates[0])
            row = self.translate_y_coordinates(panel_coordinates[1])
            color = self.panel_dict[panel_coordinates]['color']

            if color == PaintColors.WHITE.value:
                self.pixel_list[row][col] = '#'


def solution(input_file_name):
    program = parse_program(input_file_name)
    computer = IntcodeComputer(program=None)
    robot_controller = EmergencyHullPaintingRobotControl(computer, program)
    robot_controller.panels_tracker[(0, 0)]['color'] = PaintColors.WHITE.value
    robot_controller.run_program()

    display = HullPaintDisplay(robot_controller.panels_tracker)
    display.calculate_screen_size()
    display.initialize_screen()
    display.render_screen()

    for row in display.pixel_list[::-1]:
        print(''.join([pixel for pixel in row]))


if __name__ == '__main__':
    input_file = '../day_11_part_2/task_11__part_2_input.txt'
    solution(input_file)
