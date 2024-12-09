from setuptools import setup, find_packages

setup(
    name="pylox",  # Your package name
    version="0.1.0",  # Initial version
    description="Interpreter for Lox written in Python",
    author="Derek Fox",
    author_email="derekefox@gmail.com",
    url="https://github.com/Derek-Fox/PythonLoxInterpreter",  # Replace with your project URL
    packages=find_packages(where="src"),  # Automatically find all packages in the 'src' directory
    package_dir={"": "src"},  # Define the root directory for packages
    entry_points={
      "console_scripts": [
          "pylox=pylox.main:main",
      ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",  # Specify compatible Python versions
)
