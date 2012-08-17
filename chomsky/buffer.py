from .exceptions import ParseException


class Buffer(object):
    @property
    def buffer(self):
        return self.__buffer

    def __init__(self, buffer):
        self.__buffer = buffer
        self.__position = 0
        self.__marks = []

    def advance(self, amt):
        self.__position += amt

    def rest(self):
        return self.__buffer[self.__position:]

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

    def __len__(self):
        return len(self.__buffer)

    def __getitem__(self, key):
        if self.__position >= len(self.__buffer):
            raise ParseException(
                'Unexpected end of buffer at {self.position}'.format(self=self),
                buffer)

        if isinstance(key, int):
            return self.__buffer[self.position + key]

        if isinstance(key, slice):
            if key.start == None and key.stop == None:
                start = 0
                stop = len(self.__buffer)
            else:
                if key.start == None:
                    start = 0
                else:
                    start = self.position + key.start

                if key.stop == None:
                    stop = self.position
                else:
                    stop = self.position + key.stop
            return Buffer(self.__buffer[slice(start, stop, key.step)])

        raise TypeError('Unknown key {key!r}'.format(key=key))

    def __repr__(self):
        return 'Buffer({0!r} + {1!r})'.format(self.__buffer[:self.__position], self.__buffer[self.__position:])

    def __str__(self):
        return str(self.__buffer)
