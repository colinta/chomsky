class ResultList(list):
    def __repr__(self):
        return 'ResultList(' + super(ResultList, self).__repr__() + ')'

    def __str__(self):
        return ''.join(str(result) for result in self)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return ResultList(super(ResultList, self).__getitem__(key))
        return super(ResultList, self).__getitem__(key)

    def __getslice__(self, start, stop):
        '''
        deprecated, but list defines it, so have to override it here
        '''
        return ResultList(super(ResultList, self).__getslice__(start, stop))
