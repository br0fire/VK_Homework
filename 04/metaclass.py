class CustomMeta(type):
    def __new__(mcs, name, bases, attr_dict):
        new_attr_dict = {}
        for nme, val in attr_dict.items():
            new_attr_dict[f'custom_{nme}'] = val
        return super().__new__(mcs, name, bases, new_attr_dict)


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"
