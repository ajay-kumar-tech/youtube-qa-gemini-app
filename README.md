# 🎥 YouTube Q&A App using Gemini 1.5 Flash

This is a Streamlit-based web application that allows you to ask questions about the content of any YouTube video using its transcript. It uses **Google Gemini 1.5 Flash** as the LLM and extracts video transcripts using the `youtube-transcript-api`.

---

## 🚀 Features

- 🔍 **Extracts transcript** from any YouTube video (if captions are available)
- 🤖 Uses **LangChain + Gemini 1.5 Flash** for intelligent question-answering
- 🧠 Embeds transcript using **HuggingFace embeddings** + **FAISS vector store**
- 📚 Provides contextual answers by retrieving the most relevant transcript parts
- 🌐 Built with **Streamlit** – clean, responsive, and interactive UI

---

## 🧰 Tech Stack

| Component             | Tool/Service                        |
|----------------------|-------------------------------------|
| Frontend UI          | Streamlit                           |
| Transcript Fetching  | youtube-transcript-api              |
| Text Splitting       | LangChain RecursiveCharacterTextSplitter |
| Embeddings           | HuggingFace Transformers (`MiniLM`) |
| Vector Search        | FAISS                               |
| Language Model       | Google Gemini 1.5 Flash             |
| LLM Framework        | LangChain                           |
| Environment Vars     | python-dotenv                       |


---

## 🔧 Install dependencies
```pip install -r requirements.txt
---

### 1. Clone the repo:
```bash
git clone https://github.com/your-username/youtube-qa-gemini-app.git
cd youtube-qa-gemini-app

---
