# --- Day 3 Part Two: Crossed Wires ---
import copy
from task_3 import Point, Wire, LineDirection, parse_wire_steps


class StepTrackedWire(Wire):
    def calculate_steps_to_point(self, point):
        """
        Calculate the number of steps needed for the Wire to reach the point
        :param point: The Point object to calculate steps to
        :return: the number of steps
        :raises: Exception() if the point is unreachable
        """
        # copy the object of start point into the point tracker. We don't want
        # to change the initial object
        point_tracker = copy.copy(self.start_point)
        step_count = 0

        for step in self.steps:
            direction = step[0]
            distance = int(step[1:])

            for _ in range(distance):
                if direction == LineDirection.LEFT.value:
                    point_tracker.x -= 1
                elif direction == LineDirection.RIGHT.value:
                    point_tracker.x += 1
                elif direction == LineDirection.DOWN.value:
                    point_tracker.y -= 1
                else:
                    point_tracker.y += 1

                step_count += 1

                if point_tracker == point:
                    return step_count

        # at this point we should already reach the intersection
        raise Exception('The point is unreachable')


def get_intersection_points(steps, central_port_coordinates):
    """
    Get the list of intersection points from the given list of steps
    :param steps: List of step strings from the input file
    :param central_port_coordinates: Coordinates of the pivot point
    (Central port)
    :return: Wire objects and their intersection points
    """
    first_wire_steps, second_wire_steps = steps[0], steps[1]

    first_wire = StepTrackedWire(first_wire_steps, central_port_coordinates)
    seconds_wire = StepTrackedWire(second_wire_steps, central_port_coordinates)
    first_wire.create_lines()
    seconds_wire.create_lines()

    intersection_points = first_wire.get_intersection_points(seconds_wire)

    return first_wire, seconds_wire, intersection_points


def get_step_pairs(first_wire, second_wire, intersection_points):
    first_wire_steps = []
    second_wire_steps = []

    for point in intersection_points:
        first_wire_steps.append(first_wire.calculate_steps_to_point(point))
        second_wire_steps.append(second_wire.calculate_steps_to_point(point))

    return zip(first_wire_steps, second_wire_steps)


if __name__ == '__main__':
    input_file = 'task_3_part_2_input.txt'
    central_port_coordinates = Point(0, 0)

    parsed_steps = parse_wire_steps(input_file)

    step_pairs = get_step_pairs(
        *get_intersection_points(parsed_steps, central_port_coordinates)
    )
    result = min(step_pairs, key=lambda t: sum(t))
    print(sum(result))

