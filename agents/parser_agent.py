import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
def parse_problem(raw_problem):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    prompt = f"""You are a math problem parser.
    Parse this problem and return ONLY valid JSON with no extra text, 
    no markdown, no ```json blocks, just pure JSON:

    Problem: {raw_problem}

    Return this exact JSON format:
    {{
        "problem_text": "...",
        "topic": "...",
        "variables": [],
        "constraints": [],
        "needs_clarification": false
    }}"""
    response = llm.invoke(prompt)
    result = json.loads(response.content.strip())
    if result["needs_clarification"] == True:
        print("HITL triggered: problem needs clarification")
    return result


