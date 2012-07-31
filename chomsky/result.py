

class Result(str):
    pass


class ResultList(list):
    def __str__(self):
        return ''.join(str(result) for result in self)
