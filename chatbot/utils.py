import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai.llms import GoogleGenerativeAI

def process_pdf(file_path):
    text = ''
    pdf_reader = PdfReader(file_path)
    for page in pdf_reader.pages:
        text += page.extract_text() or ''
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    text_chunks = text_splitter.split_text(text)
    
    embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    
    os.makedirs('shared_storage/vectorstore', exist_ok=True)
    vector_store.save_local('shared_storage/vectorstore/faiss_index')
    return True


def load_vector_store():
    faiss_index_path = os.path.join('shared_storage', 'vectorstore', 'faiss_index')
    embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    
    faiss_file = os.path.join(faiss_index_path, 'index.faiss')
    pkl_file = os.path.join(faiss_index_path, 'index.pkl')
    
    if os.path.exists(faiss_file) and os.path.exists(pkl_file):
        return FAISS.load_local(
            folder_path=faiss_index_path,
            embeddings=embeddings,
            index_name='index',
            allow_dangerous_deserialization=True
        )
    else:
        raise FileNotFoundError("FAISS index files not found. Please ensure Admin App has generated them.")


def query_vector_store(question):
    try:
        vector_store = load_vector_store()
        retriever = vector_store.as_retriever()
        relevant_chunks = retriever.get_relevant_documents(question)
        
        context = "\n".join(chunk.page_content for chunk in relevant_chunks)

        llm = GoogleGenerativeAI(model="gemini-1.5-flash")
        
        response = llm.predict(f"Context: {context}\nQuestion: {question}")
        return response
    except Exception as e:
        return f"Error: {e}"
