

class Result(str):
    def __repr__(self):
        return 'Result(' + super(Result, self).__repr__() + ')'

    def __getitem__(self, key):
        return Result(super(Result, self).__getitem__(key))

    def __getslice__(self, start, stop):
        return Result(super(Result, self).__getslice__(start, stop))


class ResultList(list):
    def __repr__(self):
        return 'ResultList(' + super(ResultList, self).__repr__() + ')'

    def __str__(self):
        return ''.join(str(result) for result in self)

    def __getslice__(self, start, stop):
        return ResultList(super(ResultList, self).__getslice__(start, stop))
