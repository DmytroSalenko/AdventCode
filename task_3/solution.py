from enum import Enum


class LineDirection(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    UP = 'U'
    DOWN = 'D'


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point({0},{1})'.format(self.x, self.y)

    def manhattan_distance(self, point):
        return abs(self.x - point.x) + abs(self.y - point.y)


class Line:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def __repr__(self):
        return 'Line({0}; {1})'.format(self.start_point, self.end_point)

    def get_intersection_point(self, line):
        """Since we have only horizontal and vertical lines with positive
        direction we could implement the simplified intersection checking"""
        if (
            min(self.start_point.x, self.end_point.x) > line.start_point.x
            or max(self.start_point.x, self.end_point.x) < line.start_point.x
            or min(line.start_point.y, line.end_point.y) > self.start_point.y
            or max(line.start_point.y, line.end_point.y) < self.start_point.y
        ):
            # lines do not intersect
            return None
        else:
            return Point(line.start_point.x, self.start_point.y)


class Wire:
    def __init__(self, steps, central_port):
        self.steps = steps
        self.start_point = central_port
        self.vertical_lines = []
        self.horizontal_lines = []

    def _generate_line(self, base_point, step):
        """Produce a line objects with two points based on the base point and
        given path
        To simplify the calculation the starting point for every line will
        always be the left-most or the lowest point"""
        direction = step[0]
        distance = int(step[1:])
        direction_horizontal = direction in (LineDirection.LEFT.value,
                                             LineDirection.RIGHT.value)
        if direction_horizontal:
            line, second_point = self._generate_horizontal_line(base_point,
                                                                direction,
                                                                distance)
            self.horizontal_lines.append(line)
        else:
            line, second_point = self._generate_vertical_line(base_point,
                                                              direction,
                                                              distance)
            self.vertical_lines.append(line)

        return second_point

    def _generate_horizontal_line(self, base_point, direction, distance):
        # since the direction is horizontal all points will have the same
        # Y coordinate
        start_y = end_y = base_point.y
        if direction == LineDirection.LEFT.value:
            start_x = base_point.x - distance
            end_x = base_point.x

        else:
            start_x = base_point.x
            end_x = base_point.x + distance

        start_point = Point(start_x, start_y)
        end_point = Point(end_x, end_y)
        # we also want to return the second point that has been created
        # to use it as the base point for the next line
        # when we will be generating all the lines
        return Line(start_point, end_point), \
            start_point if direction == LineDirection.LEFT.value else end_point

    def _generate_vertical_line(self, base_point, direction, distance):
        # since the direction is vertical all points will have the same
        # X coordinate
        start_x = end_x = base_point.x
        if direction == LineDirection.DOWN.value:
            start_y = base_point.y - distance
            end_y = base_point.y
        else:
            start_y = base_point.y
            end_y = base_point.y + distance
        start_point = Point(start_x, start_y)
        end_point = Point(end_x, end_y)
        # we also want to return the second point that has been created
        # to use it as the base point for the next line
        # when we will be generating all the lines
        return Line(start_point, end_point), \
            start_point if direction == LineDirection.DOWN.value else end_point

    def generate_lines(self):
        # the variable to store the result of the previous line generation
        # at the beginning it will contain the central port coordinates
        previous_result = self.start_point
        for step in self.steps:
            previous_result = self._generate_line(previous_result, step)

    def get_intersection_points(self, another_wire):
        """Get the list of intersection points of the current wire with the
        given wire.
        Note: Since we don't consider collinearity cases we can only check
        the intersection of horizontal and vertical lines and vice versa"""
        intersection_points = []
        for line in self.horizontal_lines:
            for other_line in another_wire.vertical_lines:
                if intersection_point := line.get_intersection_point(other_line):
                    intersection_points.append(intersection_point)
        for line in self.vertical_lines:
            for other_line in another_wire.horizontal_lines:
                if intersection_point := line.get_intersection_point(other_line):
                    intersection_points.append(intersection_point)
        return intersection_points


def parse_wire_steps(puzzle_input_file):
    """Get the list of steps for every wire from the input_file"""
    results = []
    with open(puzzle_input_file, 'r') as puzzle_input:
        for line in puzzle_input:
            results.append([x for x in line.split(',')])
    return results


def lowest_manhattan_distance(points_list, related_to):
    """ Get the point with the lowest manhattan related to the
    given pivot point"""
    if not points_list: return None
    min_point = points_list[0]
    min_distance = min_point.manhattan_distance(related_to)
    for current_point in points_list[1:]:
        current_distance = current_point.manhattan_distance(related_to)
        if current_distance < min_distance:
            min_point = current_point
            min_distance = current_distance

    return min_point, min_distance


def solution(input_file_name, central_port_coordinates):
    # get the list of wire steps
    parsed_results = parse_wire_steps(input_file_name)
    wire_1_steps, wire_2_steps = parsed_results[0], parsed_results[1]

    wire_1 = Wire(wire_1_steps, central_port_coordinates)
    wire_2 = Wire(wire_2_steps, central_port_coordinates)
    wire_1.generate_lines()
    wire_2.generate_lines()

    intersection_points = wire_1.get_intersection_points(wire_2)
    _, min_distance = \
        lowest_manhattan_distance(intersection_points,
                                  related_to=central_port_coordinates)
    return min_distance


if __name__ == '__main__':
    input_file = 'task_3_input.txt'
    central_port_coordinates = Point(0, 0)
    min_distance = solution(input_file, central_port_coordinates)
    print(min_distance)

