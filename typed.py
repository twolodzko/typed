from inspect import Parameter, signature
from typing import Any, Callable


class _Typed:
    def __init__(self, func: Callable) -> None:
        self.func = func
        self.parameters = signature(func).parameters

    def validate_arguments(self, *args, **kwargs) -> None:
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
        self.validate_arguments(*args, **kwargs)
        return self.func(*args, **kwargs)


def typed(func: Callable) -> Callable:
    typed_func = _Typed(func)

    def wrapped(*args, **kwargs):
        return typed_func(*args, **kwargs)

    return wrapped
