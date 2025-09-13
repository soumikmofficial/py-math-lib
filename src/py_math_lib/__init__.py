"""Py Math Lib - A simple math library for demonstration purposes."""

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "0.0.0.dev0"

from .math_operations import add, subtract, multiply, divide, factorial

__all__ = ["add", "subtract", "multiply", "divide", "factorial", "__version__"]
