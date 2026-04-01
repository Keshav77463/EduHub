import os
import re
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def extract_json(text):
    """Extract JSON from LLM response that may contain markdown fences or extra text."""
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            return json.loads(match.group())
        raise
def route_intent(problem_text):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    prompt=f"""you will be given {problem_text} of which you have to 
seperate topic of which it belongs and you have to tell the difficulty of the {problem_text}
and also tell the solver type like is it formula based pr conceptual and also tell 
if you need any clearification and return the answer in json format 
 Return this exact JSON format:
 IMPORTANT: Return ONLY the JSON object. No other text.
    {{
        "topic": "probability/algebra/calculus/linear_algebra/unknown",
        "difficulty": "easy/medium/hard",
        "solver_type": "formula_based/step_by_step/conceptual",
        "needs_clarification": false
    }}"""
    response = llm.invoke(prompt)
    result = extract_json(response.content)
    if result["topic"] == "unknown":
        print("HITL triggered: problem needs clarification")
    return result
if __name__ == "__main__":
    result = route_intent("find the probability of getting heads")
    print(result)

