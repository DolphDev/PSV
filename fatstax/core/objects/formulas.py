class Formula(object):

    def __init__(self, formula):
        self.__formula__ = formula

    def call(self, rowobj):
        return self.__formula__(rowobj)