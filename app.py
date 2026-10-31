import streamlit as st
import os
import requests
import time

# Import Tavily cleanly
try:
    from tavily import TavilyClient
except ImportError:
    from tavily import Client as TavilyClient

# Streamlit Page Setup
st.set_page_config(
    page_title="VeritasAI | Autonomous Research Agent", 
    page_icon="🤝", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for Warm Cream & Pastel Pink Theme with High-Contrast Text
st.markdown("""
    <style>
    /* Main Background - Warm Champagne / Cream */
    .stApp {
        background-color: #FAF8F5;
        color: #374151;
    }
    
    /* Sidebar Styling - Soft Rose Tint with Dark Readable Text */
    section[data-testid="stSidebar"] {
        background-color: #FDE2E8 !important;
        border-right: 1px solid #FBCFE8;
    }
    section[data-testid="stSidebar"] * {
        color: #4A044E !important;
    }
    
    /* Inputs */
    .stTextInput input {
        border-radius: 12px;
        padding: 12px;
        border: 1.5px solid #FBCFE8;
        background-color: #FFFFFF;
        color: #374151;
    }
    .stTextInput input:focus {
        border-color: #EC4899;
        box-shadow: 0 0 0 2px rgba(236, 72, 153, 0.2);
    }
    
    /* Action Button */
    .stButton button {
        border-radius: 12px;
        font-weight: 600;
        width: 100%;
        background: linear-gradient(135deg, #EC4899 0%, #F43F5E 100%);
        color: white;
        border: none;
        padding: 0.65rem 1rem;
        box-shadow: 0 4px 10px rgba(236, 72, 153, 0.25);
        transition: transform 0.15s ease, opacity 0.2s ease;
    }
    .stButton button:hover {
        opacity: 0.92;
        transform: translateY(-1px);
        color: white;
    }
    
    /* Report Output Container */
    .report-container {
        background-color: #FFFFFF;
        padding: 2.2rem;
        border-radius: 16px;
        border: 1px solid #FBCFE8;
        box-shadow: 0 10px 25px rgba(236, 72, 153, 0.08);
        color: #1F2937;
        line-height: 1.7;
    }
    
    /* Header Layout */
    .logo-header {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 0.2rem;
    }
    .logo-header h1 {
        margin: 0;
        font-size: 2.6rem;
        font-weight: 800;
        color: #831843;
        letter-spacing: -0.5px;
    }
    
    /* Secondary text */
    .sub-text {
        color: #6B7280;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Design with Helping Hand Logo
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 15px; margin-top: 10px;">
        <svg width="75" height="75" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="42" fill="#FFFFFF" stroke="#EC4899" stroke-width="3"/>
            <!-- Helping Hand / Cradling Support Icon -->
            <path d="M30 60C30 60 38 72 50 72C62 72 70 60 70 60" stroke="#DB2777" stroke-width="5" stroke-linecap="round"/>
            <path d="M38 52L45 59L65 38" stroke="#DB2777" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
            <!-- Spark / Guidance Node -->
            <circle cx="65" cy="30" r="5" fill="#EC4899"/>
        </svg>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #831843;'>VeritasAI</h3>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Search Engine:** Tavily AI API")
    st.markdown("**Inference Engine:** Google Gemini 3.8 Flash")
    st.markdown("**Security:** Server-Side Encrypted Secrets")
    st.markdown("---")
    st.info("💡 **Tip:** Ask broad market analysis, technical comparisons, or industry trends.")

# Main Title Header with Helping Hand Logo
st.markdown("""
<div class="logo-header">
    <svg width="60" height="60" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="50" cy="50" r="42" fill="#FFFFFF" stroke="#EC4899" stroke-width="3"/>
        <!-- Helping Hand / Cradling Support Icon -->
        <path d="M30 60C30 60 38 72 50 72C62 72 70 60 70 60" stroke="#DB2777" stroke-width="5" stroke-linecap="round"/>
        <path d="M38 52L45 59L65 38" stroke="#DB2777" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
        <!-- Spark / Guidance Node -->
        <circle cx="65" cy="30" r="5" fill="#EC4899"/>
    </svg>
    <h1>VeritasAI</h1>
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="sub-text">Autonomous web research & intelligent report synthesis engine.</p>', unsafe_allow_html=True)

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

def search_web(query: str) -> tuple[str, float]:
    start_time = time.time()
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    response = tavily_client.search(query=query, max_results=4)
    elapsed_time = round(time.time() - start_time, 2)
    
    formatted_results = []
    for result in response.get("results", []):
        formatted_results.append(
            f"Title: {result['title']}\nURL: {result['url']}\nContent: {result['content']}\n"
        )
    return "\n".join(formatted_results), elapsed_time

if st.button("✨ Generate Research Report", type="primary"):
    if not topic.strip():
        st.warning("Please enter or select a research topic first.")
    elif not GEMINI_API_KEY or not TAVILY_API_KEY:
        st.error("Server API keys are not configured properly.")
    else:
        with st.spinner("🤝 Searching the web & synthesizing report via Gemini 3.8 Flash..."):
            try:
                # 1. Search Tavily
                search_context, tavily_latency = search_web(topic)
                
                # 2. Call Gemini API securely on the server
                start_llm_time = time.time()
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
                llm_latency = round(time.time() - start_llm_time, 2)
                res_data = res.json()
                
                if "candidates" in res_data:
                    report = res_data["candidates"][0]["content"]["parts"][0]["text"]
                    st.success("✅ Research Report Generated Successfully!")
                    
                    # 🛠️ TECHNICAL AGENT EXECUTION TRACE EXPANDER
                    with st.expander("🔍 Technical Agent Execution Trace & RAG Metadata"):
                        st.markdown(f"**Query Intent:** `{topic}`")
                        st.markdown(f"**Web Search Retrieval Latency:** `{tavily_latency} seconds` (Tavily AI)")
                        st.markdown(f"**LLM Synthesis Latency:** `{llm_latency} seconds` (Google Gemini 3.8 Flash)")
                        st.markdown("**Retrieved Context Snippets (Tool Output):**")
                        st.code(search_context, language="text")
                    
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
