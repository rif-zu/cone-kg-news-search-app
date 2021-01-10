# Cone-KG News Search Service

This repository contains:

1. A news articles search [Web application](./search_app) made with VUE
2. A [script](knowledge_graph_triplifier.py) that generates a knowledge graph from 3 raw datasets
3. A [script](elastic_search_indexer.py) to index Elastic search documents made in python

## Objectives

To provide search and advanced text analytics features.

this is done through an elastic search index that complements the SPARQL query capabilities of a triplestore.

## Datasets

Raw datasets

- Aylien
- Ieee
- Covid-19-articles

Knowledge graph-related

- An ontology
- A knowledge graph described using this ontology

## Numbers (reference)

The ieee dataset has around 1872570 documents
The aylien dataset has 1184382 documents
The covid19 articles dataset has 251673 documents
