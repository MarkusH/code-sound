import abc


class BaseType(abc.ABC):
    pass


class Expression(BaseType):
    pass


class Name(BaseType):
    pass


class Call(BaseType):
    pass


class For(BaseType):
    pass


class While(BaseType):
    pass


class If(BaseType):
    pass


class Module(BaseType):
    pass


class FunctionDef(BaseType):
    pass


class ClassDef(BaseType):
    pass


class Statement(BaseType):
    pass


class Attribute(BaseType):
    pass


class Tuple(BaseType):
    pass


class Assign(BaseType):
    pass


class Num(BaseType):
    pass
