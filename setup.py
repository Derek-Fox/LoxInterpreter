from setuptools import setup, find_packages

setup(
    name="pylox",
    version="1.0",
    description="Interpreter for Lox written in Python",
    author="Derek Fox",
    author_email="derekefox@gmail.com",
    url="https://github.com/Derek-Fox/PythonLoxInterpreter",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
      "console_scripts": [
          "pylox=run.main:main",
      ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
