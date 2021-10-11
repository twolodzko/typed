from inspect import Parameter, signature
from typing import Any, Callable


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
        for idx, (name, parameter) in enumerate(self.parameters.items()):
            if name in kwargs:
                argument = kwargs[name]
            elif idx < len(args):
                argument = args[idx]
            else:
                break

            annotation = self.parameters[name].annotation

            if annotation is Parameter.empty:
                # skip, parameter was not annotated
                continue

            if not isinstance(argument, annotation):
                raise TypeError(f"For argument {name}={argument} expected type {annotation}, got {type(argument)}")

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
