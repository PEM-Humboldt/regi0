Installation
============

Regi0 works with Python versions 3.7 through 3.9.

--------------
Stable release
--------------
There are two options to install the stable release of :code:`regi0`:

1. Install from `PyPI <https://pypi.org/project/regi0/>`_ using :code:`pip`:

.. code:: bash

   pip install regi0

Keep in mind that :code:`regi0` relies on libraries such as :code:`geopandas`, :code:`fiona` and :code:`rasterio` which require GDAL. Depending on your OS, you might need to install additional system libraries before installing :code:`regi0`. Refer to `Fiona's <https://fiona.readthedocs.io/en/latest/README.html#installation>`_ or `Rasterio's <https://rasterio.readthedocs.io/en/latest/installation.html#installation>`_ installation guides for more information.

2. Install from conda-forge using :code:`conda`:

.. code:: bash

   conda install -c conda-forge regi0

-----------
From source
-----------
There are two options to install :code:`wiutils` from source:

1. Install from the `GitHub repository <https://github.com/PEM-Humboldt/regi0>`_ using :code:`pip` and :code:`git`:

.. code:: bash

   pip install git+https://github.com/PEM-Humboldt/regi0.git#egg=regi0


2. Install from the `GitHub repository <https://github.com/PEM-Humboldt/regi0>`_ using :code:`pip`:

.. code:: bash

   pip install --upgrade https://github.com/PEM-Humboldt/regi0/tarball/master
