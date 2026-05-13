import os
import sys
import streamlit as st
sys.path.append(os.path.dirname(__file__))

from src.pipeline import run_pipeline
from src.rag.embedder import get_or_create_vector_store
from src.db.memory import Mongomemory

st.set_page_config(
    page_title="Eduhub AI Tutor",
    page_icon="🎓",
    layout="wide"
)
@st.cache_resource
def load_vector_store():
    return get_or_create_vector_store("D:\\EduHub\\data\\knowledge_base")
vector_store = load_vector_store()
with st.sidebar:
    st.header("⚙️ Settings")
    user_id = st.text_input("User ID", value="student_001")
    input_type = st.radio("Input Type", ["text", "image", "audio"])
    st.markdown("---")
    st.header("📚 History")
    if st.button("Refresh History"):
        memory = Mongomemory()
        history = memory.get_history(user_id, limit=5)
        for chat in history:
            st.write(f"**Q:** {chat['question'][:50]}...")
            st.caption(f"Topic: {chat['router_result']['topic']} | {chat['timestamp'].strftime('%Y-%m-%d %H:%M')}")
st.title("🎓 EduHub AI Math Tutor")
st.markdown("Ask any JEE math question and get a step-by-step verified solution!")
raw_input = None
if input_type == "text":
    raw_input = st.text_area("Enter your math problem here:", height=150)
elif input_type == "image":
    raw_input = st.file_uploader("Upload an image of your problem", type=["png", "jpg", "jpeg"])
elif input_type == "audio":
    raw_input = st.file_uploader("Upload an audio recording", type=["wav", "mp3", "m4a"])
# --- 5. Run Pipeline & Display Results ---
if st.button("🚀 Solve Problem", type="primary"):
    if not raw_input:
        st.warning("Please provide a question first!")
    else:
        try:
            import tempfile
            import os

            # --- NEW: Handle File Uploads by saving them temporarily ---
            if input_type in ["image", "audio"]:
                # Get the file extension (like .png or .mp3)
                file_extension = os.path.splitext(raw_input.name)[1]

                # Create a temporary file on the hard drive
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                    temp_file.write(raw_input.read())  # Save the uploaded bytes
                    temp_file_path = temp_file.name  # Get the string file path

                # We pass the real file path to the pipeline
                pipeline_input = temp_file_path
            else:
                # If it's just text, pass it normally
                pipeline_input = raw_input

            # Call our main pipeline!
            result = run_pipeline(
                raw_input=pipeline_input,  # <--- Use the new pipeline_input here!
                input_type=input_type,
                user_id=user_id,
                vector_store=vector_store
            )

            # --- NEW: Clean up the temporary file so we don't waste data ---
            if input_type in ["image", "audio"]:
                os.remove(temp_file_path)

            # --- HITL Triggers ---
            parsed_clarity = result['parsed'].get('needs_clarification')
            routed_clarity = result['routed'].get('needs_clarification')
            topic = str(result['routed'].get('topic', '')).lower()
            
            if parsed_clarity in [True, "true", "True"] or routed_clarity in [True, "true", "True"] or topic == 'unknown':
                st.error(
                    "🛑 HITL Triggered: The problem is unclear or the topic is unknown. Please rephrase your question.")

            if result['solved'].get('confidence', 1.0) < 0.7:
                st.warning(
                    "⚠️ HITL Triggered: The AI is not very confident about this answer. A human tutor should review it.")

            if result['verified'].get('verdict') == 'incorrect':
                st.error("🛑 HITL Triggered: The Verifier AI believes the Solver made a mistake! Needs human review.")

            # Create tabs to display everything neatly
            tab1, tab2, tab3 = st.tabs(["📝 Solution", "🔍 Analysis", "✅ Verification"])

            with tab1:
                st.success("Problem Solved!")
                st.write(f"**Confidence:** {result['solved'].get('confidence', 0) * 100}%")
                st.subheader("Answer")
                st.write(result['solved'].get('answer', "No answer found."))
                st.subheader("Steps")
                for step in result['solved'].get('steps', []):
                    st.write(f"- {step}")

            with tab2:
                st.info(f"**Topic Detected:** {result['routed'].get('topic', 'Unknown').capitalize()}")
                st.write(f"**Difficulty:** {result['routed'].get('difficulty', 'Unknown').capitalize()}")
                st.write("**Parsed Constraints:**")
                st.json(result['parsed'].get('constraints', []))

            with tab3:
                verdict = result['verified'].get('verdict', 'unknown')
                if verdict == "correct":
                    st.success("✅ Verifier confirmed this answer is correct.")
                elif verdict == "incorrect":
                    st.error("❌ Verifier flagged this answer as incorrect!")
                else:
                    st.warning(f"⚠️ Verifier status: {verdict}")

                st.write("**Verifier Explanation:**")
                st.write(result['verified'].get('explanation', "No explanation provided."))

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

