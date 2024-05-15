#!/usr/bin/env python3
"""Module for Cache class."""
import redis
import uuid
from typing import Union, Callable


class Cache:
    """Cache class for storing data in Redis."""

    def __init__(self):
        """Initialize Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the input data in Redis using a random key and return the key"""
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
