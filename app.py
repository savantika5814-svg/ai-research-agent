import streamlit as st
from openai import OpenAI
from tavily import TavilyClient

# --- Page Config ---
st.set_page_config(
    page_title="VeritasAI - Research Agent",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom Styling & Theme Override ---
st.markdown(
    """
    <style>
    /* Main Background & Fonts */
    .stApp {
        background-color: #0d0f12;
        color: #e2e8f0;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161a22;
        border-right: 1px solid #2d3748;
    }
    
    /* Headers & Title Styling */
    h1, h2, h3 {
        color: #f472b6 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom Card Containers */
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 20px;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 8px 16px;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        background-color: #1e293b;
        color: #f8fafc;
        border: 1px solid #475569;
        border-radius: 8px;
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        background-color: rgba(236, 72, 153, 0.15);
        color: #f472b6;
        border: 1px solid rgba(236, 72, 153, 0.3);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- Sidebar ---
with st.sidebar:
  st.markdown("# 🌸 VeritasAI")
  st.markdown(
      "<span class='status-badge'>System Active</span>", unsafe_allow_html=True
  )
  st.markdown("---")
  st.markdown(
      "**Autonomous web research & intelligent report synthesis engine.**"
  )
  st.markdown("<br>", unsafe_allow_html=True)

  st.markdown("#### Engine Configuration")
  st.markdown("• **Search Engine**: Tavily AI API")
  st.markdown("• **Inference Engine**: OpenRouter Free Tier")
  st.markdown("• **Security**: Server-Side Encrypted Secrets")

  st.markdown("---")
  st.info(
      "💡 **Tip**: Ask about emerging tech trends, competitive benchmarks, or"
      " complex technical comparisons."
  )

# --- API Keys Validation ---
try:
  openrouter_api_key = st.secrets["OPENROUTER_API_KEY"].strip()
  tavily_api_key = st.secrets["TAVILY_API_KEY"].strip()
except Exception:
  st.error(
      "⚠️ Missing API keys in Streamlit Secrets! Please verify"
      " `OPENROUTER_API_KEY` and `TAVILY_API_KEY` are present."
  )
  st.stop()

# --- Initialize Clients ---
llm_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key,
)
tavily_client = TavilyClient(api_key=tavily_api_key)

# --- Main UI ---
st.title("Research Topic")

# Quick Selection Buttons
col1, col2, col3 = st.columns(3)
selected_topic = ""

if col1.button("🔋 Solid-State EV Batteries", use_container_width=True):
  selected_topic = "Solid-State EV Batteries"
if col2.button("📊 DuckDB vs Polars Analytics", use_container_width=True):
  selected_topic = "DuckDB vs Polars Analytics"
if col3.button("🤖 AI Agents Enterprise 2026", use_container_width=True):
  selected_topic = (
      "Enterprise adoption trends for autonomous AI agents in 2026"
  )

# Input Box
topic_input = st.text_input(
    "Research Topic Input",
    value=selected_topic
    or "Key performance differences between DuckDB and Polars for data analytics",
    placeholder="Type any market research or technical analysis topic...",
    label_visibility="collapsed",
)

st.markdown("<br>", unsafe_allow_html=True)

# Generate Action
if st.button("✨ Generate Research Report", type="primary"):
  if not topic_input:
    st.warning("Please enter a research topic first.")
  else:
    with st.spinner("Searching the web & synthesizing full report..."):
      try:
        # 1. Tavily Search
        search_result = tavily_client.search(
            query=topic_input, search_depth="advanced", max_results=5
        )
        sources = search_result.get("results", [])

        context_text = "\n\n".join([
            f"Source URL: {s.get('url')}\nContent: {s.get('content')}"
            for s in sources
        ])

        # 2. OpenRouter Prompt
        prompt = f"""
        You are an elite enterprise research analyst. Synthesize the provided web search context into a highly structured, thorough, and professional research report on the topic: "{topic_input}".

        Web Search Context:
        {context_text}

        Requirements:
        - Executive Summary & Key Takeaways
        - In-Depth Technical & Market Analysis
        - Pros, Cons, or Trade-off Comparisons (if applicable)
        - Future Outlook & Conclusion
        - Explicitly cite source URLs where appropriate.
        """

        # 3. OpenRouter API Call
        response = llm_client.chat.completions.create(
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}],
        )

        report_content = response.choices[0].message.content

        # 4. Render Output
        st.markdown("---")
        st.markdown("## 📄 Research Report Output")
        st.markdown(
            f"<div class='metric-card'>{report_content}</div>",
            unsafe_allow_html=True,
        )

        # 5. Search Trace Expandable Block
        with st.expander("🔍 View RAG Execution & Search Trace"):
          st.write("### Retrived Web Context Sources:")
          for idx, source in enumerate(sources, 1):
            st.markdown(f"**{idx}. [{source.get('title')}]({source.get('url')})**")
            st.caption(source.get("content"))
            st.markdown("---")

      except Exception as e:
        st.error(f"Execution Error: {e}")
