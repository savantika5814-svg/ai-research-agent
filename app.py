import streamlit as st
import os
import requests

# Import Tavily cleanly
try:
    from tavily import TavilyClient
except ImportError:
    from tavily import Client as TavilyClient

# Streamlit Page Setup
st.set_page_config(
    page_title="SynthetiSeek | Autonomous AI Research Agent", 
    page_icon="🧠", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput input {
        border-radius: 10px;
        padding: 12px;
        border: 1px solid #30363d;
        background-color: #161b22;
        color: #c9d1d9;
    }
    .stButton button {
        border-radius: 10px;
        font-weight: 600;
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        padding: 0.6rem 1rem;
        transition: opacity 0.2s ease;
    }
    .stButton button:hover {
        opacity: 0.9;
    }
    .report-container {
        background-color: #161b22;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #30363d;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .logo-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 0.5rem;
    }
    .logo-header h1 {
        margin: 0;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Design
with st.sidebar:
    # Sidebar SVG Logo
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <svg width="70" height="70" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="45" cy="45" r="32" stroke="#60A5FA" stroke-width="6"/>
            <path d="M68 68L88 88" stroke="#A855F7" stroke-width="8" stroke-linecap="round"/>
            <circle cx="35" cy="40" r="4" fill="#60A5FA"/>
            <circle cx="55" cy="40" r="4" fill="#60A5FA"/>
            <circle cx="45" cy="55" r="4" fill="#A855F7"/>
            <path d="M35 40L45 55L55 40" stroke="#60A5FA" stroke-width="2"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)
    st.subheader("Agent Architecture")
    st.markdown("---")
    st.markdown("**Search Engine:** Tavily AI API")
    st.markdown("**Inference Engine:** Google Gemini 3.8 Flash")
    st.markdown("**Security:** Server-Side Encrypted Secrets")
    st.markdown("---")
    st.info("💡 **Tip:** Try searching for broad market trends, technical breakdowns, or industry forecasts!")

# Main Title Header with Logo
st.markdown("""
<div class="logo-header">
    <svg width="60" height="60" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="45" cy="45" r="32" stroke="#60A5FA" stroke-width="6"/>
        <path d="M68 68L88 88" stroke="#A855F7" stroke-width="8" stroke-linecap="round"/>
        <circle cx="35" cy="40" r="4" fill="#60A5FA"/>
        <circle cx="55" cy="40" r="4" fill="#60A5FA"/>
        <circle cx="45" cy="55" r="4" fill="#A855F7"/>
        <path d="M35 40L45 55L55 40" stroke="#60A5FA" stroke-width="2"/>
    </svg>
    <h1>SynthetiSeek</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("Instantly orchestrate web searches and generate structured, citation-backed professional research reports.")
st.markdown("")

# Securely load API keys from Streamlit Cloud Secrets (Server-side)
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Quick suggestion chips
st.markdown("##### Quick Topics:")
col1, col2, col3 = st.columns(3)
selected_quick_topic = ""

with col1:
    if st.button("🔋 Solid-State EV Batteries"):
        selected_quick_topic = "Latest developments in solid-state EV batteries"
with col2:
    if st.button("📊 DuckDB vs Polars Analytics"):
        selected_quick_topic = "Key performance differences between DuckDB and Polars for data analytics"
with col3:
    if st.button("🤖 AI Agents Enterprise 2026"):
        selected_quick_topic = "Enterprise adoption trends for autonomous AI agents in 2026"

# Input Field
topic = st.text_input(
    "Research Topic", 
    value=selected_quick_topic,
    placeholder="e.g., Global market trends in renewable energy..."
)

st.markdown("")

def search_web(query: str) -> str:
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    response = tavily_client.search(query=query, max_results=4)
    formatted_results = []
    for result in response.get("results", []):
        formatted_results.append(
            f"Title: {result['title']}\nURL: {result['url']}\nContent: {result['content']}\n"
        )
    return "\n".join(formatted_results)

if st.button("🚀 Generate Comprehensive Report", type="primary"):
    if not topic.strip():
        st.warning("Please enter or select a research topic first.")
    elif not GEMINI_API_KEY or not TAVILY_API_KEY:
        st.error("Server API keys are not configured properly.")
    else:
        with st.spinner("🔍 Executing Tavily web search & synthesizing via Gemini 3.8 Flash..."):
            try:
                # 1. Search Tavily
                search_context = search_web(topic)
                
                # 2. Call Gemini API securely on the server
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GEMINI_API_KEY}"
                prompt_text = (
                    "You are an expert research assistant and professional technical writer.\n"
                    "Synthesize the provided search results into a clear, structured 1-page research report.\n"
                    "Always cite source URLs directly in the text or in a References section at the bottom.\n\n"
                    f"TOPIC TO RESEARCH: {topic}\n\n"
                    f"SEARCH RESULTS & DATA:\n{search_context}"
                )
                payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
                headers = {"Content-Type": "application/json"}
                
                res = requests.post(url, headers=headers, json=payload)
                res_data = res.json()
                
                if "candidates" in res_data:
                    report = res_data["candidates"][0]["content"]["parts"][0]["text"]
                    st.success("✅ Research Report Generated Successfully!")
                    
                    st.markdown("---")
                    st.markdown(f"""
                        <div class="report-container">
                            {report}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"API Error: {res_data}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
