# --- Day 4 Part Two: Secure Container ---
from task_4 import IncreaseNumberCheckHandler, AdjacentNumberCheckHandler


class StrictAdjacentNumberCheckHandler(AdjacentNumberCheckHandler):
    def process(self, number):
        """
        Check that the password contains at ONLY two adjacent
        repeated numbers otherwise raise a ValueError
        :param number:
        :return:
        :raises ValueError if password doesn't conform to adjacent number
        criteria
        """
        digits = [int(x) for x in str(number)]
        digits.sort()

        for digit in digits:
            if digits.count(digit) == 2:
                break
        else:
            raise ValueError('Adjacent matching digits should not part of a '
                             'larger group of matching digits')
        if self.successor:
            self.successor.process(number)


if __name__ == '__main__':
    num_range = (246515, 739106)
    # compose a chain of responsibility
    increase_number_check_handler = IncreaseNumberCheckHandler()
    strict_adjacent_number_check_handler = StrictAdjacentNumberCheckHandler()
    increase_number_check_handler.add_successor(
        strict_adjacent_number_check_handler
    )

    password_count = 0
    for num in range(*num_range):
        try:
            increase_number_check_handler.process(num)
            password_count += 1
        except ValueError:
            continue

    print(password_count)