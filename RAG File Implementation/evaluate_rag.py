import pandas as pd
import time
from app import query_documents, generate_response

# === 30 User Queries ===
user_queries = [
    "What are the main stages of composting?",
    "How often should compost be turned?",
    "What temperature indicates compost is active?",
    "How does moisture affect compost quality?",
    "Which microorganisms are key in composting?",
    "How can we reduce odor in a compost pile?",
    "What materials are good sources of nitrogen?",
    "What are high-carbon materials for compost?",
    "Why is aeration important in composting?",
    "How do we know when compost is ready to use?",
    "What is the best way to balance C:N ratio?",
    "Can we compost citrus peels and onions?",
    "What happens if compost lacks oxygen?",
    "How do earthworms help in composting?",
    "Why does compost sometimes attract insects?",
    "What are the benefits of aerobic composting?",
    "Can composting be done indoors?",
    "How can composting help reduce waste?",
    "What are common mistakes in composting?",
    "Why does compost become too hot sometimes?",
    "Can meat or dairy be composted safely?",
    "How can we speed up compost decomposition?",
    "What role does pH play in composting?",
    "Why is shredding materials before composting useful?",
    "What are the signs of poor compost aeration?",
    "Can composting produce methane gas?",
    "What is vermicomposting and how is it different?",
    "How do brown and green materials differ in composting?",
    "What are the advantages of using mature compost in soil?",
    "How does composting benefit sustainable farming?"
]

# === Run RAG and Collect Responses ===
results = []
print("\n--- Running RAG for 30 User Queries ---")

for query in user_queries:
    start_time = time.time()
    retrieved_chunks = query_documents(query, n_results=3)
    rag_output = generate_response(query, retrieved_chunks)
    end_time = time.time()

    print(f"✔ Processed: {query} ({round(end_time - start_time, 2)}s)")
    results.append({
        "User Query": query,
        "RAG Output": rag_output
    })

# === Save to Excel ===
output_path = "rag_outputs_30_queries.xlsx"
pd.DataFrame(results).to_excel(output_path, index=False)

print(f"\n✅ All 30 queries processed and saved to: {output_path}")
