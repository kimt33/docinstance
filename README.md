# docinstance

Docinstance is a package for managing docstrings as instances of a Python
object, Docstring, rather than string literals. The goal of this package is to
develop a framework that allows us to painlessly construct and modify docstrings
in different styles.

## Features
Since this is a work in progress, we list the intended features of this module:

- [ ] Parse docstring into Docstring instances
  - [x] numpy docstring
  - [ ] google docstring
  - [ ] sphinx's rst docstring
- [ ] Write docstring from Docstring instance
  - [x] numpy docstring
  - [x] google docstring
  - [x] sphinx's rst docstring
- [ ] Translate docstrings from one style to another
  - [x] numpy to google or sphinx's rst style
- [ ] Inherit (parts of) docstrings
  - [ ] from parent
  - [ ] from other objects
- [ ] Generate docstring from code
  - [ ] List of parameters
  - [ ] List of methods/properties in a class
  - [ ] List of functions/classes in a module
- [ ] Generate code from docstring
  - [ ] static type checking
- [ ] Interface to IDE's
  - [ ] Vim
  - [ ] Emacs

## Getting Started

These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes. See deployment for notes on
how to deploy the project on a live system.

### Prerequisites

To use this module, no other packages are needed except for the standard Python
library for Python 3.

For testing, `pytest` is the only prerequisite.
```shell
pip install pytest
```

For quality assurance, `tox` is used along side `pytest`, `pytest-cov`,
`flake8`, `pylint`, `pydocstyle`, and `pycodestyle`.
```shell
pip install tox
pip install pytest
pip install pytest-cov
pip install flake8
pip install pylint
pip install pydocstyle
pip install pycodestyle
```

### Installing

To install the package from PyPI, use pip:
```shell
pip install docinstance
```

To install the package from source, download the package using git, then install
using pip:
```shell
git clone https://github.com/kimt33/docinstance.git
cd docinstance
pip install -e ./
```

## Running the tests

To test the code, run pytest from the package directory.
```shell
cd /path/to/docinstance/
pytest
```

## Running the quality assurance tests

To run quality assurance, run tox  from the package directory
```shell
cd /path/to/docinstance/
tox
```

Note that if you do not have different versions of Python installed, you may
need to specify the python version.
```shell
tox -e py37
tox -e py36
tox -e py35
```

## Contributing

Please read
[CONTRIBUTING.md](https://github.com/kimt33/docinstance/CONTRIBUTING.md) for
details on our code of conduct, and the process for submitting pull requests to
us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available,
see the [tags on this repository](https://github.com/kimt33/docinstance/tags).

## Authors

* **Taewon David Kim** - *Initial work* - [kimt33](https://github.com/kimt33)

See also the list of
[contributors](https://github.com/kimt33/docinstance/contributors) who
participated in this project.

## License

This project is licensed under the GPLv3 License - see the
[LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This README was templated from
  [PurpleBooth/README-Template.md](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* Inspiration
* etc
