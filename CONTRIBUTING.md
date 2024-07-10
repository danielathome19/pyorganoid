# Contributing to PyOrganoid

Thank you for your interest in contributing to PyOrganoid! Your contributions help improve the library and make it more useful for everyone. Here are some guidelines to get you started.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Contributing Code](#contributing-code)
- [Development Setup](#development-setup)
  - [Installing Dependencies](#installing-dependencies)
  - [Running Tests](#running-tests)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

## How to Contribute

### Reporting Bugs

If you find a bug, please report it by opening an issue on GitHub. Include as much detail as possible, including:
- Steps to reproduce the bug
- Expected and actual results
- Any relevant code snippets or error messages

### Suggesting Features

We welcome feature suggestions! If you have an idea, please open an issue and describe:
- The feature you would like to see
- Why you think it would be useful
- How it could be implemented

### Contributing Code

1. Fork the repository.
2. Create a new branch from the `main` branch.
3. Make your changes.
4. Write tests for your changes.
5. Ensure all tests pass.
6. Commit your changes with a descriptive commit message.
7. Push your branch to your forked repository.
8. Open a pull request.

## Development Setup

### Installing Dependencies

1. Clone the repository:
    ```sh
    git clone https://github.com/danielathome19/pyorganoid.git
    cd pyorganoid
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Running Tests

To run the tests, use the following command:
```sh
pytest tests
```

Ensure that all tests pass before submitting a pull request.


### Building the Documentation

To build the documentation, use the following commands:
```sh
sphinx-apidoc -o docs/ pyorganoid/
mv docs/modules.rst docs/source
mv docs/pyorganoid.rst docs/source
cd docs
make clean
make html
```


## Pull Request Process

1. Ensure your code follows the style guide.
2. Make sure all tests pass.
3. Open a pull request and provide a detailed description of your changes.
4. Wait for a project maintainer to review your pull request. You may be asked to make additional changes.

## Style Guide

* Follow PEP 8 for Python code.
* Use meaningful variable and function names.
* Write clear and concise comments where necessary.
* Ensure your code is well-documented.

Thank you for your contributions! If you have any questions, feel free to reach out by opening an issue on GitHub.
