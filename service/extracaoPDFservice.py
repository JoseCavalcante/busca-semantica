from fastapi import UploadFile
import fitz # PyMuPDF
import re
from datetime import datetime
from docx import Document
from io import BytesIO

# Regex patterns for entities
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
PHONE_REGEX = r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}'
URL_REGEX = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'

# ... (extract_entities remains same, skipping for brevity in replacement if possible, but replace tool needs context. I will assume extract_entities is fine and just update imports and the function)
# ACTUALLY, I need to update imports at the top first. I will do a larger replacement or multiple chunks. Let's do the function first.

def extract_docx_metadata(filedocx: UploadFile):
    # Reset cursor
    filedocx.file.seek(0)
    content_bytes = filedocx.file.read()
    
    doc = Document(BytesIO(content_bytes))
    full_text = []
    
    for para in doc.paragraphs:
        full_text.append(para.text)
        
    text_content = "\n".join(full_text)
    entities = extract_entities(text_content)
    
    doc_metadata = {
        "filename": filedocx.filename,
        "file_size": len(content_bytes),
        "page_count": 1 # DOCX doesn't have strict pages like PDF
    }
    
    return {
        "metadata": doc_metadata,
        "content": [{
            "page_number": 1,
            "text": text_content,
            "entities": entities
        }],
        "full_text": text_content
    }

def extract_entities(text: str):
    return {
        "emails": list(set(re.findall(EMAIL_REGEX, text))),
        "phones": list(set(re.findall(PHONE_REGEX, text))),
        "links": list(set(re.findall(URL_REGEX, text)))
    }

def extract_pdf_metadata(filepdf: UploadFile):
    # Reset cursor
    filepdf.file.seek(0)
    pdf_bytes = filepdf.file.read()
    
    doc_metadata = {}
    pages_content = []
    full_text = []

    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        # 1. Global Metadata
        doc_metadata = {
            "filename": filepdf.filename,
            "page_count": doc.page_count,
            "author": doc.metadata.get("author", ""),
            "creation_date": doc.metadata.get("creationDate", ""),
            "title": doc.metadata.get("title", ""),
            "file_size": len(pdf_bytes)
        }

        # 2. Page Content & Entities
        for page_num, page in enumerate(doc):
            text = page.get_text()
            if text:
                entities = extract_entities(text)
                stats = {
                    "word_count": len(text.split()),
                    "char_count": len(text)
                }
                
                pages_content.append({
                    "page_number": page_num + 1,
                    "text": text,
                    "entities": entities,
                    "stats": stats
                })
                full_text.append(text)

    return {
        "metadata": doc_metadata,
        "content": pages_content,
        "full_text": "\n".join(full_text)
    }



#function to extract text from a pdf file (Legacy wrapper)
def extract_text_from_pdf(filepdf: UploadFile):
    result = extract_pdf_metadata(filepdf)
    return result["full_text"]

#function to make split the text into chunk
# esta funcao retorna uma lista
def split_text_into_chunks(text:str, chunk_size=300, overlap=50) -> list: 
    chunks = []
    # Ensure overlap is less than chunk_size to avoid infinite loop
    if overlap >= chunk_size:
        overlap = chunk_size // 2

    # If text is shorter than chunk size, return it as single chunk
    if len(text) <= chunk_size:
        return [text]

    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
        
        # Stop if we've reached the end
        if i + chunk_size >= len(text):
            break
            
    return chunks