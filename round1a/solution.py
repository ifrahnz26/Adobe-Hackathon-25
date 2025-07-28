import fitz  # PyMuPDF
import json
import os
from collections import Counter

def get_font_statistics(doc):
    """Analyzes the document to find the most common font size."""
    font_sizes = Counter()
    for page in doc:
        blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_FONT)
        for block in blocks["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_sizes[round(span["size"])] += len(span["text"].split())
    
    if not font_sizes:
        return 12 # Default body size
    return font_sizes.most_common(1)[0][0]

def extract_outline(pdf_path):
    """Extracts the title and H1, H2, H3 headings from a PDF."""
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening {pdf_path}: {e}")
        return {"title": "", "outline": []}

    if not doc or doc.page_count == 0:
        return {"title": "", "outline": []}

    body_text_size = get_font_statistics(doc)
    
    heading_candidates = {}
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict", flags=fitz.TEXTFLAGS_FONT)["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_size = round(span["size"])
                        text = span["text"].strip()
                        # Heading condition: larger than body text, not excessively long, and has content.
                        if font_size > body_text_size and 0 < len(text.split()) < 20:
                            if font_size not in heading_candidates:
                                heading_candidates[font_size] = []
                            # Avoid duplicate headings on the same page
                            if not any(h['text'] == text and h['page'] == page_num + 1 for h in heading_candidates[font_size]):
                                heading_candidates[font_size].append({"text": text, "page": page_num + 1})

    sorted_heading_sizes = sorted(heading_candidates.keys(), reverse=True)
    
    heading_levels = {}
    if len(sorted_heading_sizes) > 0: heading_levels["H1"] = sorted_heading_sizes[0]
    if len(sorted_heading_sizes) > 1: heading_levels["H2"] = sorted_heading_sizes[1]
    if len(sorted_heading_sizes) > 2: heading_levels["H3"] = sorted_heading_sizes[2]

    title = ""
    if "H1" in heading_levels:
        for heading in heading_candidates[heading_levels["H1"]]:
            if heading["page"] <= 2:  # Assume title is in the first 2 pages
                title = heading["text"]
                break

    all_headings = []
    for level_name, size in heading_levels.items():
        for heading in heading_candidates.get(size, []):
            if heading["text"] == title: continue
            all_headings.append({"level": level_name, "text": heading["text"], "page": heading["page"]})
            
    outline = sorted(all_headings, key=lambda x: (x['page'], -ord(x['level'][-1])))

    doc.close()
    return {"title": title, "outline": outline}

def process_all_pdfs(input_dir, output_dir):
    """Processes all PDFs in the input directory and saves JSON output."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            json_output = extract_outline(pdf_path)
            
            output_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'w') as f:
                json.dump(json_output, f, indent=4)
            print(f"Processed {filename} -> {output_filename}")

if _name_ == '_main_':
    INPUT_DIR = "/app/input"
    OUTPUT_DIR = "/app/output"
    process_all_pdfs(INPUT_DIR, OUTPUT_DIR)
