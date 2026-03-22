from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_chunk_documents(folder_path):
    loader = PyPDFDirectoryLoader(folder_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")
    seen = set()
    unique_chunks = []
    for chunk in chunks:
        if chunk.page_content not in seen:
            seen.add(chunk.page_content)
            unique_chunks.append(chunk)

    print(f"Unique chunks after deduplication: {len(unique_chunks)}")
    return unique_chunks



