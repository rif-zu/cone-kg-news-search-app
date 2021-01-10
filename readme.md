# Cone-KG News Search Service

This repository contains:

1. A news articles search [Web application](./search_app) made with VUE
2. A [script](knowledge_graph_triplifier.py) that generates a knowledge graph from 3 raw datasets
3. A [script](elastic_search_indexer.py) to index Elastic search documents made in python

## Objectives

To provide a web interface for semantic-based knowledge discovery and acquisition for the public as well as provision of RDF data for researchers and data scientists to acquire knowledge in the domain and furthe rexploit the semantic data for discoveries, automated generation of insights and reasoning from linked data. This furthe provides advanced text analytics features through an elastic search index that complements the SPARQL query capabilities of a triplestore.

## Datasets

Raw datasets

- Aylien
- IEEE
- Covid-19-articles

Knowledge graph-related

- An ontology
- A knowledge graph described using this ontology

## Numbers (reference)

The ieee dataset has around 1,872,570 documents
The aylien dataset has 1,184,382 documents
The covid19 articles dataset has 251,673 documents
