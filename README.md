# Decorate a function for runtime type checking



```python
>>> @typed
... def add(x: int, y: int) -> int:
...     return x + y
>>> add(2, "2")
Traceback (most recent call last):
    ...
TypeError: For argument y=2 expected type <class 'int'>, got <class 'str'>
```
