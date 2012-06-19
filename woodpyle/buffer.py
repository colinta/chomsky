from .exceptions import ParseException


class Buffer(object):
    def __init__(self, buffer):
        self.buffer = buffer
        self.__position = 0
        self.__marks = []

    def advance(self, amt):
        self.__position += amt

    def mark(self):
        """
        Most Matchers store the position before matching.
        """
        self.__marks.append(self.__position)

    def restore_mark(self):
        """
        Restores the position of the pushed mark.
        """
        if not self.__marks:
            raise IndexError('Cannot pop mark position')
        self.__position = self.__marks.pop()

    def forget_mark(self):
        """
        Removes the last mark pushed without moving the position.
        """
        if not self.__marks:
            raise IndexError('Cannot pop mark position')
        self.__marks.pop()

    @property
    def position(self):
        return self.__position

    def __getitem__(self, key):
        if isinstance(key, int):
            if self.__position >= len(self.buffer):
                raise ParseException(
                    'Unexpected StringEnd at {self.position}'.format(self=self),
                    buffer)
            return self.buffer[self.position + key]
