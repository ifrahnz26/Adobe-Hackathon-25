python
import fitz
import json
import os
import datetime
from sentence_transformers import SentenceTransformer, util

# Configuration: This model is small (~90MB), fast, and works offline after download.
MODEL_NAME = 'all-MiniLM-L6-v2'
INPUT_DIR = "/app/input"
OUTPUT_FILE = "/app/output/challenge1b_output.json"

def chunk_document(pdf_path):
    """
    Chunks a document into sections based on font size.
    This is a basic implementation; a more advanced one could use the 1A logic.
    """
    print(f"Chunking document: {os.path.basename(pdf_path)}")
    chunks = []
    try:
        doc = fitz.open(pdf_path)
        # For simplicity, we'll treat each text block as a chunk.
        # A better approach would be to group text under headings from 1A.
        for page_num, page in enumerate(doc):
            text_blocks = page.get_text("blocks")
            for i, block in enumerate(text_blocks):
                text = block[4].strip()
                if text:
                    chunks.append({
                        'title': f"Page {page_num + 1}, Block {i}", # Placeholder title
                        'text': text,
                        'page': page_num + 1,
                        'doc': os.path.basename(pdf_path)
                    })
        doc.close()
    except Exception as e:
        print(f"Error chunking {os.path.basename(pdf_path)}: {e}")
    return chunks

def run_persona_driven_analysis(doc_paths, persona, job):
    """Main logic for Round 1B using semantic search."""
    print("Loading semantic model...")
    # The model is downloaded to a cache and runs offline from there.
    model = SentenceTransformer(MODEL_NAME)

    all_chunks = [chunk for doc_path in doc_paths for chunk in chunk_document(doc_path)]
    if not all_chunks: return {}

    print("Creating embeddings for query and document chunks...")
    query = f"{persona}: {job}"
    chunk_texts = [chunk['text'] for chunk in all_chunks]
    
    query_embedding = model.encode(query, convert_to_tensor=True)
    chunk_embeddings = model.encode(chunk_texts, convert_to_tensor=True)

    print("Calculating relevance scores...")
    cosine_scores = util.cos_sim(query_embedding, chunk_embeddings)[0]

    ranked_chunks = sorted(enumerate(cosine_scores), key=lambda x: x[1], reverse=True)
    
    extracted_sections = []
    for rank, (chunk_index, score) in enumerate(ranked_chunks):
        if score < 0.1: continue # Score threshold to filter irrelevant chunks
        chunk_data = all_chunks[chunk_index]
        extracted_sections.append({
            "document": chunk_data['doc'],
            "page_number": chunk_data['page'],
            "section_title": chunk_data['title'],
            "importance_rank": rank + 1
        })
    
    # Placeholder for sub-section analysis
    sub_section_analysis = []
    if extracted_sections:
        sub_section_analysis.append({
            "document": extracted_sections[0]['document'],
            "page_number": extracted_sections[0]['page_number'],
            "refined_text": "Refined text analysis needs to be implemented."
        })

    return {
        "metadata": {
            "input_documents": [os.path.basename(p) for p in doc_paths],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        },
        "extracted_sections": extracted_sections,
        "sub_section_analysis": sub_section_analysis
    }

if _name_ == '_main_':
    # These inputs should be read from a config file or environment variables in a real scenario
    sample_persona = "Investment Analyst"
    sample_job = "Analyze revenue trends, R&D investments, and market positioning strategies"
    
    doc_paths = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR) if f.lower().endswith('.pdf')]
    
    if doc_paths:
        final_output = run_persona_driven_analysis(doc_paths, sample_persona, sample_job)
        if not os.path.exists(os.path.dirname(OUTPUT_FILE)):
            os.makedirs(os.path.dirname(OUTPUT_FILE))
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(final_output, f, indent=4)
        print(f"\nAnalysis complete. Output saved to {OUTPUT_FILE}")
    else:
        print(f"No PDF files found in {INPUT_DIR})
