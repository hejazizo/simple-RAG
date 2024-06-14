import streamlit as st
from src.app.search import SearchEngine
from src import INDEX_DIR
from src.app.llm import call_llm


def main():
    st.title("Document Search")

    # Search input
    query_str = st.text_input("Enter your query")

    # Open or create the index (cached)
    search_engine = SearchEngine(INDEX_DIR)
    if st.sidebar.button("Rebuild Index"):
        search_engine.rebuild_index()
        st.sidebar.success("Index rebuilt successfully!", icon="✅")

    if not query_str:
        return

    search_results = search_engine(query_str)
    if not search_results:
        st.write("No results found")
        return

    # Display search results
    MAX_DOCS = 3
    st.sidebar.title(":mag: Search Results")
    for hit in search_results[:MAX_DOCS]:
        st.sidebar.write(f"**{hit['doc_name']}** (`{hit['score']:.2}`)")
        st.sidebar.html(hit['highlights'])
        with st.sidebar.expander("Full Content"):
            st.sidebar.write(f"Content: {hit['content']}")

        if search_results.index(hit) < len(search_results) - 1:
            st.sidebar.write("---")

    # Language model
    relevant_documents = [hit['content'] for hit in search_results][:MAX_DOCS]
    relevant_content = "\n".join(relevant_documents)
    user_question = query_str
    prompt_text = f"""Given the follwing documents, answer the question:
User Question: {user_question}
Relevant documents:{relevant_content}

Generate answer like you are a customer support agent for this company:
Company name: Pytopia
Company industry: Online Courses
Company location: Iran
Company website: www.pytopia.ai

Don't provide any answer if it doesn't exist in the relevant documents.
Just say "I don't know" if you can't find the answer.
"""
    model_name = "gpt-4-turbo"
    with st.spinner("Thinking..."):
        response = call_llm(model_name, prompt_text)
    st.write(response)

if __name__ == "__main__":
    main()
