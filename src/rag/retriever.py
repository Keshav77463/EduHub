def retrieve_documents(question,vector_store):
    result=vector_store.similarity_search(
        question,
        k=5
    )
    return result
