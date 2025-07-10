import streamlit as st
import os
import re

# 🔧 Clean formatting of summary output
def clean_summary_text(text: str) -> str:
    cleaned_lines = []
    for line in text.splitlines():
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)             # Remove markdown bold
        line = re.sub(r"^[\*\+\-]\s*", "- ", line)               # Normalize bullets
        if line.strip():
            cleaned_lines.append(line.strip())
    return "\n".join(cleaned_lines)

DOCUMENTS_DIR = "test_documents"
BASE_SUMMARIES_DIR = "test_results"
DEFAULT_MODEL = "llama3.2-summary"

# 🖼️ Page UI config
st.set_page_config(page_title="📄 Summary Comparator", layout="wide")
st.title("📄 Compare Original Document vs AI Summary")

# 📦 Document dropdown
document_files = [f for f in os.listdir(DOCUMENTS_DIR) if f.endswith((".txt", ".pdf", ".docx"))]
if not document_files:
    st.warning("No documents found in the folder.")
    st.stop()

file_map = {f.replace(".txt", "").replace(".pdf", "").replace(".docx", ""): f for f in document_files}
domains = sorted(file_map.keys())
selected_domain = st.selectbox("📁 Choose a document to compare:", domains)

# 🧠 Selected summarization model (fixed for now)
selected_model = DEFAULT_MODEL
summary_dir = f"{BASE_SUMMARIES_DIR}_{selected_model.replace(':', '_')}"

if selected_domain:
    original_file = os.path.join(DOCUMENTS_DIR, file_map[selected_domain])
    summary_file = os.path.join(summary_dir, selected_domain, f"summary_{file_map[selected_domain]}")

    # 🗂️ Read original
    try:
        with open(original_file, "r", encoding="utf-8") as f:
            original_text = f.read()
    except Exception as e:
        original_text = f"❌ Error reading original file: {e}"

    # 📑 Read summary
    try:
        with open(summary_file, "r", encoding="utf-8") as f:
            raw_summary = f.read()
            summary_text = clean_summary_text(raw_summary)
    except Exception as e:
        summary_text = f"❌ Error reading summary file: {e}"

    # 🎯 Display side by side
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📙 Original Document")
        st.text_area("Full Text", original_text, height=400)

    with col2:
        st.subheader(f"📘 Summary ({selected_model})")
        st.text_area("Summary", summary_text, height=400)

    # 💾 Download option
    if not summary_text.startswith("❌"):
        st.download_button(
            label="⬇️ Download Summary",
            data=summary_text,
            file_name=f"{selected_domain}_{selected_model}_summary.txt"
        )


