import streamlit as st
from llama_index.core import Settings
from LLM import get_llm
from data_init import initialize_data_and_index
from chat_session import QAChatSession  # general-purpose chat session
from main import KNOWN_TITLES
from query_handler import display_response

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

st.markdown('<div class="page-title">Regulation navigator</div>', unsafe_allow_html=True)
# Configure LLM
Settings.llm = get_llm()

st.set_page_config(page_title="Regulation Navigator", layout="wide")

# Hardcoded version for documents, could also be list of docs in folder
documents = [
    "EU AI Act",
    "Critical Entity Resilience (CER)",
    "ISO standard 27002",
    "Medical Device Regulation (MDR)",
    "NIS2 Directive",
    "Kontinuitetshantering av IS-IT-tjänst",
    "Policy för säkerhet och beredskap",
    "Commission Guidelines on AI prohibition",
    "Protective Security Act"
]

st.markdown("Documents in the database:")

cards_html = """
<style>
.carousel-container {
  display: flex;
  gap: 1.5rem;
  overflow-x: auto;
  padding: 1rem 0;
  scroll-snap-type: x mandatory;
  scrollbar-width: thin;
}
.carousel-container::-webkit-scrollbar {
  height: 6px;
}
.carousel-container::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 10px;
}
.carousel-card {
  flex: 0 0 auto;
  scroll-snap-align: start;
  background: #fafafa;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 1rem;
  width: 200px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  transition: transform .2s, box-shadow .2s;
  text-align: center;
}
.carousel-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.carousel-title {
  font-size: 1.1rem;
  font-weight: 600;
}
</style>

<div class="carousel-container">
"""
for title in documents:
    cards_html += f"""
  <div class="carousel-card">
    <div class="carousel-title">{title}</div>
  </div>
"""
cards_html += "</div>"

st.markdown(cards_html, unsafe_allow_html=True)

# RAG config
@st.cache_resource
def get_vector_index():
    _, _, vector_index = initialize_data_and_index()
    return vector_index

vector_index = get_vector_index()
known_titles = KNOWN_TITLES

# Set the chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = QAChatSession(vector_index, known_titles)
    st.session_state.chat_engine = st.session_state.chat_session.create_chat_engine()
    st.session_state.chat_history = []
    st.session_state.first_turn = True

st.divider()

# Chat interface
st.subheader("Regulation navigator chat")

if not st.session_state.chat_history:
    st.chat_message("assistant").write(
        f"What do you want to learn more about?\n"
        "You can always read the full PDF by clicking the document."
    )

for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])


user_input = st.chat_input(
    f"Ask anything about the regulations..."
)
#Chat logic
if user_input:
    st.chat_message("user").write(user_input)

    # Use the selected regulation to filter results
    # title_filter = st.session_state.selected_regulation
    # filters = None
    # if title_filter:
    #     from llama_index.core.vector_stores import MetadataFilter, MetadataFilters, FilterCondition
    #     filters = MetadataFilters(
    #         filters=[MetadataFilter(key="title", value=title_filter)],
    #         condition=FilterCondition.OR
    #     )

    chat_engine = st.session_state.chat_engine

    # On first turn only: reset memory to avoid preloaded junk
    if st.session_state.get("first_turn", False):
        chat_engine.reset_conversation()
        st.session_state.first_turn = False

    language, filters, custom_prompts = st.session_state.chat_session.process_question(
        user_input, chat_engine
    )
    response = chat_engine.chat(
        user_input, filters=filters, custom_prompts=custom_prompts
    )

    st.chat_message("assistant").write(response.response)
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": response.response})
