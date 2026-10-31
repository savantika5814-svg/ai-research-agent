import streamlit as st
from google import genai
from tavily import TavilyClient

# --- Page Config & Styling ---
st.set_page_config(
    page_title="VeritasAI - Autonomous Research Agent",
    page_icon="🔍",
    layout="wide",
)

st.sidebar.markdown("### VeritasAI")
st.sidebar.markdown(
    "Autonomous web research & intelligent report synthesis engine."
)

# --- API Keys Validation ---
try:
  gemini_api_key = st.secrets["GEMINI_API_KEY"].strip()
  tavily_api_key = st.secrets["TAVILY_API_KEY"].strip()
except Exception:
  st.error(
      "Missing API keys in Streamlit Secrets! Please add `GEMINI_API_KEY` and"
      " `TAVILY_API_KEY`."
  )
  st.stop()

# --- Initialize Clients ---
# Using the official Google GenAI SDK client initialized directly with the API key
gemini_client = genai.Client(api_key=gemini_api_key)
tavily_client = TavilyClient(api_key=tavily_api_key)

# --- Main UI layout ---
st.markdown("### Research Topic")
quick_topics = [
    "Solid-State EV Batteries",
    "DuckDB vs Polars Analytics",
    "AI Agents Enterprise 2026",
]

col1, col2, col3 = st.columns(3)
selected_topic = None

if col1.button("🔋 Solid-State EV Batteries"):
  selected_topic = "Solid-State EV Batteries"
if col2.button("📊 DuckDB vs Polars Analytics"):
  selected_topic = "DuckDB vs Polars Analytics"
if col3.button("🤖 AI Agents Enterprise 2026"):
  selected_topic = "Enterprise adoption trends for autonomous AI agents in 2026"

topic_input = st.text_input(
    "Research Topic Input",
    value=selected_topic
    or "Key performance differences between DuckDB and Polars for data analytics",
    label_visibility="collapsed",
)

if st.button("✨ Generate Research Report", type="primary"):
  if not topic_input:
    st.warning("Please enter a valid research topic.")
  else:
    with st.spinner("Executing Tavily web search and synthesizing report..."):
      try:
        # 1. Perform web search via Tavily
        search_result = tavily_client.search(
            query=topic_input, search_depth="advanced", max_results=5
        )
        sources = search_result.get("results", [])

        context_text = "\n\n".join(
            [f"Source: {s.get('url')}\nContent: {s.get('content')}" for s in sources]
        )

        # 2. Construct Prompt for Gemini
        prompt = f"""
        You are an expert research analyst. Using the web search context provided below, write a comprehensive, professional, well-structured research report addressing the topic: "{topic_input}".

        Web Search Context:
        {context_text}

        Structure the report cleanly with markdown headings, key takeaways, deep-dive analysis, and a conclusion. Cite sources appropriately.
        """

        # 3. Generate response using Gemini 2.5 Flash
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        # 4. Render Report
        st.markdown("---")
        st.markdown("## 📄 Research Report Output")
        st.markdown(response.text)

        with st.expander("🔍 View RAG Execution & Search Trace"):
          st.write(sources)

      except Exception as e:
        st.error(f"An error occurred: {e}")
