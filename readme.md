# 🎭 Mood-Based AI Chatbot

A dynamic, stateful conversational agent built with **Python**, **Streamlit**, and **LangChain**. This application utilizes the **LLaMA 3.3 70B** model via the **Groq API** to deliver high-speed inference while seamlessly switching between distinct AI personas (Angry, Sad, Funny) using engineered system prompts.

## 🚀 Features

* **Dynamic Prompt Engineering:** Modifies the underlying System Messages at runtime to dictate the LLM's personality and constraints.
* **Stateful Memory:** Leverages Streamlit's `session_state` to maintain continuous chat history and context across UI reruns.
* **High-Speed Inference:** Powered by the Groq LPU inference engine for near-instantaneous text generation.
* **Modern UI:** Clean, responsive chat interface built natively with Streamlit components.

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Framework:** Streamlit
* **LLM Orchestration:** LangChain (`langchain-groq`, `langchain-core`)
* **Model:** LLaMA 3.3 70B Versatile
* **Environment Management:** `python-dotenv`
