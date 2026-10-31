🌸 VeritasAI | Autonomous Agentic Web Research Tool
VeritasAI is a production-grade, server-side secure autonomous research agent and Retrieval-Augmented Generation (RAG) web application. It orchestrates real-time web searches and synthesizes structured, citation-backed professional research reports on demand.

🌟 Key Features
Agentic Web Retrieval: Automatically queries the live web via the Tavily API to fetch high-relevance source documents and snippets.

Intelligent Synthesis: Leverages Google Gemini 3.8 Flash via REST API to distill raw web data into clean, structured, executive-ready research briefs.

Server-Side Security: Employs Streamlit Secrets (st.secrets) for encrypted environment variable management, protecting API credentials from client-side exposure.

Agent Observability Trace: Features an interactive audit trail expander that logs retriever latency, LLM inference times, and raw tool outputs for debugging and transparency.

Polished UI/UX: Custom-branded aesthetic featuring a warm cream palette, pastel pink accents, custom SVG iconography, and quick-topic selection chips.

🏗️ Architecture & Workflow
 [ User Input / Quick Topic ] 
              │
              ▼
    [ Streamlit Cloud UI ] ──(Secure Server-Side Proxy)
              │
              ├──► [ Tavily AI API ] ────► Retrieves Live Web Context
              │                                   │
              │                                   ▼
              └──► [ Google Gemini 3.8 Flash ] ───► Synthesizes Structured Report
                                                  │
                                                  ▼
                                     [ Interactive UI & Agent Trace ]
🛠️ Tech Stack
Frontend & Deployment: Streamlit Community Cloud (Python)

Search Engine: Tavily AI API (tavily-python)

Inference Engine: Google Gemini 3.8 Flash REST API (requests)

Styling: Custom HTML/CSS injection with responsive design principles

⚙️ Local Development & Setup
If you want to run or test this project locally, follow these steps:

Clone the repository:

Bash
git clone https://github.com/savantika5814-svg/ai-research-agent.git
cd ai-research-agent
Install dependencies:

Bash
pip install streamlit tavily-python requests python-dotenv
Set up your environment variables:
Create a .env file in the root directory:

Code snippet
GEMINI_API_KEY="your_google_gemini_api_key"
TAVILY_API_KEY="your_tavily_api_key"
Run the application:

Bash
streamlit run app.py
🚀 Live Demo
Access the live production deployment here: VeritasAI on Streamlit Cloud
