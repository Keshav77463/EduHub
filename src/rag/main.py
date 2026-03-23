from src.rag.data_ingestion import load_and_chunk_documents
from src.rag.embedder import create_vector_store
from src.rag.retriever import retrieve_documents
from src.rag.answer_generator import generate_answer

knowledge_base_path = "D:\\EduHub\\data\\knowledge_base"
chunks = load_and_chunk_documents(knowledge_base_path)

vector_store = create_vector_store(chunks)

question = "What is conditional probability formula?"
results = retrieve_documents(question, vector_store)

print("\n===== Retrieved Chunks =====")
for i, doc in enumerate(results):
    print(f"\nChunk {i + 1} ")
    print(doc.page_content)

print("\n===== Generated Answer =====")
answer = generate_answer(question, results)
print(answer)