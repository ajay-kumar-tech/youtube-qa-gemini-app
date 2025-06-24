import streamlit as st
import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# --- Load environment variables ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("❌ GOOGLE_API_KEY not found in environment variables!")
    st.stop()

# --- Streamlit UI ---
st.title("🎥Paste YouTube Video Url Asked  Q&A using Gemini(ajay) 🔍")
# video_id = st.text_input("Enter YouTube Video ID (e.g., iNPuXUqVmkg):")
import re

video_url = st.text_input("Enter YouTube Video URL (e.g., https://www.youtube.com/watch?v=iNPuXUqVmkg):")

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

video_id = extract_video_id(video_url)

question = st.text_input("Ask a question about the video transcript:")

if video_id and question:
    try:
        # --- Step 1: Get transcript ---
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        transcript = " ".join(chunk["text"] for chunk in transcript_list)

        # --- Step 2: Split text ---
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.create_documents([transcript])

        # --- Step 3: Embedding + FAISS vector store ---
        embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = FAISS.from_documents(chunks, embedding)
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

        # --- Step 4: Prompt Template ---
        prompt = PromptTemplate(
            template="""
You are a helpful assistant.
Answer ONLY using the context from the video transcript.
If the context is insufficient, say "I don't know."

{context}
Question: {question}
""",
            input_variables=["context", "question"]
        )

        # --- Step 5: Retrieve relevant context ---
        retrieved_docs = retriever.invoke(question)
        context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
        prompt_input = prompt.format(context=context_text, question=question)

        # --- Step 6: Gemini LLM ---
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key
        )
        response = llm.invoke(prompt_input)

        # --- Step 7: Show Output ---
        st.subheader("📜 Answer:")
        st.write(response.content)

    except TranscriptsDisabled:
        st.error("❌ No captions available for this video.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")



#How to run
# conda activate base
# streamlit run app.py
