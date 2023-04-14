from functools import wraps


def is_magic(name: str) -> bool:
    return name.startswith("__") and name.endswith("__")


def custom_dct(attrs):
    custom_attrs = {}
    for attr_name, attr_value in attrs.items():
        if is_magic(attr_name):
            custom_attrs[attr_name] = attr_value
        else:
            custom_attrs["custom_" + attr_name] = attr_value
    return custom_attrs


class CustomMeta(type):
    def __new__(mcs, name, bases, attrs):

        def _setattr(self, name, value):
            if not is_magic(name):
                name = "custom_"+name
            object.__setattr__(self, name, value)

        def override_init(function):
            @wraps(function)
            def _wrapper(*args, **kwargs):
                cls.__setattr__ = object.__setattr__
                function(*args, **kwargs)
                cls.__setattr__ = _setattr
            return _wrapper
        cls = super().__new__(mcs, name, bases, custom_dct(attrs))
        cls.__init__ = override_init(cls.__init__)
        return cls

    def __call__(cls, *args, **kwargs):
        ret = super().__call__(*args, **kwargs)
        ret.__dict__ = custom_dct(ret.__dict__)
        return ret


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"
