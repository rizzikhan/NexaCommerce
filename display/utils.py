# import os
# from PyPDF2 import PdfReader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings

# def process_pdf(file_path):
#     """Extract text from a PDF and generate a FAISS index."""
#     text = ''
#     pdf_reader = PdfReader(file_path)
#     for page in pdf_reader.pages:
#         text += page.extract_text() or ''
    
#     # Split text into chunks
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     text_chunks = text_splitter.split_text(text)
    
#     # Generate embeddings and FAISS index
#     embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
#     vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    
#     # Save FAISS index
#     os.makedirs('shared_storage/vectorstore', exist_ok=True)
#     vector_store.save_local('shared_storage/vectorstore/faiss_index')
#     return True
