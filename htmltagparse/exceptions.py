"""htmltagparse exceptions"""
import time

__all__ = [
    "HtmlHttpError",
    "HtmlTagError",
]

class HtmlHttpError(Exception):
    """HTTPS error associated with htmltagparse."""
    def __init__(self, *args):
        pass

class HtmlTagError(Exception):
    """Error parsing tags."""
    def __init__(self, *args):
        pass
