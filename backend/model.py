import json
import os
from langchain_community.llms import Ollama

# Ensure chat history file exists
CHAT_HISTORY_FILE = "data/chat_history.json"
os.makedirs("data", exist_ok=True)
if not os.path.exists(CHAT_HISTORY_FILE):
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump([], f)

# Load Chat History
def load_chat_history():
    with open(CHAT_HISTORY_FILE, "r") as f:
        return json.load(f)

# Save Chat History
def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# Generate AI Response
def get_ai_response(user_input):
    llm = Ollama(model="mistral")  
    response = llm.invoke(user_input)
    
    # Save the conversation
    history = load_chat_history()
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": response})
    save_chat_history(history)
    
    return response
