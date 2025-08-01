import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from system_user_profile import SystemProfile
from profile_manager import get_system_summary  # Adjust import path
import os

#Need to set this again since it is not runned through main
from llama_index.core import Settings
from LLM import get_llm  

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

st.markdown('<div class="page-title">Add new system</div>', unsafe_allow_html=True)
st.set_page_config(page_title="Add System", layout="wide")
Settings.llm = get_llm()

system_name = st.text_input("System name", key="system_name")
functionality = st.text_area("System functionality (What is it used for?)", key="functionality")

# Form for registration
users = st.multiselect(
    "Who are the primary users?",
    ["Internal staff at VGR", "Specialists", "Citizens", "External contractors", "Non-specified"], key="users"
)

data = st.multiselect(
    "What type of data does the system handle?",
    ["Personal data", "Health data", "Non-sensitive data", "Security classified data", "Mixed"], key="data"
)

environment = st.multiselect(
    "Hosting environment",
    ["On-premisse", "Cloud (public)", "Cloud (private)", "Hybrid", "Unknown"], key = "environment"
)

ai_system = st.checkbox("Is this an AI system?", key="ai_system")
if ai_system:
    ai_components = st.text_area("List AI components or models", key="ai_components")
else:
    ai_components = st.text_area("", key="ai_components")

accessability = st.multiselect(
    "System access",
    ["Internal network only", "Public internet", "VPN access", "Mobile device accessible", "Other"], key="accessability"
)

criticality = st.selectbox(
    "Criticality",
    [
        "Low – loss would have minor impact",
        "Medium – operational impact",
        "High – safety/life-critical or vital to operations"
    ],
    key="criticality"
)

if "description" not in st.session_state:
    st.session_state.description = None
if "profile" not in st.session_state:
    st.session_state.profile = None
    
submitted = st.button("Done, get summary")

# Generate the description
if submitted:
    profile = SystemProfile(
        system_name=st.session_state.system_name,
        functionality=st.session_state.functionality,
        users=st.session_state.users,
        data=st.session_state.data,
        environment=st.session_state.environment,
        ai_system=st.session_state.ai_system,
        ai_components=st.session_state.ai_components,
        accessability=st.session_state.accessability,
        criticality=st.session_state.criticality
    )

    with st.spinner("Generating summary..."):
        summary = get_system_summary(profile.format_for_prompt())

    st.session_state.profile = profile
    st.session_state.description = summary
    st.rerun()

if st.session_state.description:
    st.markdown("### Assistant-generated system description:")
    st.success(st.session_state.description)

    confirm = st.button("Confirm and save system")
    redo = st.button("Edit and regererate")

    #Confirm by user to save
    if confirm:

        st.session_state.profile.save_system_to_file(summary=st.session_state.description)
        st.success(f"System '{st.session_state.profile.system_name}' has been saved successfully.")
        for key in [
            "system_name", "functionality", "users", "data", "environment", 
            "ai_system", "ai_components", "accessability", "criticality",
            "description", "profile"
        ]:
        
            st.session_state.pop(key, None)
    elif redo:
        st.rerun()