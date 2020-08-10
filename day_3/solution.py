# --- Day 3: Crossed Wires ---
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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def manhattan_distance(self, point):
        """Get the manhattan distance between the current
        and the given points"""
        return abs(self.x - point.x) + abs(self.y - point.y)


class Line:
    @property
    def is_horizontal(self):
        return self.step[0] in (LineDirection.LEFT.value,
                                LineDirection.RIGHT.value)

    @property
    def length(self):
        if self.is_horizontal:
            return abs(self.start_point.x - self.end_point.x)
        else:
            return abs(self.start_point.x - self.end_point.x)

    @property
    def direction(self):
        return self.step[0]

    def __init__(self, start_point, end_point, step):
        self.start_point = start_point
        self.end_point = end_point
        self.step = step

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

    def includes(self, point):
        """Check if the given point is on the line"""
        if self.is_horizontal:
            return (point.y == self.start_point.y
                    and self.start_point.x <= point.x <= self.end_point.x)
        else:
            return (point.x == self.start_point.x
                    and self.start_point.y <= point.y <= self.end_point.y)


class Wire:
    def __init__(self, steps, central_port):
        self.steps = steps
        self.start_point = central_port
        self.vertical_lines = []
        self.horizontal_lines = []

    def _create_line(self, base_point, step):
        """Produce a line objects with two points based on the pivot point and
        the given path.
        To simplify the calculation the starting point for every line will
        always be the left-most(in case of horizontal line) or the
        lowest(in case of vertical line) point"""
        direction = step[0]
        direction_horizontal = direction in (LineDirection.LEFT.value,
                                             LineDirection.RIGHT.value)
        if direction_horizontal:
            line, second_point = self._create_horizontal_line(base_point, step)
            self.horizontal_lines.append(line)
        else:
            line, second_point = self._create_vertical_line(base_point, step)
            self.vertical_lines.append(line)

        return second_point

    def _create_horizontal_line(self, base_point, step):
        # since the direction is horizontal all points will have the same
        # Y coordinate
        direction = step[0]
        distance = int(step[1:])
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
        return Line(start_point, end_point, step), \
            start_point if direction == LineDirection.LEFT.value else end_point

    def _create_vertical_line(self, base_point, step):
        # since the direction is vertical all points will have the same
        # X coordinate
        direction = step[0]
        distance = int(step[1:])
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
        return Line(start_point, end_point, step), \
            start_point if direction == LineDirection.DOWN.value else end_point

    def create_lines(self):
        # the variable to store the result of the previous line generation
        # at the beginning it will contain the central port coordinates
        previous_result = self.start_point
        for step in self.steps:
            previous_result = self._create_line(previous_result, step)

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


if __name__ == '__main__':
    input_file = 'task_3_input.txt'
    central_port_coordinates = Point(0, 0)

    parsed_steps = parse_wire_steps(input_file)
    first_wire_steps, second_wire_stels = parsed_steps[0], parsed_steps[1]

    first_wire = Wire(first_wire_steps, central_port_coordinates)
    second_wire = Wire(second_wire_stels, central_port_coordinates)
    first_wire.create_lines()
    second_wire.create_lines()

    intersection_points = first_wire.get_intersection_points(second_wire)
    closest_point = min(
        intersection_points,
        key=lambda t: t.manhattan_distance(central_port_coordinates)
    )
    print(closest_point.manhattan_distance(central_port_coordinates))


