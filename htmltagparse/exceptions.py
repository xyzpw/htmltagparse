"""htmltagparse exceptions"""
import time

__all__ = [
    "TagTimeoutException",
    "RequestTimeoutException",
]

class TagTimeoutException(TimeoutError):
    """Timed out while parsing tags"""

class RequestTimeoutException(TimeoutError):
    """GET request took too long"""
