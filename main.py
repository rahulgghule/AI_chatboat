import streamlit as st
from langchain_community.llms import Ollama

# Set up Streamlit UI with dark blue theme
st.set_page_config(page_title="Simple Chatbot", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #0D1B2A;
            color: #FFFFFF;
        }
        .message-container {
            width: 80%;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .user-message {
            background-color: rgba(100, 100, 100, 0.3);
            text-align: left;
            margin-left: 20%;
        }
        .bot-message {
            background-color: rgba(50, 50, 50, 0.3);
            text-align: left;
            margin-right: 20%;
        }
        h1 {
            text-align: center;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

# Title at the top
st.markdown("<h1>Simple Chatbot</h1>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="message-container user-message">🧑‍💻 {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="message-container bot-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask something...")

if user_input:
    # Append user input to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # ✅ Use Ollama AI model to generate a response
    llm = Ollama(model="mistral")  # You can use "llama2" or "gemma" as well
    bot_response = llm.invoke(user_input)

    # Append AI response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    # Rerun the script to update UI
    st.rerun()
