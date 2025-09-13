# Py Math Lib

A simple Python math library for demonstration purposes, showcasing CI/CD with Jenkins pipeline automation.

## Features

- Basic arithmetic operations (add, subtract, multiply, divide)
- Factorial calculation
- Type hints for better IDE support
- Comprehensive test coverage (>80%)
- Automated CI/CD with Jenkins

## Installation

### From PyPI (once published)
```bash
pip install py-math-lib
```

### From GitHub Packages
```bash
pip install py-math-lib --index-url https://pypi.org/simple --extra-index-url https://test.pypi.org/simple/
```

### For Development
```bash
git clone https://github.com/yourusername/py-math-lib.git
cd py-math-lib
pip install -e ".[dev]"
```

## Usage

```python
from py_math_lib import add, subtract, multiply, divide, factorial

# Basic operations
result = add(5, 3)  # 8
result = subtract(10, 4)  # 6
result = multiply(3, 7)  # 21
result = divide(15, 3)  # 5.0

# Factorial
result = factorial(5)  # 120

# Error handling
try:
    divide(10, 0)
except ValueError as e:
    print(e)  # Cannot divide by zero

try:
    factorial(-1)
except ValueError as e:
    print(e)  # Factorial is not defined for negative numbers
```

## Development

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run tests with coverage
pytest

# Run specific test file
pytest tests/test_math_operations.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black src/ tests/

# Check formatting
black --check src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/py_math_lib
```

### Building

```bash
# Build distribution packages
python -m build

# This creates:
# - dist/py_math_lib-*.whl (wheel)
# - dist/py_math_lib-*.tar.gz (source distribution)
```

## CI/CD Pipeline

This project uses Jenkins for automated CI/CD. The pipeline includes:

1. **Initialize**: Setup environment and detect branch
2. **Setup Python**: Create virtual environment and install dependencies
3. **Quality Checks**: Run linting, type checking, and format checks in parallel
4. **Test**: Run pytest with coverage reporting
5. **Build**: Create distribution packages
6. **Release**: Automated or manual release to PyPI/Test PyPI

### Pipeline Parameters

- `BRANCH_NAME`: Branch to build (auto-detected if empty)
- `RELEASE_MODE`: auto/manual/skip
- `VERSION_TYPE`: patch/minor/major (for manual release)
- `DRY_RUN`: Test without publishing
- `SKIP_TESTS`: Skip test execution

### Release Strategy

- **main/master** → Production release to PyPI
- **develop/staging** → Beta release to Test PyPI
- **feature branches** → CI only, no release

## Version Management

This project follows [Semantic Versioning](https://semver.org/) and uses [Conventional Commits](https://www.conventionalcommits.org/).

### Commit Message Format

- `feat:` New feature (minor version bump)
- `fix:` Bug fix (patch version bump)
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Build process or auxiliary tool changes

Add `BREAKING CHANGE:` in the commit body for major version bumps.

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and quality checks
5. Submit a pull request

## Support

For issues and questions, please use the [GitHub Issues](https://github.com/yourusername/py-math-lib/issues) page.