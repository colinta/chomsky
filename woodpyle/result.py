

class Result(str):
    def __init__(self, val=''):
        super(Result, self).__init__(val)
        self.suppress = False


class ResultList(list):
    def __init__(self, results=None):
        super(ResultList, self).__init__()
        if results is not None:
            self.extend(results)
        self.suppress = False

    def append(self, item, suppress=False):
        item.suppress = suppress
        super(ResultList, self).append(item)
