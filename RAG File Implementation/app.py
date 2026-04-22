import os
import chromadb
import google.generativeai as genai
import PyPDF2
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings

# Load API key safely
load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found. Add it to your .env file.")
    exit()

try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    exit()

# Initialize persistent Chroma client
chroma_client = chromadb.PersistentClient(path="chroma_persistent_storage")
collection = chroma_client.get_or_create_collection(name="document_qa_collection")

# Use a compact and efficient sentence embedding model
embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# === Load PDF files ===
def load_documents_from_directory(directory_path):
    documents = []
    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return documents
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(directory_path, filename)
            try:
                with open(filepath, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        content = page.extract_text()
                        if content:
                            text += content + "\n"
                    if text:
                        documents.append({"id": filename, "text": text})
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return documents

# === Split long text into smaller overlapping chunks ===
def split_text(text, chunk_size=2500, chunk_overlap=200):
    chunks, start = [], 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap
    return chunks

# Load and prepare PDFs
directory_path = "./my_articles"
documents = load_documents_from_directory(directory_path)
if not documents:
    print("No documents found.")
    exit()

print(f"Loaded {len(documents)} PDF(s)")
chunked_documents = []
for doc in documents:
    chunks = split_text(doc["text"])
    print(f"Splitting {doc['id']} → {len(chunks)} chunks")
    for i, chunk in enumerate(chunks):
        chunked_documents.append({"id": f"{doc['id']}_chunk{i+1}", "text": chunk})

# === Generate embeddings and insert into Chroma ===
if chunked_documents:
    print("Generating embeddings and storing in Chroma...")
    for doc in chunked_documents:
        try:
            # 🔹 CHANGED: Use embed_documents() instead of embed_query()
            embedding = embedder.embed_documents([doc["text"]])[0]
            collection.upsert(
                ids=[doc["id"]],
                embeddings=[embedding],
                documents=[doc["text"]]
            )
        except Exception as e:
            print(f"Error inserting {doc['id']}: {e}")
    print("Insertion complete.")
else:
    print("No chunks to insert.")
    exit()

# === Query Chroma for relevant chunks ===
def query_documents(question, n_results=3):
    try:
        query_embedding = embedder.embed_query(question)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        # 🔹 CHANGED: Return both documents and similarity scores for debugging
        return results.get("documents", [[]])[0]
    except Exception as e:
        print(f"Error querying ChromaDB: {e}")
        return []

# === Generate a Gemini response based on retrieved context ===
def generate_response(question, relevant_chunks):
    if not relevant_chunks:
        return "I couldn't find any relevant information in the documents."

    context = "\n\n".join(relevant_chunks)
    prompt = f"""
You are a helpful assistant for answering questions based on context.
Use only the provided context to answer accurately.
If the answer is not found in the context, say "I don't know."

Context:
{context}

Question:
{question}
"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating Gemini response: {e}")
        return "There was an error generating the response."

# === Interactive console Q&A ===
print("\n--- Document RAG System Ready ---")
while True:
    user_question = input("\nAsk a question (or type 'exit' to quit):\n> ")
    if user_question.lower() == "exit":
        break
    relevant_chunks = query_documents(user_question)
    answer = generate_response(user_question, relevant_chunks)
    print("\nAnswer:\n", answer)

print("Exiting...")
