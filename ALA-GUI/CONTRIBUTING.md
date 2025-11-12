# Contributing to ALA-GUI

Thank you for your interest in contributing to ALA-GUI! This document provides guidelines for contributing to the project.

## Development Process

### 1. Setup Development Environment

Follow the [SETUP.md](docs/SETUP.md) guide to set up your development environment.

```bash
# Clone repository
git clone https://github.com/tygwan/ALA-AutoLabelAgent.git
cd ALA-AutoLabelAgent/ALA-GUI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pip install pre-commit
pre-commit install
```

### 2. Create a Feature Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 3. Development Workflow (TDD)

Follow Test-Driven Development methodology:

**RED → GREEN → REFACTOR → COMMIT**

1. **RED**: Write a failing test
   ```python
   def test_new_feature():
       result = new_feature()
       assert result == expected_value
   ```

2. **GREEN**: Write minimal code to pass test
   ```python
   def new_feature():
       return expected_value
   ```

3. **REFACTOR**: Improve code while tests pass
   ```python
   def new_feature():
       # Refactored implementation
       return calculate_result()
   ```

4. **COMMIT**: Commit with conventional commit message
   ```bash
   git add .
   git commit -m "feat(module): add new feature"
   ```

### 4. Code Quality Checks

Before committing, ensure all checks pass:

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
flake8 src/ tests/
pylint src/

# Type check
mypy src/

# Security scan
bandit -r src/

# Run tests
pytest

# Run all checks at once
pre-commit run --all-files
```

### 5. Commit Your Changes

Use conventional commit messages:

**Format**: `<type>(<scope>): <subject>`

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes

**Examples**:
```bash
git commit -m "feat(ui): add image canvas zoom functionality"
git commit -m "fix(model): resolve SAM2 memory leak"
git commit -m "docs(readme): update installation instructions"
git commit -m "test(annotation): add unit tests for polygon tool"
```

### 6. Push and Create Pull Request

```bash
# Push branch
git push origin feature/your-feature-name

# Create pull request on GitHub
# Fill out the PR template with:
# - Description of changes
# - Related issues
# - Test results
# - Screenshots (if UI changes)
```

## Code Style Guidelines

Follow the [STYLEGUIDE.md](docs/STYLEGUIDE.md) for detailed code style guidelines.

### Key Points

- **Line Length**: 88 characters (Black default)
- **Imports**: Organized by isort (stdlib → third-party → local)
- **Type Hints**: Required for all function signatures
- **Docstrings**: Google-style for all public APIs
- **Naming**: PascalCase (classes), snake_case (functions/variables)

## Testing Guidelines

Follow the [TESTING.md](docs/TESTING.md) for comprehensive testing guidelines.

### Test Categories

**Unit Tests** (90%+ coverage):
- Fast, isolated tests
- Mock external dependencies
- One assertion per test

**Integration Tests** (70%+ coverage):
- Test component interactions
- Use real file I/O where appropriate
- Test cross-module communication

**E2E Tests** (50%+ coverage):
- Test complete user workflows
- Use qtbot for GUI interaction
- Test critical user paths

### Running Tests

```bash
# All tests
pytest

# Specific category
pytest -m unit
pytest -m integration
pytest -m e2e

# With coverage
pytest --cov=src --cov-report=html

# Specific file
pytest tests/unit/test_project_manager.py

# Verbose output
pytest -v
```

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass locally
- [ ] Code formatted with Black
- [ ] Imports sorted with isort
- [ ] No linting errors (flake8)
- [ ] No type checking errors (mypy)
- [ ] Test coverage meets targets
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #123

## How Has This Been Tested?
- [ ] Unit tests
- [ ] Integration tests
- [ ] E2E tests
- [ ] Manual testing

## Test Coverage
- Current coverage: X%
- Coverage change: +Y%

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## Code Review Process

### For Reviewers

1. **Check Tests**: Ensure adequate test coverage
2. **Verify Code Quality**: Confirm style guidelines followed
3. **Test Functionality**: Pull branch and test locally
4. **Review Logic**: Check for bugs and edge cases
5. **Provide Feedback**: Be constructive and specific

### For Authors

1. **Respond to Feedback**: Address all comments
2. **Update PR**: Push changes to same branch
3. **Request Re-review**: After addressing feedback
4. **Merge**: Wait for approval before merging

## CI/CD Pipeline

### Automated Checks

Every push and PR triggers:

1. **Linting**: flake8, pylint
2. **Type Checking**: mypy
3. **Security Scan**: bandit
4. **Tests**: pytest with coverage
5. **Build**: Package creation

### Required Status Checks

Before merging, ensure:
- ✅ All tests pass
- ✅ Code quality checks pass
- ✅ Coverage meets targets (70%+)
- ✅ Security scan passes
- ✅ At least one approving review

## Project Structure

```
ALA-GUI/
├── src/
│   ├── models/          # Data models
│   ├── views/           # PyQt6 UI components
│   ├── controllers/     # Business logic
│   └── utils/           # Utility functions
├── tests/
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── e2e/             # End-to-end tests
├── docs/                # Documentation
└── examples/            # Example code
```

## Milestone Development

Current development follows milestones from [PLAN.md](../PLAN.md):

- **M0**: Project Setup ✅
- **M1**: Foundation & Core Infrastructure (Current)
- **M2**: PyQt6 Image Display & Navigation
- **M3**: Model Integration
- **M4**: Annotation Tools
- **M5**: Web Integration
- **M6**: Pipeline Integration
- **M7**: Polish & UX
- **M8**: Deployment

## Communication

### Reporting Issues

Use GitHub Issues with appropriate labels:

- `bug`: Something isn't working
- `enhancement`: New feature request
- `documentation`: Documentation improvement
- `question`: Further information needed
- `good first issue`: Good for newcomers

### Feature Requests

Before submitting feature requests:

1. Check existing issues
2. Verify alignment with project goals
3. Provide detailed use case
4. Consider implementation complexity

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Check [docs/](docs/) for detailed guides
- Review [README.md](README.md) for project overview
- Open an issue for questions

## Thank You!

Your contributions make ALA-GUI better for everyone. We appreciate your time and effort! 🙏

---

**Last Updated**: 2025-01-13
**M0: Project Setup**
