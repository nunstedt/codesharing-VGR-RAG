from llama_index.core import Document
from docling.document_converter import DocumentConverter
from llama_index.core.node_parser import SentenceSplitter 
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.ollama import OllamaEmbedding
import re
import os
import hashlib
import csv
import time 
import fitz  # PyMuPDF
import glob

from pypdf import PdfReader

pdf_folder = "./pdf_folder"
csv_db = "./db.csv"
chunk_folder = "./chunks_test"


# pdf conversion logic
def conversion(filepath):
    #create markdown file from source file

    file_size_bytes = os.path.getsize(filepath)  # Get file size in bytes
    file_size_kb = file_size_bytes / 1024  # Convert to kilobytes
    filename = os.path.basename(filepath)  # Get just the file name
    start = time.time()
    print(f"👉 Converting new document {filename} of size: {file_size_kb:.2f} kB to markdown")

    source_file = filepath
    source_file = source_file.replace("\\", "/")
    converter = DocumentConverter()
    result_convert = converter.convert(source_file)
    markdown_converstion = result_convert.document.export_to_markdown()
    print(f"Conversion took: {time.time() - start:.2f} seconds")

    #clean data
    clean_start = time.time()
    remove_EN = re.sub(r'\s*\bEN\b\s*', ' ', markdown_converstion)
    remove_Value = re.sub(r'\s*\bL  333/164\b\s*', ' ', remove_EN)
    remove_Value2 = re.sub(r'\b\d+(?:\.\d+)+\b', '', remove_Value)
    remove_Value3 = re.sub(r"\b\d+\s+(OJ C\s+\d+,\s*,\s*)?p\.\s*\d+\b", '', remove_Value2) 
    remove_imageTag = remove_Value3.replace("<!-- image -->", "")

    #print(remove_imageTag)


    # Optional: removel extra lines from the markdown document
    def remove_extra_blank_lines(text):
        lines = text.splitlines()
        cleaned_lines = [line for line in lines if line.strip() != ""]
        return "\n".join(cleaned_lines)

    cleaned_text = remove_extra_blank_lines(remove_imageTag)
    print(f"Data cleaning took: {time.time() - clean_start:.2f} seconds")

    # Chunk data
    chunk_start = time.time()
    embed_model = OllamaEmbedding(
        model_name="mxbai-embed-large",)

    splitter = SemanticSplitterNodeParser(
        buffer_size=5, breakpoint_percentile_threshold=95, embed_model=embed_model)

    #base_splitter = SentenceSplitter(chunk_size=512)
    doc = Document(text=cleaned_text)
    nodes = splitter.get_nodes_from_documents([doc])
    print(f"Chunking took: {time.time() - chunk_start:.2f} seconds")


    # save as nodes to a file

    output_folder = chunk_folder
    os.makedirs(output_folder, exist_ok=True)

    for i, doc in enumerate(nodes):
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        output_filename = f"{base_name}_{i+1:03d}.md"
        output_path = os.path.join(output_folder, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
         f.write(doc.text)
    print(f"Saved {output_path}")



# compute file hash
def compute_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

# load previous hashes from CSV database
def load_processed_hashes(csv_file):
    hashes = set()
    if not os.path.exists(csv_file):
        return hashes
    try:
        with open(csv_file, newline='', encoding ='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if row:
                    hashes.add(row[0])
    except UnicodeDecodeError:
    # Code added to handle encoding error for mac (Frida)
        print("⚠️ UTF-8 decode failed — trying ISO-8859-1 fallback.")
        with open(csv_file, newline='', encoding='ISO-8859-1') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row:
                    hashes.add(row[0])
    return hashes

# append new hashes to CSV database

#def append_processed_file(csv_file, file_hash, filename):
 #   file_exists = os.path.exists(csv_file)
  #  with open(csv_file, 'a', newline='') as f:
   #     writer = csv.writer(f)
    #    if not file_exists:
     #       writer.writerow(['file_hash', 'original_filename'])
      #  writer.writerow([file_hash, filename])

def append_processed_file(csv_file, file_hash, filename):
    file_exists = os.path.exists(csv_file)
    write_header = not file_exists or os.path.getsize(csv_file) == 0
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(['file_hash', 'original_filename'])
        writer.writerow([file_hash, filename])

def get_pdf_titles(pdf_folder):
    """Return a dict mapping base filename (without extension) to PDF title."""
    titles = {}
    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith('.pdf'):
            base = os.path.splitext(filename)[0]
            try:
                reader = PdfReader(os.path.join(pdf_folder, filename))
                title = reader.metadata.get('/Title', '') if reader.metadata else ''
                titles[base] = title
            except Exception:
                titles[base] = ''
    return titles


def get_pdf_date(pdf_folder):

    dates= {}
    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith('.pdf'):
            base = os.path.splitext(filename)[0]
            try:
                reader = PdfReader(os.path.join(pdf_folder, filename))
                date = reader.metadata.get('/CreationDate', '') if reader.metadata else ''
                dates[base] = date
            except Exception:
                dates[base] = ''

    return dates


# load markdown nodes from a folder N0TE: this function is named parse_and_get_nodes for compatibility reasons
def parse_and_get_nodes(folder: str) -> list:
    print(f"Loading markdown nodes from folder: {folder}")
    nodes = []
    pdf_titles = get_pdf_titles(pdf_folder)
    pdf_dates = get_pdf_date(pdf_folder)
    for filename in os.listdir(folder):
        if filename.lower().endswith('.md'):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath):
                with open(filepath, encoding="utf-8") as f:
                    content = f.read()
                    # Remove the chunk suffix (e.g., _001) to get the original PDF base name
                    base_name = os.path.splitext(filename)[0]
                    pdf_base = base_name.rsplit('_', 1)[0]  # This splits at the last underscore
                    title = pdf_titles.get(pdf_base, '')
                    date = pdf_dates.get(pdf_base, '')
                    nodes.append(Document(
                        text=content,
                        metadata={
                            "pdf_title": title,
                            "pdf_date": date
                        }
                    ))
    print(f"Success !!")                
    return nodes

# Main processing loop

def process_all_files(folder_path):
    import time
    total_start = time.time()
    processed_hashes = load_processed_hashes(csv_db)

    for root, _, files in os.walk(folder_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            if not os.path.isfile(filepath):
                continue

            file_hash = compute_file_hash(filepath)

            if file_hash in processed_hashes:
                print(f"Skipping: {filename} (already processed)")
                continue

            # === Your file processing logic ===
            print(f"Processing: {filename}")
            file_start = time.time()
            append_processed_file(csv_db, file_hash, filename)
            conversion(filepath)
            print(f"[TIMER] Processing {filename} took {time.time() - file_start:.2f} seconds.")
    print(f"[TIMER] process_all_files total time: {time.time() - total_start:.2f} seconds.")


def prepare_pdfs(pdf_folder):
    folder_path = "unprocessed_pdf_folder"
    new_folder_path = pdf_folder
    
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    for pdf_path in pdf_files:
    # Extract the base filename without the .pdf extension
        filename = os.path.basename(pdf_path)
        title = filename.removesuffix(".pdf")  # Python 3.9+

    # Open the PDF
        doc = fitz.open(pdf_path)

    # Set metadata
        doc.set_metadata({
            "title": title,
            # Add more metadata fields here if needed
        })

        # if "AI" in title:
        #     doc.set_metadata({
        #     "supplementary": "AI",
        #     # Add more metadata fields here if needed
        # })
                    
        

    # Save the updated PDF to a new file (or overwrite original if preferred)
        output_path = os.path.join(new_folder_path, f"{title}.pdf")
        doc.save(output_path)
        doc.close()

    #print(f"Saved: {output_path}")


#prepare_pdfs(pdf_folder)

process_all_files(pdf_folder)

parse_and_get_nodes(chunk_folder) # this function is named parse_and_get_nodes for compatibility reasons
# it actually loads the chunked nodes from the folder and returns them as a list of Document nodes

