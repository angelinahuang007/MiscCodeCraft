import unittest
from src.core import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        self.calc = Calculator()

    def test_add(self):
        """Test addition functionality."""
        # Test positive numbers
        self.assertEqual(self.calc.add(2, 3), 5.0)
        # Test negative numbers
        self.assertEqual(self.calc.add(-1, -1), -2.0)
        # Test zero
        self.assertEqual(self.calc.add(0, 5), 5.0)
        # Test floating point numbers
        self.assertAlmostEqual(self.calc.add(0.1, 0.2), 0.3, places=10)

    def test_subtract(self):
        """Test subtraction functionality."""
        # Test positive numbers
        self.assertEqual(self.calc.subtract(5, 3), 2.0)
        # Test negative numbers
        self.assertEqual(self.calc.subtract(-1, -1), 0.0)
        # Test zero
        self.assertEqual(self.calc.subtract(5, 0), 5.0)
        # Test floating point numbers
        self.assertAlmostEqual(self.calc.subtract(0.3, 0.1), 0.2, places=10)

    def test_multiply(self):
        """Test multiplication functionality."""
        # Test positive numbers
        self.assertEqual(self.calc.multiply(2, 3), 6.0)
        # Test negative numbers
        self.assertEqual(self.calc.multiply(-2, 3), -6.0)
        # Test zero
        self.assertEqual(self.calc.multiply(5, 0), 0.0)
        # Test floating point numbers
        self.assertAlmostEqual(self.calc.multiply(0.1, 0.2), 0.02, places=10)

    def test_divide(self):
        """Test division functionality."""
        # Test positive numbers
        self.assertEqual(self.calc.divide(6, 2), 3.0)
        # Test negative numbers
        self.assertEqual(self.calc.divide(-6, 2), -3.0)
        # Test floating point numbers
        self.assertAlmostEqual(self.calc.divide(0.3, 0.1), 3.0, places=10)
        
    def test_divide_by_zero(self):
        """Test division by zero raises appropriate error."""
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(5, 0)

if __name__ == '__main__':
    unittest.main()

