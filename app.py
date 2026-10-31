import streamlit as st
import os
import requests

# Import Tavily cleanly
try:
    from tavily import TavilyClient
except ImportError:
    from tavily import Client as TavilyClient

# Streamlit Page Setup
st.set_page_config(page_title="Autonomous AI Research Agent", page_icon="🔍", layout="wide")

st.title("🤖 Autonomous AI & Web Research Agent")
st.write("Enter any topic below to run an automated web search and generate a synthesized research report.")

# Securely load API keys from Streamlit Cloud Secrets (Server-side)
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]
except Exception:
    # Fallback for local testing if running via python
    from dotenv import load_dotenv
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Input Field
topic = st.text_input("Research Topic", placeholder="e.g., Latest developments in solid-state EV batteries")

def search_web(query: str) -> str:
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    response = tavily_client.search(query=query, max_results=4)
    formatted_results = []
    for result in response.get("results", []):
        formatted_results.append(
            f"Title: {result['title']}\nURL: {result['url']}\nContent: {result['content']}\n"
        )
    return "\n".join(formatted_results)

if st.button("Generate Research Report", type="primary"):
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    elif not GEMINI_API_KEY or not TAVILY_API_KEY:
        st.error("Server API keys are not configured properly.")
    else:
        with st.spinner("🔍 Searching the web and generating report via Gemini 3.8 Flash..."):
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
                    st.success("Report Generated Successfully!")
                    
                    st.markdown("---")
                    st.markdown(report)
                else:
                    st.error(f"API Error: {res_data}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
