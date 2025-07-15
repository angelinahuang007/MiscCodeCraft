"""
Core calculator functionality providing basic arithmetic operations.
"""

class Calculator:
    def add(self, a: float, b: float) -> float:
        """Add two numbers and return the result."""
        return float(a + b)
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a and return the result."""
        return float(a - b)
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers and return the result."""
        return float(a * b)
    
    def divide(self, a: float, b: float) -> float:
        """Divide a by b and return the result.
        
        Raises:
            ZeroDivisionError: If b is zero
        """
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        return float(a / b) 