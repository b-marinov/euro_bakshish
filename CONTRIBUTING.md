# Contributing to Euro Bakshish

Thank you for your interest in contributing to Euro Bakshish! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect different viewpoints and experiences

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, browser, versions)

### Suggesting Features

1. Check if the feature has been requested in Issues
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Code Contributions

#### Setup Development Environment

Follow the setup guide in `docs/SETUP.md`

#### Coding Standards

**Python (Backend)**
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Write unit tests for new features
- Keep functions focused and small

**JavaScript/React (Web)**
- Use ES6+ syntax
- Follow Airbnb JavaScript Style Guide
- Use functional components with hooks
- Add PropTypes or TypeScript types
- Write meaningful component names

**Kotlin (Android)**
- Follow Kotlin coding conventions
- Use meaningful class and variable names
- Add KDoc comments for public APIs
- Follow MVVM architecture pattern
- Use coroutines for async operations

#### Git Workflow

1. Fork the repository
2. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Write/update tests
5. Ensure all tests pass
6. Commit with clear messages:
   ```bash
   git commit -m "Add feature: description of feature"
   ```
7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
8. Create a Pull Request

#### Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when relevant

Examples:
```
Add user profile page
Fix login authentication bug
Update trip creation API endpoint
Refactor dashboard component
```

#### Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update README.md if needed
5. Request review from maintainers
6. Address review feedback
7. Squash commits if requested

#### Testing

**Backend Tests**
```bash
cd backend
pytest
```

**Web Tests**
```bash
cd web
npm test
```

**Coverage**
Aim for >80% code coverage for new code

#### Documentation

- Update relevant documentation when changing features
- Add inline comments for complex logic
- Update API documentation for endpoint changes
- Keep README files up to date

## Project Structure

See `docs/ARCHITECTURE.md` for detailed architecture information.

## Questions?

Feel free to:
- Open an issue for questions
- Reach out to maintainers
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

## Recognition

Contributors will be recognized in the project README and release notes.

Thank you for contributing to Euro Bakshish! 🚗🌟
