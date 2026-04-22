import re
import pandas as pd
import os

# === Define paths ===
text_file_path = r"E:\IIIT Banglore\PE Sem 3\RAG File Implementation\Text form of handbook\Farmers_Compost_Handbook.txt"
excel_output_path = r"E:\IIIT Banglore\PE Sem 3\RAG File Implementation\Farmers_Compost_Handbook_Sentences.xlsx"

# === Function to remove illegal characters for Excel ===
def clean_text(text):
    # Remove ASCII control characters (except tab, newline, carriage return)
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', '', text)
    return text

# === Check file existence ===
if not os.path.exists(text_file_path):
    print("❌ Text file not found. Please check the path.")
else:
    # === Read and clean the text ===
    with open(text_file_path, "r", encoding="utf-8") as file:
        raw_text = file.read()
        text = clean_text(raw_text)

    # === Split into sentences ===
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    # === Create Excel ===
    df = pd.DataFrame(sentences, columns=["Sentence"])
    df.to_excel(excel_output_path, index=False)

    print(f"✅ Done! Extracted {len(sentences)} clean sentences to:\n{excel_output_path}")
