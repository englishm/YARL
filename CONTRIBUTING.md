# How to Contribute to YARL

1. Find an issue you would like to work on and get it assigned to you. You can also create an issue to describe your proposed feature or bugfix.
2. Fork the repository.
3. Create a branch for your contribution (see [Branch Naming Guidelines](##branch-naming-guidelines) below).
4. Develop your contribution.
5. When finished, push and create a pull request to merge your contribution into the `develop` branch.
6. Your contribution will be checked by Travis CI and one of the maintainers.
7. If approved, your contribution will be merged with `develop`, and will eventually be released on `master`.

## Branch Naming Guidelines

**Features:** name your branch `feature/descriptive-name`.

**Bugfixes:** name your branch `bugfix/descriptive-name`.

**Hotfixes:** name your branch `hotfix/descriptive-name`. Hotfixes are special and should be pull-requested/merged with `master`.

## Style Guidelines

For all Python code, the [PEP-8](https://www.python.org/dev/peps/pep-0008/) style guide should be followed. Use descriptive variable names. Travis CI will be linting for PEP-8.

Include comments when your code is not self-explanatory. [Docstrings](https://www.python.org/dev/peps/pep-0257/) at the beginning of functions and classes are generally a good idea.
