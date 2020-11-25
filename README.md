# geographic-validation
Este repositorio contiene funciones comunes para la validación geográfica de registros biológicos. Adicionalmente, contiene una interfaz de consola para correr un proceso completo de validación geográfica, el cual utiliza todas las funciones comunes expuestas. Este proceso de validación está basado en el [trabajo](https://github.com/LBAB-Humboldt/GEOGRAPHICAL_VERIFICATIONS) de:

> Bello, C., O. Ramos., A.C. Moreno-Ramírez., J. Velázquez-Tibatá., M.C. Londoño-Murcia. 2012. Protocolo para  ejecutar el script de R para laverificación geográfica de registros biológicos en Colombia, Venezuela,Panamá, Ecuador, Brasil y  Perú.Laboratorio de  Biogeografía y Bio-acustica (LABB).Instituto de Investigación de Recursos Biológicos Alexander von Humboldt. Bogotá D.C., Colombia. 23 p. 

El flujo de trabajo consiste en:

1. Leer una tabla con registros biológicos y eliminar datos que no tengan coordenadas geográficas.
2. Comparar la información de país, departamento y municipio contra los límites politico-administrativos históricos.
3. Identificar registros ubicados en zonas urbanas.
4. Extraer valores de elevación para todos los registros e identificar valores anómalos.
5. Identificar duplicados espaciales.
6. Guardar una copia o subconjunto de los registros originales con nuevas columnas que contienen los resultados de la validación.

## Por dónde empezar
A continuación se presentan las instrucciones para la ejecución local de la validación geográfica.

### Prerrequisitos
La interfaz de consola y las funciones comunes de validación geográfica están desarrolladas completamente en Python. Por esta razón, es necesario tener instalado un intérprete de Python (versión 3.6 o superior) para su ejecución. Puede instalar una de las siguientes alternativas:

* [Anaconda](https://www.anaconda.com/products/individual)
* [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (Recomendado)
* [Python](https://www.python.org/downloads/)

Por lo pronto, las capas geográficas utilizadas durante la validación deben estar presentes de manera local. Puede descargar una copia de las capas utilizadas [acá](https://drive.google.com/file/d/1lqb-FOJUOP-L_r3eEnxAVswqFtysnBPW/view?usp=sharing).

### Instalación
Clone este repositorio en su máquina utilizando `git`:

```
git clone https://github.com/PEM-Humboldt/geographic-validation.git
```

Si no tiene `git`, también puede descargar el proyecto haciendo click [acá](https://github.com/PEM-Humboldt/geographic-validation/archive/master.zip).

Para evitar conflictos con otras posibles instalaciones de Python que pueda tener, es necesario crear un entorno virtual para ejecutar la herramienta. Dependiendo si instaló Python o Anaconda/Miniconda, siga los pasos correspondientes mostrados a continuación.

#### Anaconda o Miniconda
Para crear el entorno virtual con todos los paquetes, abra una terminal en la raíz del proyecto y ejecute el siguiente comando:

```
conda env create -f environment.yml
```

Con este comando se instalará un entorno llamado `gv-env`. A partir de ahora, cada vez que ejecute la herramienta deberá activar el entorno con el siguiente comando:

```
conda activate gv-env
```


#### Python

Para crear el entorno virtual, abra una terminal en la raíz del proyecto y ejecute el siguiente comando:

```
python -m venv gv-env
```

Para instalar los paquetes necesarios en el entorno virtual recién creado , active el entorno virtual ejecutando alguno de los siguientes comando dependiendo de su sistema operativo.

Para sistemas Unix (MacOS y Linux):
```
source hf-indicators/bin/activate
```

Para sistemas Windows:
```
hf-indicators\Scripts\act
```

Una vez activado el entorno virtual, ejecute el siguiente comando para instalar los paquetes necesarios:

```
python -m pip install -r requirements.txt
```

 A partir de ahora, cada vez que ejecute la herramienta deberá activar el entorno con uno de los dos comandos mencionados previamente.

### Ejecución
Como se mencionó anteriormente, el proceso completo de validación geográfica está expuesto mediante una interfaz de línea de comandos (CLI), lo cual quiere decir que se ejecuta desde una terminal. Para ejecutar la herramienta debe activar el entorno virtual creado. Una vez activado el entorno, puede ejecutar la herramienta desde la raíz del proyecto mediante el siguiente comando:

```
python src/main.py -h
```

Si la instalación fue exitosa, este comando mostrará un mensaje de ayuda sobre cómo utilizar la herramienta.

```
Geographic validation tool. Performs a complete geographic validation on a dataset of biological records and saves a copy or a subset of the original file with
the corresponding new columns.

positional arguments:
  src         Absolute or relative path of the input table. Only csv and xlsx files are supported.
  dst         Absolute or relative path of the output table. Only csv files are supported.

optional arguments:
  -h, --help  show this help message and exit
  -crs CRS    Input coordinate reference system in the form epsg:code. Default is epsg:4326
  --drop      Drop records with positive flags.
```

Como puede ver, la herramienta recibe dos argumentos posicionales:

* `src`: ruta absoluta o relativa del archivo de entrada con los registros. Por ahora solo se soportan archivos csv o xlsx.
* `dst`: ruta absoluta o relativa del archivo de salida. El archivo de salida debe ser csv.

Adicionalmente, la herramienta recibe dos argumentos opcionales:

* `-crs`: sistema de referencia de los registros. Debe ser en la forma epsg:codigo. Por defecto, se utiliza el sistema de referencia 4326.
* `--drop`: elimina los registros que tengan algún flag positivo en el archivo de salida. Si no especifica este argumento, se mantendrán todos los registros.

<hr>

Suponga que tiene un archivo con registros de aves en su carpeta de descargas y quiere ejecutar la validación geográfica sobre este archivo. Un ejemplo de comando para ejecutar la herramienta es el siguiente:

```
python src/main.py ~/Downloads/avesEndemicas.csv  ~/resultadoValidacionGeografica.csv
```

Al ejecutar este comando, se creará un archivo de resultados con el nombre `resultadoValidacionGeografica.csv`.

Suponga que ahora quiere ejecutar la validación geográfica sobre un archivo con registros de mamíferos cuyas coordenadas están en MAGNA SIRGAS con origen Bogotá. Adicionalmente, quiere eliminar aquellos registros con flags positivos. Puede utilizar el siguiente comando:

```
python src/main.py ~/Downloads/mamiferos.csv  ~/resultado.csv -crs epsg:3116 --drop
```

Al ejecutar este comando, se creará un archivo de resultados con el nombre `resultado.csv`. Además de las columnas resultantes de la validación, el archivo tendrá solo aquellos registros que no hayan obtenido ningún flag posittivo durante el proceso.

### Configuración
Aparte de los parámetros que la interfaz de consola recibe, es posible configurar otras opciones de la herramienta. Para esto está el archivo `config/settings.ini`. Este consiste en 9 secciones con múltiples parejas de `llave = valor`. Para configurar la herramienta solo debe modificar el valor dependiendo de sus necesidades. No debe modificar las llaves ni agregar nuevas parejas. A continuación se encuentra una descripción de las 9 secciones:

1. `paths`: contiene las rutas (relativas o absolutas) a las capas geográficas utilizadas durante la validación.
2. `colnames`: contiene los nombres de las columnas presentes en el archivo de entrada durante la validación. **Asegúrese que todas estas columnas están presentes en el archivo de entrada. De lo contrario la validación no funcionará.**
3. `matchnames`: nombres de los campos en las capas geográficas contra los cuales comparar algunas de las columnas en el archivo de entrada. **Asegúrese que todos estos campos están presentes en las capas geográficas. De lo contrario la validación no funcionará.**
4. `flagnames`: nombres de las columnas que se crearán con los respectivos flags.
5. `suggestednames`: nombres de las columnas que se crearán con las respectivas sugerencias donde algunos de los flags sean positivos.
6. `sourcenames`: nombres de las columnas que se crearán con las respectivas fuentes de las sugerencias.
7. `valuenames`: nombres de las columnas que se crearán para extraer nuevos valores de una fuente de datos. Por ahora solo se extraen valores de altura.
8. `misc`: varios valores. Por ahora solo se encuentra la resolución de la cuadrícula que se crea para identificar duplicados espaciales.
9. `texts`: textos de ayuda que se muestran al ejecutar la ayuda de la herramienta (*i.e.* `python src/main.py -h`).

Por defecto la configuración asume que las capas geográficas están ubicadas dentro del proyecto de la siguiente manera:

```
.
├── data
│   └── gpkg
│       ├── admin0.gpkg
│       ├── admin1.gpkg
│       ├── admin2.gpkg
│       ├── urban.gpkg
│       └── geofences.shx
│   └── tif
│       └── dem_col.tif
├── environment.yml
├── LICENSE.txt
├── README.md
├── requirements.txt
└── src
```

Puede descargar las capas y copiarlas dentro del proyecto para que la estructura sea la misma. También puede colocarlas donde quiera y cambiar los valores en la sección 1 de la configuración.

## Ejecución de pruebas unitarias
Para la ejecución de las pruebas unitarias es necesario instalar `pytest`. Para esto active el entorno virtual y ejecute alguno de los siguientes comandos:

Para Anaconda/Miniconda:
```
conda install pytest
```

Para Python:
```
pip install pytest
```

El siguiente comando ejecuta todas las pruebas:
```
pytest tests/
```

## Autores
* Marcelo Villa-Piñeros (mvilla@humboldt.org.co)
