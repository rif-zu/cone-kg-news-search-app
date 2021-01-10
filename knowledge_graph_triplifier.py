import os
import pandas as pd
import json
import numpy as np
from triplifier.rdf.event import Event

from rdflib import Graph
from config import NS, INPUT_DATA_DIR, OUTPUT_DATA_DIR
from triplifier.rdf.ontology import FNO

MAX_DOCS_PER_FILE = 60000
def process_directory(input_directory, output_directory):
    print(f'input_directory: {input_directory}')
    print(f'output_directory: {output_directory}')
    for r, d, f in os.walk(input_directory):
        for file in f:
            file_path = os.path.join(r, file)
            dataset_name = file.rstrip('.sample')
            print(f'Reading: {file_path}')

            # Process covid19 files
            if file.startswith('covid19'):
                dataset_name = dataset_name.rstrip('.csv')

                processed_documents = 0
                file_index = 0
                graph = Graph()

                df = pd.read_csv(file_path)
                for index, row in df.iterrows():
                    source_dataset_id = row[0]
                    _URI = f'{NS}/{dataset_name}/{source_dataset_id}'
                    event = Event(f'{dataset_name}/{source_dataset_id}', row['content'], graph=graph)
                    event.add_date(row['date'])
                    event.add_organization(row['domain'])
                    event.add_url(row['url'])
                    event.add_date(row['date'])
                    event.add_title(row['title'])
                    if ('author' in row and not row['author'] is np.nan):
                        event.add_publisher(row['author'])
                    graph = event.graph

                    processed_documents = processed_documents + 1
                    if processed_documents % MAX_DOCS_PER_FILE == 0:
                        write_turtle_file(graph, output_directory, f'{dataset_name}_{file_index}')
                        file_index = file_index + 1
                        graph = Graph()
                write_turtle_file(graph, output_directory, f'{dataset_name}_{file_index}')

            # Process aylien files
            elif file.startswith('aylien'):
                dataset_name = dataset_name.rstrip('.jsonl')

                processed_documents = 0
                file_index = 0
                graph = Graph()

                with open(file_path) as fp:
                    for index, line in enumerate(fp):
                        row = json.loads(line)
                        source_dataset_id = row['id']
                        event = Event(f'{dataset_name}/{source_dataset_id}', row['body'], graph=graph)
                        event.add_organization(row['source']['name'], row['source']['id'])
                        event.add_url(row['links']['permalink'])
                        event.add_date(row['published_at'])
                        event.add_title(row['title'])
                        event.add_publisher(row['author']['name'], row['author']['id'])

                        if row['media']:
                            for media in row['media']:
                                event.add_image(media['url'])

                        graph = event.graph

                        processed_documents = processed_documents + 1
                        if processed_documents % MAX_DOCS_PER_FILE == 0:
                            write_turtle_file(graph, output_directory, f'{dataset_name}_{file_index}')
                            file_index = file_index + 1
                            graph = Graph()
                    write_turtle_file(graph, output_directory, f'{dataset_name}_{file_index}')

            # Process ieee files
            elif file.startswith('16119'):
                dataset_name = dataset_name.rstrip('.json')

                processed_documents = 0
                file_index = 0
                graph = Graph()

                with open(file_path) as fp:
                    for index, line in enumerate(fp):
                        row = json.loads(line)
                        source_dataset_id = row['uuid']
                        _URI = f'{NS}/{dataset_name}/{source_dataset_id}'
                        event = Event(f'{dataset_name}/{source_dataset_id}', row['text'], graph=graph)
                        event.add_date(row['published'])
                        event.add_organization(row['thread']['section_title'])
                        event.add_url(row['url'])
                        event.add_date(row['published'])
                        event.add_title(row['title'])
                        event.add_publisher(row['author'])
                        graph = event.graph

                        processed_documents = processed_documents + 1
                        if processed_documents % MAX_DOCS_PER_FILE == 0:
                            write_turtle_file(graph, output_directory, f'{dataset_name}_{file_index}')
                            file_index = file_index + 1
                            graph = Graph()
                    write_turtle_file(graph, output_directory, f'{dataset_name}_{file_index}')
            else:
                raise NotImplemented

    print(f'Ended')

def write_turtle_file(graph, output_directory, filename):
    graph.bind("fno", FNO)
    destination_file = f'{output_directory}/{filename}.n3'
    print(f'Writing : {destination_file}')
    graph.serialize(destination=destination_file, format='n3')

# Reads all files from a directory and generates triples from them
if __name__ == '__main__':
    process_directory(INPUT_DATA_DIR, OUTPUT_DATA_DIR)
