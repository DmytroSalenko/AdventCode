class Memory:
    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, value):
        self._container = value

    @container.setter
    def container(self, value):
        self._container = value

    def __init__(self, program=None):
        self._container = program if program is not None else []

    def __getitem__(self, item):
        return self._container.__getitem__(item)

    def __setitem__(self, key, value):
        return self._container.__setitem__(key, value)

