import os
import re
from utils import extract_text_from_file
from ollama_helper import ask_ollama

INPUT_DIR = "test_documents"
BASE_OUTPUT_DIR = "test_results"
MODEL_NAME = "llama3.2-summary"

# Safe model name for folder structure
model_safe_name = MODEL_NAME.replace(":", "_")
OUTPUT_DIR = f"{BASE_OUTPUT_DIR}_{model_safe_name}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Summary cleaning function
def clean_summary_text(text: str) -> str:
    cleaned_lines = []
    for line in text.splitlines():
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)           # Remove markdown bold
        line = re.sub(r"^[\*\+\-]\s*", "- ", line)             # Normalize bullets
        if line.strip():
            cleaned_lines.append(line.strip())
    return "\n".join(cleaned_lines)

# Loop over documents
for file_name in os.listdir(INPUT_DIR):
    if not file_name.endswith((".txt", ".pdf", ".docx")):
        continue

    input_path = os.path.join(INPUT_DIR, file_name)
    domain = os.path.splitext(file_name)[0]
    domain_output_dir = os.path.join(OUTPUT_DIR, domain)
    os.makedirs(domain_output_dir, exist_ok=True)

    print(f"📄 Summarizing with {MODEL_NAME}: {input_path}")
    raw_text = extract_text_from_file(input_path)

    if raw_text:
        try:
            prompt = (
                "Summarize the following document content in clear, concise bullet points. "
                "Focus only on the key points while preserving semantic meaning:\n\n"
                + raw_text
            )

            summary = ask_ollama(prompt, model=MODEL_NAME)
            cleaned_summary = clean_summary_text(summary)

            output_path = os.path.join(domain_output_dir, f"summary_{file_name}")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned_summary)

            print(f"✅ Saved summary to {output_path}")

        except Exception as e:
            print(f"❌ Error while summarizing {file_name}: {e}")
    else:
        print(f"⚠️ Skipping file with no extractable text: {input_path}")

