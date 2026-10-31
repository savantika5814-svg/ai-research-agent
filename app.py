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
    page_title="Autonomous AI Research Agent", 
    page_icon="✨", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished, modern UI aesthetics
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
    </style>
""", unsafe_allow_html=True)

# Sidebar Design
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/artificial-intelligence.png", width=100)
    st.subheader("Agent Architecture")
    st.markdown("---")
    st.markdown("**Search Engine:** Tavily AI API")
    st.markdown("**Inference Engine:** Google Gemini 3.8 Flash")
    st.markdown("**Security:** Server-Side Encrypted Secrets")
    st.markdown("---")
    st.info("💡 **Tip:** Try searching for broad market trends, technical breakdowns, or industry forecasts!")

# Main Title Header
st.title("✨ Autonomous AI Research Agent")
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

# Input Field (prefills if quick button is clicked)
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
                    
                    # Styled output card container
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
