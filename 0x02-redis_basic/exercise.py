#!/usr/bin/env python3
"""Module for Cache class."""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a function."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)

        return output
    return wrapper


class Cache:
    """Cache class for storing data in Redis."""

    def __init__(self):
        """Initialize Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the input data in Redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """Retrieve data from Redis"""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieve data from Redis as a UTF-8 decoded string"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieve data from Redis as an integer"""
        return self.get(key, fn=int)


def replay(func: Callable):
    """Display the history of calls of a particular function."""
    inputs = cache._redis.lrange("{}:inputs".format(func.__qualname__), 0, -1)
    outputs = cache._redis.lrange("{}:outputs".format(func.__qualname__), 0, -1)

    print("{} was called {} times:".format(func.__qualname__, len(inputs)))
    for input_data, output_data in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(func.__qualname__, input_data, output_data))