# Dependency Checker for Package.json

This Python script helps to identify dependency confusion vulnerabilities in your project. It takes a `package.json` file, extracts all dependencies, and checks if each package is hosted properly. This tool is useful for ensuring that your dependencies are secure and correctly managed.

## Features

- **Extracts Dependencies**: Reads `package.json` and extracts all dependencies.
- **Checks Package Hosting**: Verifies if each package is correctly hosted to avoid dependency confusion vulnerabilities.

## Prerequisites

- Python 3.6 or higher
- Required Python packages: `requests`, `colorama`

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/gurudattch/dependancer
    ```

2. **Navigate to the project directory:**

    ```bash
    cd dependancer
    ```

3. **Install required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place your `package.json` file in the same directory as the script.

2. Run the script with the following command:

    ```bash
    python main.py -f package.json
    ```

3. The script will output the status of each dependency and report any issues with hosting.

## Configuration

The script assumes that `package.json` is in the same directory. You can modify the script to specify a different path if needed.
