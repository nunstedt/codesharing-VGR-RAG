import streamlit as st
import os
import json
from chat_session import ComplianceChatSession
from mode_logic import run_compliance_mode
from data_init import initialize_data_and_index
from main import KNOWN_TITLES
from LLM import get_llm
from llama_index.core import Settings
from query_handler import display_response

#Styling using CSS (workaround)
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] ul li:nth-child(5) {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>

    /* Title */
    .page-title {
        font-size: 2rem;
        font-weight: 700;
        text-align: center;
        margin-top: 1.0rem;
        margin-bottom: 2.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">Compliance assistant</div>', unsafe_allow_html=True)
st.set_page_config(page_title="Compliance Assistant", layout="wide")

# Variable to check for active mode and seperate them
MODE = "compliance_assistant"
st.session_state_active_mode = MODE

#Configuration for RAG
Settings.llm = get_llm()

@st.cache_resource
def get_vector_index():
    _, _, vector_index = initialize_data_and_index()
    return vector_index

vector_index = get_vector_index()
known_titles = KNOWN_TITLES

SYSTEMS_DIR = "./system_profile"

#Load systems from profile
system_files = [f for f in os.listdir(SYSTEMS_DIR) if f.endswith(".json")]
systems = []

for file in system_files:
    with open(os.path.join(SYSTEMS_DIR, file), "r") as f:
        data = json.load(f)
        data["file_name"] = file
        systems.append(data)

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}
if "selected_system" not in st.session_state:
    st.session_state.selected_system = None
if "chat_engines" not in st.session_state:
    st.session_state.chat_engines = {}

chat_session = st.session_state.chat_sessions.get(MODE)
chat_history = st.session_state.chat_histories.get(MODE, [])

#Load system descriptions for system selection UI
system_descriptions = [f for f in os.listdir(SYSTEMS_DIR) if f.endswith(".txt")]


#UI system selection
st.markdown("Choose a system to get tailored compliance guidance:")
cols = st.columns(len(systems) if systems else 1)

for idx, system in enumerate(systems):
    name = system.get("system_name", f"System {idx+1}")
    description = system.get("functionality", "No description available.")
    json_file_name = system["file_name"]
    txt_file_name = os.path.splitext(json_file_name)[0] + ".txt"
    txt_path = os.path.join(SYSTEMS_DIR, txt_file_name)

    # Load description from .txt file
    system_description = ""
    if os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as txt_file:
            system_description = txt_file.read()
    else:
        system_description = "No additional description found."

    with cols[idx]: 
        is_selected = st.session_state.selected_system == name

        # Expand to read full descr
        with st.expander(f"📄 {name}"):
            st.markdown(system_description)

        if st.button("Select", key=f"use_btn_{idx}"):
            st.session_state.selected_system = name
            chat_session = ComplianceChatSession(vector_index, known_titles, system_description)
            st.session_state.chat_sessions[MODE] = chat_session
            st.session_state.chat_engines[MODE] = chat_session.create_chat_engine()
            st.session_state.chat_histories[MODE] = []
            chat_history = []

st.divider()

# Chat interface
if "selected_system" in st.session_state and st.session_state.selected_system:
    st.subheader(f"Compliance assistant for: {st.session_state.selected_system}")

    chat_session = st.session_state.chat_sessions[MODE]
    chat_history = st.session_state.chat_histories.get(MODE, [])

    if not chat_history:
        st.chat_message("assistant").write(
            f"Great, let's dive in to actions towards compliance for **{st.session_state.selected_system}**.\n"
            f"Ask any question to get started."
        )

    for msg in chat_history:
        st.chat_message(msg["role"]).write(msg["content"])


    user_input = st.chat_input(
        f"What do you need assistance with? Ask questions and get tips related to {st.session_state.selected_system}..."
    )
    # Chat logic sync
    if user_input and chat_session:
        st.chat_message("user").write(user_input)
        chat_engine = st.session_state.chat_engines[MODE]
        language, filters, custom_prompts = chat_session.process_question(user_input, chat_engine)
        response = chat_engine.chat(user_input, filters=filters, custom_prompts=custom_prompts)

        st.session_state.chat_histories[MODE].append({"role": "user", "content": user_input})
        st.session_state.chat_histories[MODE].append({"role": "assistant", "content": response.response})
        st.chat_message("assistant").write(response.response)
else:
    st.info("Select a system to start chatting with the compliance assistant.")
