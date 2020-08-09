from utils import Observable


class Buffer:
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __init__(self, value=None):
        self._value = value


class InputBuffer(Observable, Buffer):
    def __init__(self, value=None):
        super().__init__(value)
        self._input_requested = Observable(False)

    def request_input(self):
        self._input_requested.value = True

    def subscribe(self, subscriber, callback):
        self._input_requested.subscribe(subscriber, callback)

    def unsubscribe(self, subscriber):
        self._input_requested.unsubscribe(subscriber)

    def notify_subscribers(self, new_value):
        pass


class OutputBuffer(Observable, Buffer):
    pass
