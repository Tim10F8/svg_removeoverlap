# Contributing to svg_removeoverlap

Thank you for considering contributing to `svg_removeoverlap`! We welcome any contributions that can help improve this project.

## How to Contribute

### Reporting Bugs
- If you find a bug, please open an issue on the GitHub repository.
- Describe the bug in detail, including:
    - Steps to reproduce the bug.
    - Expected behavior.
    - Actual behavior.
    - Your operating system and Python version.
    - Version of `svg_removeoverlap` you are using.
    - Sample SVG file that triggers the bug, if possible.

### Suggesting Enhancements
- If you have an idea for a new feature or an improvement to an existing one, please open an issue on GitHub.
- Describe your suggestion clearly and explain why it would be beneficial.

### Code Contributions
1.  **Fork the Repository:** Start by forking the [official repository](https://github.com/twardoch/svg_removeoverlap) on GitHub.
2.  **Clone Your Fork:** Clone your forked repository to your local machine.
    ```bash
    git clone https://github.com/YOUR_USERNAME/svg_removeoverlap.git
    cd svg_removeoverlap
    ```
3.  **Create a Branch:** Create a new branch for your changes.
    ```bash
    git checkout -b feature/your-feature-name
    ```
    or
    ```bash
    git checkout -b bugfix/issue-number
    ```
4.  **Set Up Development Environment:**
    - It's recommended to use a virtual environment:
      ```bash
      python3 -m venv .venv
      source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
      ```
    - Install dependencies, including development tools:
      ```bash
      pip install -e .[testing]
      pip install pre-commit  # If not already installed globally
      pre-commit install
      ```
5.  **Make Your Changes:**
    - Write clean, readable, and well-commented code.
    - Follow the existing code style (primarily Black and Flake8, enforced by pre-commit hooks).
    - Add tests for any new functionality or bug fixes. Ensure all tests pass by running `pytest`.
      ```bash
      pytest
      ```
6.  **Commit Your Changes:**
    - Make sure your commit messages are clear and descriptive.
    - Ensure pre-commit hooks pass before committing.
7.  **Push to Your Fork:**
    ```bash
    git push origin feature/your-feature-name
    ```
8.  **Open a Pull Request (PR):**
    - Go to the original `svg_removeoverlap` repository and open a Pull Request from your forked branch.
    - Provide a clear description of your changes in the PR.
    - Link any relevant issues.

## Code Style
- This project uses [Black](https://github.com/psf/black) for code formatting and [Flake8](https://flake8.pycqa.org/en/latest/) for linting. These are enforced by pre-commit hooks.
- Type hints are encouraged.

## Testing
- Tests are written using [pytest](https://docs.pytest.org/).
- Please ensure that your changes include appropriate tests and that all existing and new tests pass.

## Questions?
If you have any questions, feel free to open an issue or reach out to the maintainers.

Thank you for your contribution!
