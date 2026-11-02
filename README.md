# 🌸 VeritasAI - Autonomous Research Agent

VeritasAI is an autonomous web research and intelligent report synthesis engine built with **Streamlit**, **Tavily AI**, and **OpenRouter**. It replaces restrictive cloud IAM bindings with a streamlined, universal API architecture to generate deep-dive, professionally cited research reports on any technical or market topic.

---

## 📊 System Architecture & Workflow

```mermaid
graph TD
    A[User Input / Quick Topic] -->|Trigger Research| B(Streamlit App UI)
    B -->|Query Parameters| C[Tavily AI Search API]
    C -->|Retrieved Web Sources & Context| D[OpenRouter LLM Engine]
    D -->|Synthesized Structured Report| E[Pastel Cream & Pink Card Output]
    E -->|Debug Trace & Links| F[Search Trace Expandable View]

## ✨ Key Features
-Autonomous Web Scraping & RAG: Leverages Tavily AI’s advanced search API to retrieve high-precision web sources and context snippets.

-Universal LLM Synthesis: Powered by OpenRouter’s free-tier routing, seamlessly generating comprehensive markdown reports complete with executive summaries, technical comparisons, and source citations.

-Interactive Quick Topics: One-click preset query buttons for instant analysis on emerging tech domains (e.g., Solid-State EV Batteries, DuckDB vs Polars, Enterprise AI Agents).

-Custom Aesthetic UI: Tailored with a cozy pastel cream background (#faf6ed), high-contrast typography, and dark-to-light pink smudge gradient buttons.

-Execution Trace Viewer: Expandable debug trace showing exact retrieved source URLs, titles, and content snippets used for synthesis

##🚀 Tech Stack
Frontend & UI: Streamlit

Search Engine: Tavily AI API (tavily-python)

Inference Engine: OpenRouter API (openai client-compatible wrapper)

##🔑 Free Tier Limits & Quotas
Tavily AI Search: Provides 1,000 free search queries per month (~33 deep-dive reports per day).

OpenRouter: Free models support 20 requests per minute and 50 full generations per day at zero cost.

##🛠️ Local Installation & Setup
1.Clone the Repository:git clone [https://github.com/savantika5814-svg/ai-research-agent.git](https://github.com/savantika5814-svg/ai-research-agent.git)
cd ai-research-agent
2.Install Dependencies:
Ensure you have Python installed, then install the required packages:pip install -r requirements.txt
Configure Secrets:
Create a .streamlit/secrets.toml file locally for development:OPENROUTER_API_KEY = "your-openrouter-api-key"
TAVILY_API_KEY = "your-tavily-api-key"
Run the App Locally:streamlit run app.py

##📦 Streamlit Cloud Deployment
1.Push your code and requirements.txt to your GitHub repository.

2.Link the repository to Streamlit Cloud.

3.In your Streamlit Cloud app dashboard, go to Settings -> Secrets and paste your production keys:
OPENROUTER_API_KEY = "sk-or-v1-..."
TAVILY_API_KEY = "tvly-..."

4.Save changes, and your agent will build and deploy instantly!
