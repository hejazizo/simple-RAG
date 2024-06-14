from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.query import Or, Term
from whoosh.fields import Schema, TEXT, ID
from src import INDEX_DIR, DOCUMENT_DIR
from whoosh.qparser import PrefixPlugin, FuzzyTermPlugin


class SearchEngine:
    def __init__(self, index_dir, rebuild=False):
        self.schema = Schema(
            doc_name=TEXT(stored=True),
            content=TEXT(),
            doc_id=ID(stored=True, unique=True)
        )
        if rebuild:
            self.rebuild_index()

        self.ix = index.open_dir(index_dir)
        self.parser = QueryParser("content", self.ix.schema)
        self.parser.add_plugin(PrefixPlugin())
        self.parser.add_plugin(FuzzyTermPlugin())

    def rebuild_index(self):
        print("Creating index...")
        if not INDEX_DIR.exists():
            INDEX_DIR.mkdir()
        ix = index.create_in(INDEX_DIR, self.schema)

        writer = ix.writer()
        for doc_id, doc in enumerate(DOCUMENT_DIR.glob('*.txt')):
            with open(doc, 'r') as f:
                content = f.read()
            writer.add_document(
                doc_name=doc.name,
                content=content,
                doc_id=str(doc_id)
            )
        writer.commit()
        print("Indexing completed!")

    def __call__(self, query_str):
        with self.ix.searcher() as searcher:
            query_terms = query_str.split()  # Split the query into individual words

            # Create an Or query with all the query terms
            query = Or([Term("content", term) for term in query_terms])

            results = searcher.search(query, limit=None)  # Set limit to None to retrieve all matching documents

            if len(results) > 0:
                search_results = []
                for hit in results:
                    doc_name = hit['doc_name']
                    doc_file_path = DOCUMENT_DIR / doc_name
                    content = doc_file_path.read_text()
                    result = {
                        "doc_id": hit["doc_id"],
                        "doc_name": hit["doc_name"],
                        "score": hit.score,
                        "content": content,
                        "highlights": hit.highlights("content", text=content)
                    }
                    search_results.append(result)
                return search_results
            else:
                return
