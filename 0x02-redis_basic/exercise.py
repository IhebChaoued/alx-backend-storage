#!/usr/bin/env python3
"""Module for Cache class"""

import redis
import uuid
from typing import Callable, Optional, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of times a method is called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function to increment call count."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a function."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function to store input and output history."""
        class_name = self.__class__.__name__
        method_name = method.__name__
        input_key = f"{class_name}.{method_name}:inputs"
        output_key = f"{class_name}.{method_name}:outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)

        return output

    return wrapper


def replay(method: Callable) -> None:
    """Display history of calls for a specific function."""
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(
            name, i.decode('utf-8'), o.decode('utf-8')))


class Cache():
    """Cache class for storing data in Redis."""

    def __init__(self):
        """Initialize Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the input data in Redis."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, None]:
        """Retrieve data from Redis."""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_int(self, key):
        """Retrieve data from Redis as an integer."""
        return self.get(key, int)

    def get_str(self, key):
        """Retrieve data from Redis as a string."""
        val = self._redis.get(key)
        return val.decode('utf-8')
