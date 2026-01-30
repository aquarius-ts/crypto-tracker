# Contributing to Crypto Real-Time Price Tracker

Thank you for considering contributing to this project! Here are some guidelines to help you get started.

## How to Contribute

1. **Fork the Repository**
   - Click the "Fork" button at the top right of the repository page

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd YOUR_REPO
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**
   - Write clean, readable code
   - Follow PEP 8 style guidelines
   - Add comments where necessary
   - Update documentation if needed

5. **Test Your Changes**
   ```bash
   # Run tests
   pytest
   
   # Check code style
   flake8 .
   
   # Security scan
   bandit -r .
   ```

6. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add: your descriptive commit message"
   ```

7. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Describe your changes
   - Submit the PR

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Maximum line length: 127 characters

## Commit Messages

Use clear and descriptive commit messages:
- `Add: new feature`
- `Fix: bug description`
- `Update: what was updated`
- `Refactor: what was refactored`
- `Docs: documentation changes`

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for good code coverage

## Bug Reports

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages (if any)

## Feature Requests

When requesting features, please:
- Describe the feature clearly
- Explain why it would be useful
- Provide examples if possible

## Questions?

Feel free to open an issue for any questions or discussions.

Thank you for contributing! 🎉
