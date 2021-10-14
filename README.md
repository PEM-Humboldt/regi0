# Regi0

`regi0` tiene funciones útiles para la verificación geográfica y taxonómica de registros biológicos.

## Instalación

Con `pip`:
```shell
pip install regi0
```

Con `conda`:
```shell

```

## Ejecución
Para asegurarse que la instalación de `regio` fue satisfactoria ejecute el siguiente comando:

```shell
python -c "import regi0"
```
Si el comando no arroja ningún error, la instalación fue satisfactoria.

Puede acceder a las funciones de `regi0` importando el paquete desde una consola o un script de Python. Para mayor información sobre las funciones disponibles, consulte la [documentación](https://regi0.readthedocs.io).

`regi0` también ofrece una interfaz de línea de comando (CLI) construida sobre las funciones disponibles para ejecutar flujos predefinidos de verificación geográfica y taxonómica sobre registros biológicos. Puede consultar más información sobre esta interfaz [acá](regi0/cli/README.md) o en la [documentación](https://regi0.readthedocs.io).


## Cómo contribuir

1. Clone este repositorio en su máquina:
```shell
git clone https://github.com/PEM-Humboldt/regi0.git
```

2. Ubíquese en la raíz del proyecto:
```shell
cd regi0
```

3. Instale el paquete en modo de desarrollo:
```shell
pip install --editable .[dev,docs,test]
```

Se recomienda que la instalación del paquete en modo de desarrollo se haga en un [entorno virtual](https://www.python.org/dev/peps/pep-0405/) para no alterar otras instalaciones existentes de Python en el sistema.

Teniendo en cuenta que `regi0` tiene dependencias como `fiona`, `gdal` y `rasterio`, las cuales pueden necesitar pasos adicionales (ver [1] y [2]) a los anteriores para su instalación, se recomienda utilizar un [entorno virtual de `conda`](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) para instalar `regi0` en modo de desarrollo y evitar la instalación manual de algunas dependencias.

1. Para crear el entorno virtual de `conda`, ubíquese en la raíz del proyecto y ejecute:
```shell
conda env create -f environment.yml
```

2. Active el entorno virtual recién creado:
```shell
conda activate regi0-dev
```

3. Instale el paquete en modo de desarrollo:
```shell
pip install --editable .[dev,docs,test]
```

### Ejecución de pruebas unitarias
Ubicado dentro del proyecto, ejecute:

```
pytest tests/
```

## Autores y contribuidores

* Erika Suarez-Valencia - [erikasv](https://github.com/erikasv)
* Helena Olaya-Rodríguez - [heleolaya](https://github.com/heleolaya)
* Marcelo Villa-Piñeros - [marcelovilla](https://github.com/marcelovilla)

## Licencia
Este paquete tiene una licencia MIT. Ver [LICENSE.txt](LICENSE.txt) para más información.


[1]: https://github.com/Toblerity/Fiona#installation
[2]: https://github.com/mapbox/rasterio#installation