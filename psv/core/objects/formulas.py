class Formula(object):

    __slots__ = ["__formula__", "__rowreference__", "__kwargs__"]

    def __init__(self, formula, rowreference, **kwargs):
        self.__formula__ = formula
        self.__rowreference__ = rowreference
        self.__kwargs__ = kwargs

    def __call__(self):
        return self.call()

    def __str__(self):
        return str(self.call())

    def call(self):
        if self.__kwargs__:
            return self.__formula__(self.__rowreference__, **self.__kwargs__)
        else:
            return self.__formula__(self.__rowreference__)
