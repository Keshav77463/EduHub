import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def generate_answer(question, retrieved_docs):
    context = []
    for doc in retrieved_docs:
        context.append(doc.page_content)


    prompt = f"""You are a JEE math tutor helping students.
    Use the context below to answer the question.
    If the formula is not in context, _____________  # you fill this!

    Context:
    {context}

    Question: {question}

    Give a complete step by step answer:"""

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3,
    )

    response = llm.invoke(prompt)
    return response.content
