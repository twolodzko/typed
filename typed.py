from inspect import Parameter, signature
from typing import Any, Callable, Iterable, Tuple
from istype import istype


class _Typed:
    def __init__(self, func: Callable) -> None:
        """Decorate a function for runtime type checking"""
        self.func = func
        self.parameters = signature(func).parameters

    def validate_arguments(self, *args, **kwargs) -> None:
        """
        Validate arguments passed to the function based on the type annotations

        :raises TypeError: When argument passed to the function is inconsistent with type annotation
        """
        for name, argument in self.arguments_iterator(*args, **kwargs):
            annotation = self.parameters[name].annotation

            if annotation is Parameter.empty:
                # skip, parameter was not annotated
                continue

            if not istype(argument, annotation):
                raise TypeError(f"For argument {name}={argument} expected type {annotation}, got {type(argument)}")

    def arguments_iterator(self, *args, **kwargs) -> Iterable[Tuple[str, Any]]:
        """Iterate over function arguments"""
        for i, arg in enumerate(args):
            yield list(self.parameters.keys())[i], arg
        for name, arg in kwargs.items():
            yield name, arg

    def __call__(self, *args, **kwargs) -> Any:
        """Call the `self.func` function"""
        self.validate_arguments(*args, **kwargs)
        return self.func(*args, **kwargs)


def typed(func: Callable) -> Callable:
    """
    Decorate a function or method, so that the types of the input parameters are validated in runtime.
    When passing arguments with types inconsistent with type annotation, the decorated function raises a `TypeError`.

    :param func: A function to be decorated
    :return: Decorated function

    :example:

    >>> @typed
    ... def add(x: int, y: int) -> int:
    ...     return x + y
    >>> add(2, 2)
    4
    >>> add(2, "2")
    Traceback (most recent call last):
        ...
    TypeError: For argument y=2 expected type <class 'int'>, got <class 'str'>
    """
    typed_func = _Typed(func)

    def wrapped(*args, **kwargs):
        return typed_func(*args, **kwargs)

    return wrapped
