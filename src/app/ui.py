import streamlit as st
import streamlit as st
from whoosh import index
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer
from whoosh.query import Or, Term

# Function to open or create the index (cached)
@st.cache_resource()
def open_index():
    print("Opening existing index...")
    return index.open_dir("src/scripts/index_dir")

# Streamlit UI
def main():
    st.title("Document Search")

    # Search input
    query_str = st.text_input("Enter your query")

    # Open or create the index (cached)
    ix = open_index()

    if query_str:
        # Perform the search
        with ix.searcher() as searcher:
            query_terms = query_str.split()
            query = Or([Term("content", term) for term in query_terms])
            results = searcher.search(query, limit=None)

            if len(results) > 0:
                st.subheader(f"Found {len(results)} documents:")
                for hit in results:
                    st.write(f"Document ID: {hit['doc_id']}")
                    st.write(f"Title: {hit['title']}")
                    st.write(f"Score: {hit.score}")
                    st.write("---")
            else:
                st.write("No matching documents found.")

if __name__ == "__main__":
    main()
