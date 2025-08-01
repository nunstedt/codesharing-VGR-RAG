import streamlit as st

    # .info-icon {
    #     background-color: #ff9800;
    #     color: white;
    #     border-radius: 50%;
    #     width: 40px;
    #     height: 40px;
    #     display: flex;
    #     align-items: center;
    #     justify-content: center;
    #     margin: 0 auto 1rem auto;
    #     font-weight: bold;


st.markdown("""
    <style>
    [data-testid="stSidebarNav"] ul li:nth-child(5) {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)


# --- Custom CSS Styling ---
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

    /* Card container layout */
    .card-row {
        display: flex;
        justify-content: center;
        gap: 4rem;
        margin-bottom: 3rem;
    }

    /* Individual card */
    .card {
        background-color: #fafafa;
        border: 1px solid #eee;
        border-radius: 12px;
        padding: 1.5rem;
        width: 240px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: left;
        transition: all 0.2s ease;
    }

    .card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }

    .card-icon {
        font-size: 1.5rem;
        margin-bottom: 0.6rem;
    }

    .card-title {
        font-weight: 600;
        margin-bottom: 0.25rem;
    }

    .card-desc {
        font-size: 0.88rem;
        color: #555;
    }

    /* Info box styling */
    .info-box {
        background: rgba(255, 87, 34, 0.1);
        border-radius: 16px;
        padding: 2.5rem;
        max-width: 800px;
        margin: 0 auto;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .info-icon {
        color: #ff5722;
        font-size: 1.4rem;
        margin-bottom: 0.6rem;
    }

    .info-title {
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .info-text {
        color: #444;
        font-size: 0.95rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="page-title">VGR security compliance and regulation tool</div>', unsafe_allow_html=True)


st.set_page_config(page_title="VGR Compliance Tool", layout="wide")


# Cards row
st.markdown("""
<div class="card-row">
    <a href="/My_systems" target="_self" style="text-decoration: none; color: inherit;">
        <div class="card">
            <div class="card-icon">📁</div>
            <div class="card-title">My systems</div>
            <div class="card-desc">Manage your registered systems.</div>
        </div>
    </a>
    <a href="/Compliance_assistant" target="_self" style="text-decoration: none; color: inherit;">
        <div class="card">
            <div class="card-icon">📋</div>
            <div class="card-title">Compliance assistant</div>
            <div class="card-desc">Get system-specific guidance to structure your compliance tasks.</div>
        </div>
    </a>
    <a href="/Regulation_navigation" target="_self" style="text-decoration: none; color: inherit;">
        <div class="card">
            <div class="card-icon">📖</div>
            <div class="card-title">Regulation navigation</div>
            <div class="card-desc">Exlore relevant regulations and ask questions to learn more.</div>
        </div>
    </a>
</div>
""", unsafe_allow_html=True)

# Info box
st.markdown("""
<div class="info-box">
    <div class="info-icon">!</div>
    <div class="info-title">Important information about using the tool</div>
    <div class="info-text">
        This tool is powered by generative AI, enriched with specific regulations relevant to VGR's work on security and AI.
        Always validate recommendations with relevant policies and professional judgment.
    </div>
        <a href="/Regulation_navigation" target="_self">
        <button style="
            margin-top: 1rem;
            padding: 0.5rem 1rem;
            background-color: #fafafa;
            color: #444;
            border: none;
            border-radius: 6px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: background-color 0.2s ease;">
            Read more
        </button>
    </a>
</div>
""", unsafe_allow_html=True)