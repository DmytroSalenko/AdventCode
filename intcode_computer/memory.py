class Memory:
    """Storage for the IntComputer class. It should store the command
    instructions to run the program. This class behaves as a normal list
    except it may contain some additional logic if required"""
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


class DynamicMemory(Memory):
    """This class behaves exactly as its superclass but also it is capable
    dynamically extend the capacity of memory when computer tries to access
    address outside of the currently allocated memory"""
    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except IndexError as e:
            if item >= len(self.container):
                self._reallocate_memory(item)
                return self.__getitem__(item)
            else:
                raise e

    def __setitem__(self, key, value):
        try:
            return super().__setitem__(key, value)
        except IndexError as e:
            if key >= len(self.container):
                self._reallocate_memory(key)
                return self.__setitem__(key, value)
            else:
                raise e

    def _reallocate_memory(self, index):
        current_size = len(self._container)
        items_to_add = index - current_size
        items_to_add = (items_to_add * 3) + 1
        self.container.extend([0]*items_to_add)
