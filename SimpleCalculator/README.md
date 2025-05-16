# Simple Calculator

A modern, user-friendly calculator application built with Python and Tkinter, following Test-Driven Development (TDD) principles.

## Features

### Core Features
- Basic arithmetic operations:
  - Addition (+)
  - Subtraction (-)
  - Multiplication (*)
  - Division (/)
- Advanced operations:
  - Square root (√)
  - Power (x²)
  - Percentage (%)
- Memory functions:
  - Memory Save (MS)
  - Memory Recall (MR)
  - Memory Clear (MC)
- Clear entry (CE) and All Clear (AC)
- Support for decimal numbers
- Keyboard input support

### Technical Features
- Error handling for:
  - Division by zero
  - Invalid inputs
  - Overflow conditions
- History of calculations
- Responsive GUI
- Cross-platform compatibility

## Tech Stack

- **Language:** Python 3.11+
- **GUI Framework:** Tkinter
- **Testing:**
  - pytest for unit testing
  - pytest-cov for code coverage
- **Code Quality:**
  - flake8 for linting
  - black for code formatting
- **Documentation:** Sphinx

## Project Structure

```
SimpleCalculator/
├── src/
│   ├── calculator/
│   │   ├── __init__.py
│   │   ├── core.py          # Core calculation logic
│   │   ├── memory.py        # Memory management
│   │   └── gui.py           # GUI implementation
│   └── main.py              # Application entry point
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_memory.py
│   └── test_gui.py
├── docs/
│   └── technical_docs/
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## User Stories

1. **Basic Calculation**
   ```
   As a user
   I want to perform basic arithmetic operations
   So that I can solve simple mathematical problems
   ```

2. **Memory Functions**
   ```
   As a user
   I want to store and recall numbers in memory
   So that I can reuse previous results in calculations
   ```

3. **Error Prevention**
   ```
   As a user
   I want to be notified of invalid operations
   So that I can avoid calculation errors
   ```

4. **Calculation History**
   ```
   As a user
   I want to see my calculation history
   So that I can track my previous calculations
   ```

5. **Keyboard Support**
   ```
   As a user
   I want to use my keyboard for input
   So that I can work more efficiently
   ```

## Development Approach

This project follows Test-Driven Development (TDD) principles:
1. Write failing tests first
2. Implement minimum code to pass tests
3. Refactor while maintaining test coverage
4. Repeat for new features

## Getting Started

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. For development, install additional dependencies:
   ```
   pip install -r requirements-dev.txt
   ```

## Running Tests

```bash
pytest tests/
pytest --cov=src tests/  # For coverage report
```

## Contributing

1. Write tests first
2. Ensure all tests pass
3. Maintain code coverage above 90%
4. Follow PEP 8 guidelines
5. Use descriptive commit messages 