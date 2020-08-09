class Observable:
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.notify_subscribers(value)

    @property
    def subscribers(self):
        return self._subscribers

    def __init__(self, value):
        self._value = value
        self._subscribers = {}

    def subscribe(self, subscriber, subscriber_callback):
        subscriber_id = id(subscriber)
        if subscriber_id not in self._subscribers.keys():
            self._subscribers[id(subscriber)] = subscriber_callback

    def unsubscribe(self, subscriber):
        self._subscribers.pop(id(subscriber))

    def notify_subscribers(self, new_value):
        for subscriber_callback in self._subscribers.values():
            subscriber_callback(new_value)


class ObserverMixin:
    def subscribe(self, observable, callback):
        observable.subscribe(self, callback)

    def unsubscribe(self, observable):
        observable.unsubscribe(self)