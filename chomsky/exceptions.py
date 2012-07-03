

class ParseException(Exception):
    def __init__(self, message, buffer):
        self.buffer = buffer
        super(ParseException, self).__init__(message)


class RollbackException(Exception):
    pass
