# Adobe-Hackathon-25

# Adobe Hackathon 2025 - Round 1A Submission
This project extracts a structured outline (Title, H1, H2, H3) from PDF files. [cite: 30]

The solution uses the PyMuPDF library to perform a stylistic analysis of the text.

1.  *Font Profiling*: The script first finds the most common font size, assuming it represents the body text.
2.  *Heading Identification*: It identifies text with a font size larger than the body text as potential headings.
3.  *Level Classification*: These candidates are grouped by font size. The largest sizes are classified as H1, the next largest as H2, and so on.
4.  *Title Extraction*: The title is assumed to be the first H1-level heading found on the initial pages.

* *PyMuPDF (fitz)*: A high-performance Python library for PDF parsing, chosen for speed and detailed attribute access.


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

# Adobe Hackathon 2025 - Round 1B Submission
Run the Docker Container
Place your input PDFs into a local ./input directory and create an empty ./output directory.

Bash

docker run --rm \
  -v "$(pwd)/input:/app/input" \
  -v "$(pwd)/output:/app/output" \
  solution1b:latest
Note: The first run will require internet access for the container to download the sentence-transformer model. Subsequent runs will use the cached model and can be executed fully offline with --network none.
