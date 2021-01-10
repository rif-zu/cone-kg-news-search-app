import os
from config import ES_ENDPOINT, ES_USERNAME, ES_PASSWORD, INPUT_DATA_DIR
from triplifier.json_ld_generators import select_json_document_generator
from triplifier.take_samples import SAMPLE_SIZE
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk
import tqdm

es = Elasticsearch(
    hosts=[ES_ENDPOINT],
    http_auth=(ES_USERNAME, ES_PASSWORD),
    timeout=60
)

PATH = INPUT_DATA_DIR

def index_directory_in_elastic_search(path):
    for r, d, f in os.walk(path):
        for file in f:
            file_path = os.path.join(r, file)
            index_file_in_elastic_search(file_path, file)

def index_file_in_elastic_search(file_path, file, sample_size=SAMPLE_SIZE):

    dataset_name, generator = select_json_document_generator(file_path, file)

    # The name of the elastic search index will be the name of source file
    print(f'deleting index: {dataset_name}')
    es.indices.delete(index=dataset_name, ignore=[400, 404])

    print(f'indexing file: {file} into ES index: {dataset_name}')
    progress = tqdm.tqdm(unit="docs", total=sample_size)
    successes = 0
    for ok, action in streaming_bulk(
            client=es,
            index=dataset_name,
            actions=generator,
            max_retries=3,
            raise_on_error=False,

    ):
        progress.update(1)
        successes += ok
    es.indices.refresh(index=dataset_name)
    print("Indexed %d/%d documents" % (successes, sample_size))


if __name__ == '__main__':
    index_directory_in_elastic_search(PATH)
