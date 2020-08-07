# --- Day 4: Secure Container ---
import abc


class NumberProcessingHandler(metaclass=abc.ABCMeta):
    """Abstract class for the password processing handlers. These hanlders
     check that the password conform to the certain rules"""
    def __init__(self, successor=None):
        self.successor = successor

    def add_successor(self, successor):
        self.successor = successor

    @abc.abstractmethod
    def process(self, password):
        pass


class AdjacentNumberCheckHandler(NumberProcessingHandler):
    def process(self, number):
        """
        Check that the password contains at least two adjacent
        repeated numbers otherwise raise a ValueError
        :param number: password to check
        :return:
        :raises ValueError if password doesn't conform to adjacent number rule
        """
        digits = [int(x) for x in str(number)]
        for i in range(len(digits)-1):
            if digits[i] == digits[i+1]:
                break
        else:
            raise ValueError(
                'Number should have at lease two adjacent repeated digits'
            )
        if self.successor:
            self.successor.process(number)


class IncreaseNumberCheckHandler(NumberProcessingHandler):
    def process(self, number):
        """
         Check that the digits in the password never decrease
        :param number:
        :return:
        :raises ValueError if digits decrease
        """
        digits = [int(x) for x in str(number)]
        if digits == sorted(digits):
            if self.successor:
                self.successor.process(number)
        else:
            raise ValueError('Digits should never decrease')


if __name__ == '__main__':
    num_range = (246515, 739106)
    # compose a chain of responsibility
    adjacent_number_check_handler = AdjacentNumberCheckHandler()
    increase_number_check_handler = IncreaseNumberCheckHandler()
    increase_number_check_handler.add_successor(adjacent_number_check_handler)

    password_count = 0
    for num in range(*num_range):
        try:
            increase_number_check_handler.process(num)
            password_count += 1
        except ValueError:
            continue

    print(password_count)
