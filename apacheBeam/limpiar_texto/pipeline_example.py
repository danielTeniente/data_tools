import argparse
import requests
import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

# función principal
def main():
    parser = argparse.ArgumentParser(description="Clean a TXT text")
    parser.add_argument("--input_file", help="Input file")
    parser.add_argument("--output_file", help="Output file")
    # se obtienen los parámetros para el pipeline
    args, beam_args = parser.parse_known_args()
    run_pipeline(args, beam_args)

# función para limpiar un los diálogos del dataset
def clean_text(dataset_object):
    return dataset_object

# ejecuta el pipeline
def run_pipeline(custom_args, beam_args):
    input_file = custom_args.input_file
    output_file = custom_args.output_file

    opts = PipelineOptions(beam_args)

    #pipeline
    with beam.Pipeline(options=opts) as p:
        # la entrada no tiene orden
        lines = p | 'Input' >> beam.io.ReadFromText(input_file)
        # PCollection
        dictionaries = lines | 'Get dictionaries' >> beam.Map(lambda line: json.loads(str(line).encode('utf-8')))
        # limpia los diálogos
        new_text = dictionaries | 'Clean text' >> beam.Map(lambda dictionary: clean_text(dictionary))
        # escribe los resultados
        new_text | beam.io.WriteToText(output_file)

if __name__=='__main__':
    main()