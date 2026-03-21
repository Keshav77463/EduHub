from embedder import create_vector_store
def retrieve_documents(question,vector_store):
    result=vector_store.similarity_search(
        question,
        k=3
    )
    return result
