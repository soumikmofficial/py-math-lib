"""Unit tests for math operations."""

import pytest
from py_math_lib import add, subtract, multiply, divide, factorial


class TestAddition:
    """Test cases for addition function."""
    
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert add(2, 3) == 5
        assert add(10, 20) == 30
    
    def test_add_negative_numbers(self):
        """Test adding negative numbers."""
        assert add(-2, -3) == -5
        assert add(-10, 5) == -5
    
    def test_add_floats(self):
        """Test adding floating point numbers."""
        assert add(2.5, 3.5) == 6.0
        assert add(0.1, 0.2) == pytest.approx(0.3)
    
    def test_add_zero(self):
        """Test adding with zero."""
        assert add(5, 0) == 5
        assert add(0, 0) == 0


class TestSubtraction:
    """Test cases for subtraction function."""
    
    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers."""
        assert subtract(5, 3) == 2
        assert subtract(20, 10) == 10
    
    def test_subtract_negative_numbers(self):
        """Test subtracting negative numbers."""
        assert subtract(-5, -3) == -2
        assert subtract(5, -3) == 8
    
    def test_subtract_floats(self):
        """Test subtracting floating point numbers."""
        assert subtract(5.5, 2.5) == 3.0
        assert subtract(0.3, 0.1) == pytest.approx(0.2)
    
    def test_subtract_zero(self):
        """Test subtracting with zero."""
        assert subtract(5, 0) == 5
        assert subtract(0, 5) == -5


class TestMultiplication:
    """Test cases for multiplication function."""
    
    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers."""
        assert multiply(2, 3) == 6
        assert multiply(5, 4) == 20
    
    def test_multiply_negative_numbers(self):
        """Test multiplying with negative numbers."""
        assert multiply(-2, 3) == -6
        assert multiply(-2, -3) == 6
    
    def test_multiply_floats(self):
        """Test multiplying floating point numbers."""
        assert multiply(2.5, 2) == 5.0
        assert multiply(0.1, 0.2) == pytest.approx(0.02)
    
    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        assert multiply(5, 0) == 0
        assert multiply(0, 10) == 0
    
    def test_multiply_by_one(self):
        """Test multiplying by one."""
        assert multiply(5, 1) == 5
        assert multiply(1, 10) == 10


class TestDivision:
    """Test cases for division function."""
    
    def test_divide_positive_numbers(self):
        """Test dividing positive numbers."""
        assert divide(6, 2) == 3
        assert divide(20, 4) == 5
    
    def test_divide_negative_numbers(self):
        """Test dividing with negative numbers."""
        assert divide(-6, 2) == -3
        assert divide(-6, -2) == 3
    
    def test_divide_floats(self):
        """Test dividing floating point numbers."""
        assert divide(5.0, 2.0) == 2.5
        assert divide(1.0, 3.0) == pytest.approx(0.333333, rel=1e-5)
    
    def test_divide_by_one(self):
        """Test dividing by one."""
        assert divide(5, 1) == 5
        assert divide(-10, 1) == -10
    
    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(0, 0)


class TestFactorial:
    """Test cases for factorial function."""
    
    def test_factorial_of_zero(self):
        """Test factorial of zero."""
        assert factorial(0) == 1
    
    def test_factorial_of_one(self):
        """Test factorial of one."""
        assert factorial(1) == 1
    
    def test_factorial_of_positive_numbers(self):
        """Test factorial of positive numbers."""
        assert factorial(3) == 6
        assert factorial(4) == 24
        assert factorial(5) == 120
        assert factorial(10) == 3628800
    
    def test_factorial_of_negative_raises_error(self):
        """Test that factorial of negative number raises ValueError."""
        with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
            factorial(-1)
        with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
            factorial(-10)
    
    def test_factorial_of_non_integer_raises_error(self):
        """Test that factorial of non-integer raises TypeError."""
        with pytest.raises(TypeError, match="Factorial is only defined for integers"):
            factorial(3.5)
        with pytest.raises(TypeError, match="Factorial is only defined for integers"):
            factorial("5")


class TestEdgeCases:
    """Test edge cases and complex scenarios."""
    
    def test_large_numbers(self):
        """Test operations with large numbers."""
        assert add(1e10, 1e10) == 2e10
        assert multiply(1e5, 1e5) == 1e10
    
    def test_very_small_numbers(self):
        """Test operations with very small numbers."""
        assert add(1e-10, 1e-10) == pytest.approx(2e-10)
        assert divide(1e-10, 2) == pytest.approx(5e-11)
    
    def test_chained_operations(self):
        """Test combining multiple operations."""
        result = add(multiply(2, 3), divide(8, 2))
        assert result == 10
        
        result = subtract(factorial(4), multiply(3, 5))
        assert result == 9  # 24 - 15 = 9