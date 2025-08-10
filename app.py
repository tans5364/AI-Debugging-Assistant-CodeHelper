import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)



# Inject custom CSS with enhanced styling and Google Fonts
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        /* Global Styling */
        .main {
            background: linear-gradient(135deg, #f0f4ff, #ffffff);
            color: #333333;
            font-family: 'Poppins', sans-serif;
        }
        
        /* Sidebar Styling */
        .sidebar .sidebar-content {
            background: linear-gradient(135deg, #e8f0fe, #ffffff);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
            border: none;
        }
        
        /* Input and Dropdown Styling */
        .stTextInput textarea, .stSelectbox div[data-baseweb="select"] {
            color: #333333 !important;
            background-color: #ffffff !important;
            border: 1px solid #d1d9e6 !important;
            border-radius: 8px !important;
            padding: 12px;
            transition: all 0.3s ease;
        }
        .stTextInput textarea:focus, .stSelectbox div[data-baseweb="select"]:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 8px rgba(102, 126, 234, 0.6);
        }
        .stSelectbox div[data-baseweb="select"] {
            color: #333333 !important;
            background-color: #ffffff !important;
            border-radius: 8px;
            padding: 12px;
            border: 1px solid #d1d9e6;
        }
        .stSelectbox svg {
            fill: #333333 !important;
        }
        div[role="listbox"] div {
            background-color: #ffffff !important;
            color: #333333 !important;
            border: 1px solid #d1d9e6;
        }
        
        /* Sidebar Headers */
        .sidebar .stHeader {
            font-size: 22px;
            font-weight: 600;
            color: #4c6ef5;
            margin-bottom: 20px;
        }
        
        /* App Title Styling */
        h1 {
            text-align: center;
            font-size: 3.5rem;
            color: #4c6ef5;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        /* Subtitle Styling */
        .stCaption {
            text-align: center;
            font-size: 1.3rem;
            color: #555555;
            margin-bottom: 30px;
        }
        
        /* Divider Styling */
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(to right, #4c6ef5, #b197fc);
            margin: 25px 0;
        }
        
        /* Glowing Header Animation */
        @keyframes glow {
            0% { text-shadow: 0 0 10px #4c6ef5; }
            50% { text-shadow: 0 0 20px #4c6ef5; }
            100% { text-shadow: 0 0 10px #4c6ef5; }
        }
        .glowing-text {
            animation: glow 2s infinite ease-in-out;
        }
    </style>
""", unsafe_allow_html=True)

# App Title and Subtitle
st.markdown(
    """
    <h1 style='text-align: center;'>CodexAI</h1>
    <h2 style='text-align: center;'>The Code Companion</h3>
    """,
    unsafe_allow_html=True
)
st.markdown('<p class="stCaption">Elevate Your Coding Experience with AI Magic</p>', unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.markdown('<h3 class="glowing-text">✨ Configuration</h3>', unsafe_allow_html=True)
selected_model = st.sidebar.selectbox(
    "Choose Model",
    ["deepseek-r1:1.5b", "deepseek-r1:3b"],
    index=0
)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown('<h3 class="glowing-text">🚀 Model Capabilities</h3>', unsafe_allow_html=True)
st.sidebar.markdown("""
- **Python Mastery**
- **Smart Debugging**
- **Detailed Documentation**
- **Innovative Solutions**
""", unsafe_allow_html=True)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("Built with [Ollama](https://ollama.ai/) | [LangChain](https://python.langchain.com/)")


# initiate the chat engine

llm_engine=ChatOllama(
    model=selected_model,
    base_url="http://localhost:11434",

    temperature=0.3

)

# System prompt configuration
system_prompt = SystemMessagePromptTemplate.from_template(
    "You are an expert AI coding assistant. Provide concise, correct solutions "
    "with strategic print statements for debugging. Always respond in English."
)

# Session state management
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "Hi! I'm DeepSeek. How can I help you code today? 💻"}]

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    for message in st.session_state.message_log:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input and processing
user_query = st.chat_input("Type your coding question here...")

def generate_ai_response(prompt_chain):
    processing_pipeline=prompt_chain | llm_engine | StrOutputParser()
    return processing_pipeline.invoke({})

def build_prompt_chain():
    prompt_sequence = [system_prompt]
    for msg in st.session_state.message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence)

if user_query:
    # Add user message to log
    st.session_state.message_log.append({"role": "user", "content": user_query})
    
    # Generate AI response
    with st.spinner("🧠 Processing..."):
        prompt_chain = build_prompt_chain()
        ai_response = generate_ai_response(prompt_chain)
    
    # Add AI response to log
    st.session_state.message_log.append({"role": "ai", "content": ai_response})
    
    # Rerun to update chat display
    st.rerun()
