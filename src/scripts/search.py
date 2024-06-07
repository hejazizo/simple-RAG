from pathlib import Path

from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import FuzzyTermPlugin, PrefixPlugin

from src import INDEX_DIR

ix = index.open_dir(INDEX_DIR)

parser = QueryParser("content", ix.schema)
parser.add_plugin(PrefixPlugin())
parser.add_plugin(FuzzyTermPlugin())

# Perform a search
from whoosh.query import Or, Term

with ix.searcher() as searcher:
    query_str = "political"
    query_terms = query_str.split()  # Split the query into individual words

    # Create an Or query with all the query terms
    query = Or([Term("content", term) for term in query_terms])

    results = searcher.search(query, limit=None)  # Set limit to None to retrieve all matching documents

    if len(results) > 0:
        print(f"Found {len(results)} documents:")
        for hit in results:
            print(f"Document ID: {hit['doc_id']}")
            print(f"Title: {hit['title']}")
            print(f"Score: {hit.score}")
            print("---")
    else:
        print("No matching documents found.")
