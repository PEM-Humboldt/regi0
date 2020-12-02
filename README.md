# recovery
Recovery es un paquete con funciones útiles para la verificación geográfica y taxonómica de registros biológicos.

## Instalación

### Prerrequisitos
* [Python](https://www.python.org/downloads/) (v. 3.8+)


Puede instalar recovery ejecutando el siguiente comando:

```
pip install git+https://github.com/PEM-Humboldt/recovery.git#egg=recovery
```

Si no tiene `git`, ejecute:

```
pip install --upgrade https://github.com/PEM-Humboldt/recovery/tarball/master
```

Para asegurarse que recovery haya quedado instalado, ejecute:

```
python -c "import recovery"
```

Si la instalación fue exitosa, el comando correrá sin ningún problema.

# recovery-cli
Con el fin de facilitar la verificación de registros, recovery tiene una interfaz de consola de comandos (CLI) que permite ejecutar flujos de trabajo completos de verificación desde una terminal. Esta interfaz está documentada en [recovery/cli/README.md](recovery/cli/README.md).

## Cómo contribuir

### Configuración del entorno de desarrollo
Para el desarrollo de recovery se utiliza `poetry`, un auxiliar de empaquetado y gestor de dependencias. Antes de continuar debe [instalarlo](https://python-poetry.org/docs/#installation).

En primer lugar, es necesario clonar este repositorio localmente. Para esto, ejecute:

```
git clone https://github.com/PEM-Humboldt/recovery.git
```

 Luego, ubíquese dentro de del directorio del proyecto:
 
 ```
cd recovery
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
