class NonNegative:
    def __get__(self, obj, objtype):
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise ValueError('Object can be only int or float')
        if value < 0:
            raise ValueError('Cannot be negative.')
        obj.__dict__[self.name] = value

    def __set_name__(self, obj, name):
        self.name = name


class IntegerLabel:
    def __get__(self, obj, objtype):
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise ValueError('Object can be only int')
        if not 1 <= value <= 10:
            raise ValueError('Label takes a value from 1 to 10')
        obj.__dict__[self.name] = value

    def __set_name__(self, obj, name):
        self.name = name


class ListBool:
    def __get__(self, obj, objtype):
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        if not isinstance(value, tuple):
            raise ValueError('Object can be only tuple')
        if len(value) != 3:
            raise ValueError('Tuple contains only 3 values')
        if list(filter(lambda x: not isinstance(x, bool), value)):
            raise ValueError('Tuple contains only boolean values')
        obj.__dict__[self.name] = value

    def __set_name__(self, obj, name):
        self.name = name


class ChipTantrix:

    area = NonNegative()
    label = IntegerLabel()
    solid_lines = ListBool()

    def __init__(self, area, label, solid_lines):
        self.area = area
        self.label = label
        self.solid_lines = solid_lines
