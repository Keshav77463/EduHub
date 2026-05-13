import os,sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from agents.parser_agent import parse_problem
from agents.intent_router_agent import route_intent
from agents.solver_agent import solve_problem
from agents.verifier import verifier
from src.db.memory import Mongomemory
from src.multimodal.whisper_transcriber import transcribe_audio
from src.multimodal.ocr_transcriber import extract_text_from_image

def run_pipeline(raw_input,input_type,user_id,vector_store):
    if input_type == "image":
        question = extract_text_from_image(raw_input)
    elif input_type == "audio":
        question = transcribe_audio(raw_input)
    else:
        question = raw_input
    parsed = parse_problem(question)
    routed = route_intent(question)
    solved = solve_problem(parsed["problem_text"],routed["topic"],vector_store)
    verified = verifier(parsed["problem_text"], solved["answer"], routed["topic"])
    memory = Mongomemory()
    memory.save_conversation(user_id, question, input_type, parsed, routed, solved, verified)
    return {"parsed": parsed, "routed": routed, "solved": solved, "verified": verified}
if __name__ == "__main__":
    from src.rag.embedder import create_vector_store
    from src.rag.data_ingestion import load_and_chunk_documents

    chunks = load_and_chunk_documents("D:\\EduHub\\data\\knowledge_base")
    vs = create_vector_store(chunks)

    result = run_pipeline(
        raw_input="What is the formula for conditional probability?",
        input_type="text",
        user_id="test_user",
        vector_store=vs
    )
    print(result)

