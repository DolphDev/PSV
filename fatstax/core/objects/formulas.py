class Formula(object):

    def __init__(self, formula, rowreference, **kwargs):
        self.__formula__ = formula
        self.__rowreference__ = rowreference 
        self.__kwargs__ = kwargs

    def call(self, rowobj):
        if self.__rowreference__ != rowobj:
            rowobj = self.__rowreference__
        if self.__kwargs__:
            return self.__formula__(self.__rowreference__, **self.__kwargs__)
        else:
            return self.__formula__(self.__rowreference__)
