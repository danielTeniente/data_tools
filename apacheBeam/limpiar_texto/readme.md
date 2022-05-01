# Limpiar texto

## Detalles importantes sobre Apache Beam
Ya que la biblioteca sirve para ejecutar pipelines en paralelo, no se tiene el control de cómo será procesado el archivo de entrada. Eso significa que los procesos de lectura o escritura no tienen un orden. Es importante tomarlo en cuenta al trabajar con un archivo csv, mi consejo es que se utilicen archivos con objetos json.

En este caso, en el archivo [dialogos.csv](../../dataset/dialogos.txt) contienen ejemplos de diálogos en un txt. Cada línea maneja el formato json, que facilitará mi trabajo al crear el pipeline.

El dataset original se encuentra en [este repositorio](https://github.com/danielTeniente/dataset_dialogos).

El código completo está en [este archivo](./pipeline_example.py).

## Explicación

La función `main()` es el inicio del programa. Se argumentos mediante la línea de comandos y se inicializan las variables de ApacheBeam.

Al final, se llama a la función `run_pipeline(args, beam_args)`

```python
def main():
    parser = argparse.ArgumentParser(description="Clean a TXT text")
    parser.add_argument("--input_file", help="Input file")
    parser.add_argument("--output_file", help="Output file")
    # se obtienen los parámetros para el pipeline
    args, beam_args = parser.parse_known_args()
    run_pipeline(args, beam_args)
```

La función principal es la que ejecuta el pipeline. Lo primero que se hace es obtener los parámetros enviados por el usuario. En este caso necesitamos el nombre del dataset y el nombre del archivo de salida donde se escribirá el resultado.

```python
def run_pipeline(custom_args, beam_args):
    input_file = custom_args.input_file
    output_file = custom_args.output_file

    opts = PipelineOptions(beam_args)
```

Luego, se inicia el pipeline mediante la palabra clave `with`. Existen otras formas de ejecutar el pipeline, pero me parece que utilizar `with` es una buena práctica.

Lo siguiente es establecer el pipeline mediante el uso de `|`. La primera línea simplemente lee el archivo. Se empieza con la variable `p` y el resultado se almacena en `lilnes`.

```python
    #pipeline
    with beam.Pipeline(options=opts) as p:
        # la entrada no tiene orden
        lines = p | 'Input' >> beam.io.ReadFromText(input_file)
```
La función `ReadFromText` de apache Beam lee el archivo línea por línea y retorna una PCollection. Esta estructura de datos no tiene orden, debido a que permite el procesamiento en paralelo. Entonces, el orden de las líneas puede mantenerse o no. Esto es importante, un PCollection no tiene orden, así que no podemos hacer algo como `lines[0]`.

El siguiente paso es convertir los strings en diccionarios para acceder a la información de forma sencilla. Se puede observar que `lines` es la entrada del siguiente pipe `|`. La salida se llama `dictionaries`. La función `Map` recibe los datos de la PCollection y los procesa uno por uno. Esos datos son recibidos por una función, en este caso, utilizo una función anónima `lamba`. Por cada `line` quiero obtener un diccionario, por eso utilizo `json.loads`.

```python
        # PCollection
        dictionaries = lines | 'Get dictionaries' >> beam.Map(lambda line: json.loads(str(line).encode('utf-8')))
```
Repito el mismo proceso para limpiar el texto de cada diccionario. La función `clean_text` no requiere de mayor explicación, simplemente quita signos especiales.

```python
        # limpia los diálogos
        new_text = dictionaries | 'Clean text' >> beam.Map(lambda dictionary: clean_text(dictionary))
```
Al final, utiliza otra función de ApacheBeam para guardar la salida en un archivo de texto.

```python
        # escribe los resultados
        new_text | beam.io.WriteToText(output_file)
```

### Ejecución

La forma de ejecutar este pipeline es la siguiente:
`python ./pipeline_example.py --input_file ..\..\dataset\dialogos.txt --output_file clean_text.txt`

De todas formas, lo mejor es crear un archivo .bat como [run.bat](./run.bat) para no tener que ingresar el mismo comando una y otra vez. Esto es útil a medida que vas probando el código.
