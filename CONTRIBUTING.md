# Contributing to Learning Path Advisor Pro

Thank you for your interest in contributing to Learning Path Advisor Pro! This document provides guidelines and instructions for contributing.

## 🤝 Code of Conduct

Please be respectful and professional in all interactions. We aim to maintain a welcoming and inclusive environment for all contributors.

## 🚀 Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/goal-planning-aiAgent.git
   cd goal-planning-aiAgent
   ```
3. **Set up development environment**
   ```bash
   python setup.py
   ```

## 💻 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or updates

### 2. Make Your Changes

- Write clean, readable code
- Follow existing code style and conventions
- Add comments for complex logic
- Update documentation as needed

### 3. Test Your Changes

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=learning-path-advisor/backend --cov-report=html

# Test specific file
pytest tests/test_api.py -v
```

All tests must pass before submitting a pull request.

### 4. Commit Your Changes

```bash
git add .
git commit -m "Brief description of changes"
```

Commit message guidelines:
- Use present tense ("Add feature" not "Added feature")
- First line should be 50 characters or less
- Reference issues and pull requests when relevant

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear description of changes
- Reference to related issues
- Screenshots (if UI changes)
- Testing steps

## 📝 Code Style Guidelines

### Python Code

- Follow PEP 8 style guide
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use meaningful variable and function names

Example:
```python
def calculate_learning_path(
    start_courses: List[str],
    goal_course: str,
    learning_style: str = "balanced"
) -> Dict[str, Any]:
    """
    Calculate optimal learning path.
    
    Args:
        start_courses: List of completed courses
        goal_course: Target course to reach
        learning_style: Optimization strategy
        
    Returns:
        Dictionary containing path details
    """
    pass
```

### JavaScript Code

- Use modern ES6+ syntax
- Use `const` and `let`, avoid `var`
- Use meaningful variable names
- Add JSDoc comments for functions

Example:
```javascript
/**
 * Fetch learning path from API
 * @param {string[]} startCourses - Completed courses
 * @param {string} goalCourse - Target course
 * @returns {Promise<Object>} Learning path data
 */
async function fetchLearningPath(startCourses, goalCourse) {
    // Implementation
}
```

## 🧪 Testing Guidelines

- Write tests for new features
- Update tests for modified features
- Aim for high test coverage (>80%)
- Test both success and error cases

Example:
```python
def test_learning_path_calculation():
    """Test learning path endpoint with valid input"""
    payload = {
        'start_courses': ['Python Basics'],
        'goal_course': 'Machine Learning',
        'learning_style': 'balanced'
    }
    response = client.post('/api/path', json=payload)
    assert response.status_code == 200
    assert 'path' in response.json
```

## 📚 Documentation

- Update README.md for user-facing changes
- Add docstrings to all functions and classes
- Update API documentation for endpoint changes
- Add comments for complex algorithms

## 🐛 Bug Reports

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Error messages and stack traces
- Screenshots if applicable

## ✨ Feature Requests

For feature requests, please include:
- Clear description of the feature
- Use cases and benefits
- Potential implementation approach
- Any relevant examples or references

## 🔍 Code Review Process

All contributions go through code review:
1. Automated tests must pass
2. Code style must be consistent
3. Documentation must be updated
4. At least one maintainer approval required

## 📋 Pull Request Checklist

Before submitting, ensure:
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No unnecessary files included
- [ ] Branch is up to date with main

## 🎯 Areas for Contribution

Looking for ideas? Consider:

### Backend
- Additional pathfinding algorithms
- New decision strategies
- Performance optimizations
- Database improvements
- API enhancements

### Frontend
- UI/UX improvements
- Mobile responsiveness
- Accessibility features
- Visualization enhancements
- Dark mode

### Documentation
- Tutorial creation
- API examples
- Video guides
- Translation to other languages

### Testing
- Increase test coverage
- Integration tests
- Performance tests
- UI tests

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## 📞 Questions?

- Open an issue for questions
- Tag with `question` label
- Be specific and provide context

Thank you for contributing to Learning Path Advisor Pro! 🚀
