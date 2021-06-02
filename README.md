# bdcc-tools
BDCC Tools: Biodiversity Data Cleaning and Curation Tools.

## Instalación

### Prerrequisitos
* [Python](https://www.python.org/downloads/) (v. 3.8+)

Si su sistema operativo es Windows, es necesario instalar primero tres dependencias a partir de sus distribuciones binarias:

* [`gdal`](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)
* [`Fiona`](https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona)
* [`rasterio`](https://www.lfd.uci.edu/~gohlke/pythonlibs/#rasterio)

Descargue los binarios más recientes correspondientes a la versión de Python y la arquitectura de su sistema (*i.e.* 32 o 64 bits). Una vez descargados, instale los binarios ejecutando los siguientes comandos (reemplazando por las rutas y archivos correspondientes):

```
pip install "C:\foo\bar\GDAL-3.3.0-cp39-cp39-win_amd64.whl"
pip install "C:\foo\bar\Fiona-1.8.20-cp39-cp39-win_amd64.whl"
pip install "C:\foo\bar\rasterio-1.2.4-cp39-cp39-win_amd64.whl"
```



Puede instalar `bdcctools` ejecutando el siguiente comando:

```
pip install git+https://github.com/PEM-Humboldt/bdcc-tools.git#egg=bdcctools
```

Si no tiene `git`, ejecute:

```
pip install --upgrade https://github.com/PEM-Humboldt/bdcc-tools/tarball/master
```

Para asegurarse que recovery haya quedado instalado, ejecute:

```
python -c "import bdcctools"
```

Si la instalación fue exitosa, el comando correrá sin ningún problema.


## Cómo contribuir

### Configuración del entorno de desarrollo
Para el desarrollo de recovery se utiliza `poetry`, un auxiliar de empaquetado y gestor de dependencias. Antes de continuar debe [instalarlo](https://python-poetry.org/docs/#installation)

Si su sistema operativo es Windows, es necesario instalar primero tres dependencias a partir de sus distribuciones binarias:

* [`gdal`](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal)
* [`Fiona`](https://www.lfd.uci.edu/~gohlke/pythonlibs/#fiona)
* [`rasterio`](https://www.lfd.uci.edu/~gohlke/pythonlibs/#rasterio)

Descargue los binarios más recientes correspondientes a la versión de Python y la arquitectura de su sistema (*i.e.* 32 o 64 bits). Una vez descargados, instale los binarios ejecutando los siguientes comandos (reemplazando por las rutas y archivos correspondientes):

```
poetry run pip install "C:\foo\bar\GDAL-3.3.0-cp39-cp39-win_amd64.whl"
poetry run pip install "C:\foo\bar\Fiona-1.8.20-cp39-cp39-win_amd64.whl"
poetry run pip install "C:\foo\bar\rasterio-1.2.4-cp39-cp39-win_amd64.whl"
```

En primer lugar, es necesario clonar este repositorio localmente. Para esto, ejecute:

```
git clone https://github.com/PEM-Humboldt/bdcctools.git
```

 Luego, ubíquese dentro de del directorio del proyecto:
 
 ```
cd bdcctools
```

e instale todas las dependencias necesarias:

```
poetry install
```

El entorno de desarrollo está listo y todas las dependencias necesarias están instaladas. En caso de necesitar agregar nuevas dependencias, ejecute:

```
poetry add <dependencia>
poetry update
```

Es recomendable familiarizarse con la [documentación](https://python-poetry.org/docs/) de `poetry`.

### Ejecución de pruebas unitarias
Ubicado dentro del proyecto, ejecute:

```
poetry run pytest tests/
```
