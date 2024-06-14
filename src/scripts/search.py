from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.qparser import FuzzyTermPlugin, PrefixPlugin
from whoosh.query import Or, Term
from src import INDEX_DIR


class SearchEngine:
    def __init__(self):
        self.ix = index.open_dir(INDEX_DIR)
        self.parser = QueryParser("content", self.ix.schema)
        self.parser.add_plugin(PrefixPlugin())
        self.parser.add_plugin(FuzzyTermPlugin())

    def search_documents(self, query_str):
        with self.ix.searcher() as searcher:
            query_terms = query_str.split()  # Split the query into individual words

            # Create an Or query with all the query terms
            query = Or([Term("content", term) for term in query_terms])

            results = searcher.search(query, limit=None)  # Set limit to None to retrieve all matching documents

            if len(results) > 0:
                search_results = []
                for hit in results:
                    result = {
                        "doc_id": hit["doc_id"],
                        "title": hit["title"],
                        "score": hit.score
                    }
                    search_results.append(result)
                return search_results
            else:
                return None


if __name__ == "__main__":
    # Test case for SearchEngine
    search_engine = SearchEngine()

    # Test search with a sample query
    query = "communism"
    results = search_engine.search_documents(query)

    if results:
        print(f"Found {len(results)} documents:")
        for result in results:
            print(f"Document ID: {result['doc_id']}")
            print(f"Title: {result['title']}")
            print(f"Score: {result['score']}")
            print("---")
    else:
        print("No matching documents found.")
