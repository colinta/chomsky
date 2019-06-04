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

    def mark(self, mark_id=None):
        """
        Most Matchers store the position before matching.

        The ``mark_id`` feature is useful during internal chomsky debugging.
        Passing the matcher or grammar will ensure that the object that set the
        mark is the same object that later restored or removed the mark.
        """
        self.__marks.append((self.__position, mark_id and id(mark_id)))

    def restore_mark(self, mark_id=None):
        """
        Restores the position of the pushed mark.
        """
        if not self.__marks:
            raise IndexError('Cannot pop mark position')
        pos, prev_id = self.__marks.pop()
        mark_id = mark_id and id(mark_id)
        if (prev_id or mark_id) and prev_id != mark_id:
            raise Exception('Mark ids do not match. old={prev_id!r}, new={mark_id!r}'.format(**locals()))
        self.__position = pos

    def forget_mark(self, mark_id=None):
        """
        Removes the last mark pushed without moving the position.
        """
        if not self.__marks:
            raise IndexError('Cannot pop mark position')
        pos, prev_id = self.__marks.pop()
        mark_id = mark_id and id(mark_id)
        if (prev_id or mark_id) and prev_id != mark_id:
            raise Exception('Mark ids do not match. old={prev_id!r}, new={mark_id!r}'.format(**locals()))
        return pos, self.__position

    @property
    def position(self):
        return self.__position

    def __bool__(self):
        return len(self.__buffer) and self.__position < len(self.__buffer)

    def __len__(self):
        return len(self.__buffer)

    def __getitem__(self, key):
        if self.__position >= len(self.__buffer):
            raise ParseException(
                'Unexpected end of buffer at {self.position}'.format(self=self)
                )

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
                    stop = len(self.__buffer)
                elif key.stop < 0:
                    stop = key.stop
                else:
                    stop = self.position + key.stop
            return Buffer(self.__buffer[slice(start, stop, key.step)])

        raise TypeError('Unknown key {key!r}'.format(key=key))

    def __repr__(self):
        return 'Buffer({0!r} + {1!r})'.format(self.__buffer[:self.__position], self.__buffer[self.__position:])

    def __str__(self):
        return self.__buffer
