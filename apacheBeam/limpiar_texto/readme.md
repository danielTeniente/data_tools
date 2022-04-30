# Limpiar texto

## Detalles importantes sobre Apache Beam
Ya que la biblioteca sirve para ejecutar pipelines en paralelo, no se tiene el control de cómo será procesado el archivo de entrada. Eso significa que los procesos de lectura o escritura no tienen un orden. Es importante tomarlo en cuenta al trabajar con un archivo csv, mi consejo es que se utilicen archivos con objetos json.

En este caso, en el archivo [dialogos.csv](../../dataset/dialogos.txt) contienen ejemplos de diálogos en un txt. Cada línea maneja el formato json, que facilitará mi trabajo al crear el pipeline.

El dataset original se encuentra en [este repositorio](https://github.com/danielTeniente/dataset_dialogos).

El código completo está en [este archivo](./pipeline_example.py).


