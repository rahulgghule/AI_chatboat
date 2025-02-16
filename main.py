import streamlit as st
import faiss
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama

# Set up Streamlit UI
st.set_page_config(page_title="RAGBot - PDF Q&A", layout="wide")

# Title at the top
st.markdown("<h1 style='text-align: center;'>📄 RAGBot - PDF Q&A</h1>", unsafe_allow_html=True)

# Upload PDF File
uploaded_file = st.file_uploader("📂 Upload a PDF file", type="pdf")

if uploaded_file:
    pdf_path = os.path.join("docs", uploaded_file.name)
    
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load & extract text from PDF
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_docs = text_splitter.split_documents(docs)

    # Create vector database
    embeddings = OllamaEmbeddings(model="mistral")  # Use 'gemma' or 'llama2'
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    # Save FAISS index
    vectorstore.save_local("faiss_index")

    st.success("✅ PDF Uploaded & Processed! You can now ask questions.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        role = "🧑‍💻 You" if message["role"] == "user" else "🤖 AI"
        st.markdown(f"**{role}:** {message['content']}")

    # Chat input
    user_input = st.chat_input("Ask a question about the PDF...")

    if user_input:
        # Append user question
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Load FAISS index
        vectorstore = FAISS.load_local("faiss_index", embeddings)

        # Retrieve relevant text from PDF
        docs = vectorstore.similarity_search(user_input, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])

        # Use Ollama to generate answer
        llm = Ollama(model="mistral")
        prompt = f"Answer based on the provided context:\n\n{context}\n\nQuestion: {user_input}"
        response = llm.invoke(prompt)

        # Append AI response
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display AI response
        st.markdown(f"**🤖 AI:** {response}")
