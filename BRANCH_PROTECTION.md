# Branch Protection Policy

This document outlines the branch protection rules for the Exo Windows Fork project.

## Protected Branches

### Main Branch (`main`)
- **Status**: Fully protected
- **Purpose**: Production-ready code
- **Requirements**:
  - All tests must pass
  - Code review required (minimum 1 approval)
  - Status checks must pass
  - Branches must be up to date before merging

### Develop Branch (`develop`)
- **Status**: Protected
- **Purpose**: Integration and testing branch
- **Requirements**:
  - Tests must pass
  - Code review recommended
  - Status checks must pass

## Merge Requirements

### For Main Branch
1. **Code Review**: Minimum 1 approval from maintainers
2. **Tests**: All CI/CD tests must pass
3. **Documentation**: Changes must be documented
4. **Changelog**: Update CHANGELOG.md with changes

### For Develop Branch
1. **Tests**: All CI/CD tests must pass
2. **Code Quality**: No major linting issues
3. **Documentation**: Document significant changes

## Commit Message Guidelines

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Code change that improves performance
- **test**: Adding or updating tests
- **chore**: Changes to build process or dependencies

### Examples
```
feat(windows): Add GPU detection for Intel Arc

fix(service): Resolve caching issue in backend service

docs(readme): Update installation instructions for Windows 11

refactor(config): Simplify system configuration module
```

## Release Process

1. **Version Bump**: Update version in setup.py
2. **Changelog**: Add release notes to CHANGELOG.md
3. **Tag**: Create git tag (e.g., v0.0.2-windows)
4. **Release**: Create GitHub release with notes
5. **Announce**: Post release announcement

## Hotfix Branches

For critical bugs:
1. Create branch from `main`: `hotfix/issue-description`
2. Fix the issue
3. Test thoroughly
4. Create PR to `main`
5. Merge to `main` and `develop`

## Feature Branches

For new features:
1. Create branch from `develop`: `feature/feature-name`
2. Implement feature
3. Add tests
4. Update documentation
5. Create PR to `develop`
6. After review and testing, merge to `develop`

## Naming Conventions

- **Feature**: `feature/short-description`
- **Bugfix**: `bugfix/issue-number-description`
- **Hotfix**: `hotfix/critical-issue`
- **Documentation**: `docs/topic-description`
- **Refactor**: `refactor/area-description`

## Code Review Checklist

Reviewers should verify:
- [ ] Code follows project style guidelines
- [ ] Changes are well-documented
- [ ] Tests are included and passing
- [ ] No security vulnerabilities
- [ ] Performance impact is acceptable
- [ ] Breaking changes are documented
- [ ] Changelog is updated

## Continuous Integration

All branches are automatically tested with:
- Python 3.12+ compatibility
- Code linting (flake8)
- Module import tests
- Windows-specific tests

## Questions?

For questions about branch protection or contribution process, please:
1. Check CONTRIBUTORS.md
2. Review existing issues and PRs
3. Open a discussion or issue

---

**Last Updated**: December 2025
**Maintained By**: Exo Windows Team
