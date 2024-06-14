from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer
from src import INDEX_DIR, DOCUMENT_DIR
from argparse import ArgumentParser


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--rebuild', action='store_true')
    args = parser.parse_args()

    schema = Schema(
        title=TEXT(stored=True),
        content=TEXT(stored=True),
        doc_id=ID(stored=True, unique=True)
    )

    if not index.exists_in(INDEX_DIR) or args.rebuild:
        print("Creating index...")
        if not INDEX_DIR.exists():
            INDEX_DIR.mkdir()
        ix = index.create_in(INDEX_DIR, schema)
    else:
        print("Opening index...")
        ix = index.open_dir(INDEX_DIR)


    writer = ix.writer()
    for doc_id, doc in enumerate(DOCUMENT_DIR.glob('*.txt')):
        with open(doc, 'r') as f:
            content = f.read()
        writer.add_document(
            title=doc.stem,
            content=content,
            doc_id=str(doc_id)
        )
    writer.commit()
    print("Indexing completed!")
