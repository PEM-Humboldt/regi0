# Regi0

Regi0 is a Python package with useful functions to complement and verify biological records. These functions are divided into two main modules (geographic and taxonomic) and rely on both user data and several web APIs (*e.g.* GNR, IUCN and Species+).

## Installation

Regi0 works with Python versions 3.7 through 3.9.

Using `pip`:
```shell
pip install regi0
```

Using `conda`:
```shell
conda install -c conda-forge
```

## Execution
To check whether the installation of `wiutils` was successful, execute the following command:

```shell
python -c "import regi0"
```
If this does not throw any error, the installation was successful.

You can use any `regi0` function by importing the package from a Python console or script. You can also execute flexible and predefined geographic and taxonomic verification workflows using `regi0`'s command line interface (CLI). For more information about the available functions and the CLI, check the [documentation](https://regi0.readthedocs.io).

## How to contribute

It is recommended to install the package using a [virtual environment](https://www.python.org/dev/peps/pep-0405/) to avoid tampering other Python installations in your system.

1. Clone this repo in your computer:
```shell
git clone https://github.com/PEM-Humboldt/regi0.git
```

2. Go to the project's root:
```shell
cd regi0
```

3. Install the package in development mode:
```shell
pip install --editable .[dev,docs,test]
```

Considering `regi0` has dependencies such as `fiona` and `rasterio`, which may require additional installation steps to the ones described above (see [1] and [2]), it is also recommended using a [`conda` virtual environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) to install it and avoid having to manually install other dependencies.

1. Go to the project's root and create the `conda` virtual environment:
```shell
conda env create -f environment.yml
```

2. Activate the `conda` virtual environment:
```shell
conda activate regi0-dev
```

3. Install the package in development mode:
```shell
pip install --editable .[dev,docs,test]
```

### Unit tests
Go to the project's root and execute:

```
pytest tests/
```

## Authors and contributors

* Erika Suarez-Valencia - [erikasv](https://github.com/erikasv)
* Helena Olaya-Rodríguez - [heleolaya](https://github.com/heleolaya)
* Marcelo Villa-Piñeros - [marcelovilla](https://github.com/marcelovilla)

## License
This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

[1]: https://github.com/Toblerity/Fiona#installation
[2]: https://github.com/mapbox/rasterio#installation
