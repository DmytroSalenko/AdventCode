# --- Day 3 Part Two: Crossed Wires ---
import copy
from task_3 import Point, Line, Wire, LineDirection, parse_wire_steps


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


if __name__ == '__main__':
    input_file = 'task_3_part_2_input.txt'
    central_port_coordinates = Point(0, 0)
    parsed_results = parse_wire_steps(input_file)
    wire_1_steps, wire_2_steps = parsed_results[0], parsed_results[1]

    wire_1 = StepTrackedWire(wire_1_steps, central_port_coordinates)
    wire_2 = StepTrackedWire(wire_2_steps, central_port_coordinates)
    wire_1.create_lines()
    wire_2.create_lines()

    intersection_points = wire_1.get_intersection_points(wire_2)

    wire_1_point_steps = []
    wire_2_point_steps = []

    for point in intersection_points:
        wire_1_point_steps.append(wire_1.calculate_steps_to_point(point))
        wire_2_point_steps.append(wire_2.calculate_steps_to_point(point))


    print(list(zip(wire_1_point_steps, wire_2_point_steps)))

