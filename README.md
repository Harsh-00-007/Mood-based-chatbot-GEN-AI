# 🚀 Enterprise AI Solutions Dashboard

A multi-tool, stateful web application built with **Python**, **Streamlit**, and **LangChain**. This application utilizes the **LLaMA 3.3 70B** model via the ultra-low latency **Groq API** inference engine to showcase two distinct AI architectures: deterministic data extraction and dynamic conversational memory.

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Framework:** Streamlit (Multi-tab UI & Session State)
* **LLM Orchestration:** LangChain (`langchain-groq`, `langchain-core`)
* **Data Validation:** Pydantic
* **Model:** LLaMA 3.3 70B Versatile
* **Environment Management:** `python-dotenv`

## 📊 Features & Architecture

### 1. B2B Mobile Inventory Extractor
An enterprise-grade tool that converts unstructured user queries into strict, database-ready JSON schemas.
* **Structured Outputs:** Leverages LangChain's `with_structured_output` and strict Pydantic schemas to enforce data shape and prevent hallucinations.
* **Deterministic Configuration:** Operates at `0.1` temperature to ensure high factual accuracy when extracting hardware specifications, pricing, and variants.
* **Fault Tolerance:** Built-in safeguards to return "N/A" for out-of-context data rather than generating false information.
* <img width="1915" height="962" alt="Screenshot 2026-06-21 095432" src="https://github.com/user-attachments/assets/3c3773f5-115b-45aa-a649-ba66335ec33e" />


### 2. Interactive Persona Chatbot
A dynamic conversational agent that alters its behavioral parameters seamlessly at runtime.
* **Dynamic Prompt Engineering:** Modifies the underlying LangChain `SystemMessage` based on user UI selection to dictate the LLM's personality constraints (Angry, Sad, Funny).
* **Stateful Memory:** Leverages Streamlit's `session_state` to maintain continuous chat history and contextual awareness across interface reruns.
* **Dynamic UI Rendering:** Automatically updates visual avatars and roles based on the active system prompt.
* <img width="1918" height="922" alt="Screenshot 2026-06-21 095455" src="https://github.com/user-attachments/assets/162bcb41-d8ff-4846-9a48-d1018ac12a00" />
