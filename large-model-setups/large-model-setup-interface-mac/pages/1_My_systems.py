import streamlit as st
import os
import json

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

st.markdown('<div class="page-title">My registered systems</div>', unsafe_allow_html=True)
st.set_page_config(page_title="My Systems", layout="wide")

st.divider()
SYSTEMS_DIR = "./system_profile"


def parse_criticality(text):
    if "1" in text or "Low" in text:
        return 1
    elif "2" in text or "Medium" in text:
        return 2
    elif "3" in text or "High" in text:
        return 3
    return 0

# Load registered systems from the folder
system_files = [f for f in os.listdir(SYSTEMS_DIR) if f.endswith(".json")]

if not system_files:
    st.info("No systems registered yet.")
else:
    header_cols = st.columns([3, 1, 5])
    with header_cols[0]:
        st.markdown("**Name**")
    with header_cols[1]:
        st.markdown("**AI / no AI**")
    with header_cols[2]:
        st.markdown("**Criticality**")


    for file_name in system_files:
        with open(os.path.join(SYSTEMS_DIR, file_name), "r") as f:
            data = json.load(f)

        name = data.get("system_name", file_name.replace(".json", ""))
        is_ai = data.get("ai_system", False)
        criticality = data.get("criticality", "Unknown")
        crit_number = parse_criticality(criticality)

        # Create layout for the addded systems
        with st.container():
            cols = st.columns([3, 1, 1, 4])
            with cols[0]:
                st.markdown(f"<div class='system-row col-name'>{name}</div>", unsafe_allow_html=True)
            with cols[1]:
                icon = "AI" if is_ai else "-"
                color = "green" if is_ai else "red"
                st.markdown(f"""<div class='system-row' style='color:{color}; font-size: 1.0rem; '>
                {icon}
                </div>
                """, unsafe_allow_html=True)
            with cols[2]:
                st.markdown(f"<div class='system-row'>{crit_number}</div>", unsafe_allow_html=True)
            with cols[3]:
                col_buttons = st.columns([1, 1, 1, 1])
                if col_buttons[0].button("Edit", key=f"edit_{file_name}"):
                    st.info(f"Edit {name} (not yet implemented)")
                if col_buttons[1].button("Delete", key=f"delete_{file_name}"):
                    os.remove(os.path.join(SYSTEMS_DIR, file_name))
                    st.success(f"Deleted {name}")
                    st.experimental_rerun()
                if col_buttons[2].button("More info", key=f"chat_{file_name}"):
                    st.info(f"Previous chats for {name} (not yet implemented)")




if st.button("➕", key="add", help="Add new system"):
    st.switch_page("pages/4_Add_system.py") 
