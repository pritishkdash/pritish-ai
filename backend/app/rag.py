'''import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PDF_PATH = os.path.join(BASE_DIR, "../data/pritish_cv.pdf")
DB_PATH = os.path.join(BASE_DIR, "../vectorstore")
#DB_PATH = "vectorstore"
#PDF_PATH = "data/pritish_cv.pdf"

def create_vectorstore():
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    db = FAISS.from_documents(docs, embeddings)
    db.save_local(DB_PATH)

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)

# ✅ FIXED LOGIC
if not os.path.exists(f"{DB_PATH}/index.faiss"):
    print("⚡ Creating vector database...")
    create_vectorstore()

db = load_vectorstore()

def retrieve(query):
    docs = db.similarity_search(query, k=3)
    return " ".join([d.page_content for d in docs])'''



import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../vectorstore")

def load_vectorstore():
    print("✅ Loading vectorstore (light mode)...")

    # 🔥 NO HEAVY MODEL
    embeddings = FakeEmbeddings(size=384)

    return FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

db = load_vectorstore()

def retrieve(query):
    docs = db.similarity_search(query, k=3)
    return " ".join([d.page_content for d in docs])
