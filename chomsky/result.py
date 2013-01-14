

class Result(unicode):
    def __repr__(self):
        return 'Result(' + super(Result, self).__repr__() + ')'

    def __getitem__(self, key):
        return Result(super(Result, self).__getitem__(key))

    def __getslice__(self, start, stop):
        '''
        deprecated, but unicode defines it, so have to override it here
        '''
        return Result(super(Result, self).__getslice__(start, stop))


class ResultList(list):
    def __repr__(self):
        return 'ResultList(' + super(ResultList, self).__repr__() + ')'

    def __str__(self):
        return Result(''.join(str(result) for result in self))

    def __unicode__(self):
        return Result(''.join(unicode(result) for result in self))

    def __getitem__(self, key):
        if isinstance(key, slice):
            return ResultList(super(ResultList, self).__getitem__(key))
        return super(ResultList, self).__getitem__(key)

    def __getslice__(self, start, stop):
        '''
        deprecated, but list defines it, so have to override it here
        '''
        return ResultList(super(ResultList, self).__getslice__(start, stop))
