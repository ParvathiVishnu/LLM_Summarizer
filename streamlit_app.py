import streamlit as st
import tempfile
import textwrap
import base64
import re

from utils import extract_text_from_file
from ollama_helper import ask_ollama

# Cleaning function for summaries
def clean_summary_text(text: str) -> str:
    cleaned_lines = []
    for line in text.splitlines():
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)            # Remove bold
        line = re.sub(r"^[\*\+\-]\s*", "- ", line)              # Normalize bullets
        if line.strip():
            cleaned_lines.append(line.strip())
    return "\n".join(cleaned_lines)

# Set your summarization model
SUMMARY_MODEL = "llama3.2-summary"

# Streamlit setup
st.set_page_config(page_title="📄 Document Summarizer", layout="wide")
st.title("📄 LLM Document Summarizer")
st.markdown(f"Using **{SUMMARY_MODEL}** for summarization.")

# File uploader
uploaded_file = st.file_uploader("📤 Upload a document (.txt, .docx, .pdf)", type=["txt", "docx", "pdf"])
text = ""

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("🧠 Extracting text from document..."):
        text = extract_text_from_file(tmp_path)

    if text:
        st.subheader("📝 Document Preview")
        st.text_area("Preview (first 3000 characters)", text[:3000], height=300)

# Summarization section
if text:
    st.markdown("### ✂️ Summarization Options")
    bullet_format = st.checkbox("📌 Format summary as bullet points")

    if st.button("🧠 Summarize Document"):
        def chunk_text(text, max_chars=1500):
            return textwrap.wrap(text, width=max_chars, break_long_words=False, replace_whitespace=False)

        with st.spinner("Splitting and summarizing chunks..."):
            chunks = chunk_text(text)
            summaries = []

            for i, chunk in enumerate(chunks):
                st.info(f"📄 Summarizing chunk {i + 1} of {len(chunks)}...")
                prompt = f"Summarize the following content{' in bullet points' if bullet_format else ''}:\n\n{chunk}"
                summary = ask_ollama(prompt, model=SUMMARY_MODEL)
                summaries.append(clean_summary_text(summary.strip()))

            final_summary = "\n\n".join(summaries)

            st.subheader("✅ Final Summary")
            st.success(final_summary)

            with st.expander("📑 View Individual Chunk Summaries"):
                for i, s in enumerate(summaries):
                    st.markdown(f"**Chunk {i + 1}:**\n{s}\n")

            # Download option
            summary_filename = uploaded_file.name.replace(".", "_") + "_summary.txt"
            b64 = base64.b64encode(final_summary.encode()).decode()
            href = f'<a href="data:file/txt;base64,{b64}" download="{summary_filename}">📥 Download Summary</a>'
            st.markdown(href, unsafe_allow_html=True)
