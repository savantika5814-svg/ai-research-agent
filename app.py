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

# --- Custom Styling (Pastel Cream & Pink Smudge Theme) ---
st.markdown(
    """
    <style>
    /* Main Pastel Cream Background & High-Contrast Dark Text */
    .stApp {
        background-color: #faf6ed;
        color: #2b2321;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #f2ece1;
        border-right: 1px solid #e7ded0;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] li, [data-testid="stSidebar"] label {
        color: #3d322e !important;
    }
    
    /* Headers & Titles */
    h1, h2, h3, h4, h5, h6 {
        color: #9d174d !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    
    /* General Text Readability */
    p, span, label, .stMarkdown, .streamlit-expanderHeader {
        color: #2b2321 !important;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        background-color: #ffffff;
        color: #2b2321;
        border: 1px solid #d4c5b9;
        border-radius: 8px;
    }
    
    /* Pink Buttons & Boxes with Dark-to-Light Pink Smudge Gradient */
    .stButton>button {
        background: linear-gradient(135deg, #be185d 0%, #db2777 50%, #f472b6 100%);
        color: #ffffff;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 20px;
        box-shadow: 0 4px 15px rgba(190, 24, 93, 0.25);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(190, 24, 93, 0.4);
        background: linear-gradient(135deg, #9d174d 0%, #be185d 50%, #ec4899 100%);
    }
    
    /* Report Output Card */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e7ded0;
        border-radius: 14px;
        padding: 24px;
        color: #2b2321;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        background: linear-gradient(135deg, #fbcfe8 0%, #f472b6 100%);
        color: #831843;
        border: 1px solid #f472b6;
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

        # 4. Render Output inside clean card
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
