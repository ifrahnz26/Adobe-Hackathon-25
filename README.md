# Adobe-Hackathon-25

# Adobe Hackathon 2025 - Round 1A Submission

[cite_start]This project extracts a structured outline (Title, H1, H2, H3) from PDF files. [cite: 30]

## [cite_start]Approach [cite: 89]
The solution uses the PyMuPDF library to perform a stylistic analysis of the text.

1.  *Font Profiling*: The script first finds the most common font size, assuming it represents the body text.
2.  *Heading Identification*: It identifies text with a font size larger than the body text as potential headings.
3.  *Level Classification*: These candidates are grouped by font size. The largest sizes are classified as H1, the next largest as H2, and so on.
4.  *Title Extraction*: The title is assumed to be the first H1-level heading found on the initial pages.

## [cite_start]Libraries Used [cite: 90]
* *PyMuPDF (fitz)*: A high-performance Python library for PDF parsing, chosen for speed and detailed attribute access.

## [cite_start]How to Build and Run [cite: 93]

### Build the Docker Image
This command must be run from the project's root directory.

sh
docker build --platform linux/amd64 -t solution1a:latest .
Run the Docker Container
Place your input PDFs into a local directory (e.g., ./input). Create an empty output directory (e.g., ./output). Then, run the container using the command specified in the challenge instructions. 

Bash

docker run --rm \
  -v "$(pwd)/input:/app/input" \
  -v "$(pwd)/output:/app/output" \
  --network none \
  solution1a:latest
The container will process each PDF in 

/app/input and generate a corresponding .json file in /app/output. 
