# recovery-cli

Recovery-CLI es una interfaz de consola de comandos para ejecutar flujos de trabajo pre-establecidos de verificación sin necesidad de crear nuevas rutinas o scripts.

La interfaz está expuesta mediante el programa `recovery`, accesible desde cualquier ubicación en su computador después de haber [instalado el paquete](../../README.md#instalación).

```
$ recovery --help
Usage: recovery [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  download  Download necessary data to run the
            recovery geo command line utility.

  geo       Performs a complete geographic
            verification on a set of records.

  setup     Setups the configuration files required
            to run the other CLI commands.
```

## Comandos
Actualmente hay un comando principal (`geo`) y dos comandos auxiliares (`download` y `setup`). Tenga en cuenta que es necesario ejecutar **una sola vez** los comandos auxiliares (primero `setup` y luego `download`) pues se necesita establecer los archivos de configuración y descargar los datos de entrada para ejecutar la verificación geográfica.

### setup
```
$ recovery setup --help
Usage: recovery setup [OPTIONS]

Options:
  --help  Show this message and exit.
```
Este comando no recibe ningún argumento ni opción y es el encargado de copiar las plantillas de los archivos de configuración ([logger.ini](../../config/logger.ini) y [settings.ini](../../config/settings.ini)) en la carpeta de configuración por defecto del sistema. Las rutas de estas carpetas son:

* MacOS:
* Linux: `~/.config/recovery`
* Windows:

Ejemplo:
```
recovery setup
```

### download
```
$ recovery download --help
Usage: recovery download [OPTIONS] [DST] [URL]

Options:
  --quiet  Silence information logging.  [default:
           False]

  --help   Show this message and exit.
```
Este comando se encarga de descargar los datos necesarios para ejecutar la rutina de verificación geográfica. Adicionalmente, modifica la copia de la plantilla de configuración [settings.ini](../../config/settings.ini) con las nuevas rutas locales de los archivos descargados. Acepta dos argumentos:

* `DST`: ruta (absoluta o relativa de la carpeta dónde se van a descargar y extraer los datos).
* `URL`: url del archivo comprimido almacenado en Google Drive con los datos necesarios.

Por defecto (si no se pasa ningún argumento), la rutina descargará el archivo especificado en [settings.ini](../../config/settings.ini) y extraerá los datos en el directorio actual de trabajo desde donde se ejecute el comando.

Ejemplos:
```
recovery download
recovery download /home/foo/bar https://drive.google.com/uc?id=15TsDoq7u4hRotucE2LJyO-N5XCIteuCi
```

### geo
```
$ recovery geo --help
Usage: recovery geo [OPTIONS] SRC DST

Options:
  --lon_col TEXT       Longitude column.  [default:
                       lon]

  --lat_col TEXT       Latitude column.  [default:
                       lat]

  --crs TEXT           Coordinate Reference System
                       in the form epsg:code.
                       [default: epsg:4326]

  --admin0_col TEXT    Level 0 administrative
                       division column (i.e.
                       country).  [default: country]

  --admin1_col TEXT    Level 1 administrative
                       division column (e.g.
                       department or state).
                       [default: adm1]

  --admin2_col TEXT    Level 2 administrative
                       division column (e.g.
                       municipality or county).
                       [default: adm2]

  --date_col TEXT      Collection date column.
                       [default:
                       earliestDateCollected]

  --species-col TEXT   Species name column.
                       [default: species]

  --default-year TEXT  Default year to take for
                       records that do not have a
                       collection date or whose
                       collection data did not match
                       with any year. Can be 'last'
                       for the most recent year in
                       the historical data or
                       'first' for the oldest year
                       in the historical data. Do
                       not pass this parameter to
                       ignore the verification on
                       records without a date.

  --gridres FLOAT      Resolution of the grid to
                       identify spatial duplicated.
                       Units must be the same as
                       crs.  [default:
                       0.00833333376796715]

  --ignore TEXT        What records that are spatial
                       duplicates to ignore. Can be
                       'first' or 'last'. Do not
                       pass this parameter to not
                       ignore any record.  [default:
                       False]

  --drop               Drop records with a positive
                       flag.  [default: False]

  --quiet              Silence information logging.
                       [default: False]

  --help               Show this message and exit.
```
Este comando ejecuta un flujo de trabajo completo de verificación geográfica. Acepta dos argumentos:

* `SRC`: tabla de entrada con los registros biológicos. Puede ser un archivo .csv o .xlsx.
* `DST`: tabla de salida con una copia o subconjunto de los registros originales y múltiples columnas extras con flags, sugerencias y fuentes de verificación. El comando acepta adicionalmente diferentes opciones que permiten especificar nombres de columnas en la tabla de entrada y comportamiento del comando. Todas las opciones tienen valores por defecto que pueden ser modificados al ejecutar el comando o en el archivo de configuración.

El flujo de trabajo consiste en los siguientes pasos:

1. Eliminar registros sin coordenadas.
2. Verificar límites administrativos (*i.e.* país, departamento y municipio).
3. Identificar registros ubicados dentro de centros poblados o zonas urbanas.
4. Extraer valores de altura e identificar anómalos a nivel de especie.
5. Identificar registros de una misma especie duplicados espacialmente.

## Configuración
El archivo de configuración settings.ini, copiado de la plantilla en su máquina local (ver [`setup`](#setup)), permite configurar diferentes parámetros del comando `geo`. Este archivo de configuración está dividido en cinco secciones:

### `paths`
Contiene las rutas locales absolutas de los archivos utilizados durante la verificación. Recuerde que al ejecutar el comando `download`, esas rutas se actualizan automáticamente.

### `colnames`
Nombres de las columnas de la tabla de registros de entrada que se toman por defecto si no se especifican en las opciones del comando `geo`.

### `matchnames`
Nombres de los campos en las capas geográficas de comparación (*i.e.* límites administrativos) para comparar con la tabla de registros de entrada.

### `flagnames`
Nombres de los flags resultantes de la verificación.

### `sourcenames`
Nombres de las columnas resultantes que contienen las fuentes utilizadas para la verificación.

### `valuenames`
Nombre de las columnas que se crearán con los valores extraidos.

### `misc`
Otros parámetros de configuración. En este momento se encuentran la resolución de la cuadrícula que se utiliza para identificar duplicados espaciales y la URL de Google Drive con el archivo comprimido con los datos necesarios para ejecutar el comando `geo`.
