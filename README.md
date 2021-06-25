# bdcc-tools
BDCC Tools: Biodiversity Data Cleaning and Curation Tools.

`bdcctools` tiene funciones útiles para la verificación geográfica y taxonómica de registros biológicos.

## Instalación

Con `pip`:
```shell

```

Con `conda`:
```shell

```


## Cómo contribuir

1. Clone este repositorio en su máquina:
```shell
git clone https://github.com/PEM-Humboldt/bdcc-tools.git
```

2. Ubíquese en la raíz del proyecto:
```shell
cd bdcc-tools
```

3. Instale el paquete en modo de desarrollo:
```shell
pip install --editable .[dev,test]
```

Se recomienda que la instalación del paquete en modo de desarrollo se haga en un [entorno virtual](https://www.python.org/dev/peps/pep-0405/) para no alterar otras instalaciones existentes de Python en el sistema.

Teniendo en cuenta que `bdcctools` tiene dependencias como `fiona`, `gdal` y `rasterio`, las cuales pueden necesitar pasos adicionales (ver [1] y [2]) a los anteriores para su instalación, se recomienda utilizar un [entorno virtual de `conda`](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) para instalar `bdcctools` en modo de desarrollo y evitar la instalación manual de algunas dependencias.

1. Para crear el entorno virtual de `conda`, ubíquese en la raíz del proyecto y ejecute:
```shell
conda env create -f environment.yml
```

2. Active el entorno virtual recién creado:
```shell
conda activate bdcctools-dev
```

3. Instale el paquete en modo de desarrollo:
```shell
pip install --editable .[dev,test]
```

### Ejecución de pruebas unitarias
Ubicado dentro del proyecto, ejecute:

```
pytest tests/
```


[1]: https://github.com/Toblerity/Fiona#installation
[2]: https://github.com/mapbox/rasterio#installation