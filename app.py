import os
import logging
import streamlit as st

from loaders.file_loader import load_file
from embed.embed_store import embed_and_store
from qa.qa_pipeline import answer_question
from logger import setup_logger

os.makedirs("temp_files", exist_ok=True)

setup_logger()
logging.info("🚀 Application started")

st.set_page_config(page_title="Document Q&A GenAI", layout="wide")
st.title("📄 Ask Questions from Your Document using Gemini AI")

uploaded_file = st.file_uploader(
    "Upload your PDF, scanned PDF, image, or TXT file", 
    type=["pdf", "txt", "jpg", "jpeg", "png"],
)

if uploaded_file:
    file_path = f"temp_files/{uploaded_file.name}"

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    logging.info(f"📁 File uploaded: {uploaded_file.name}")
    st.success("✅ File uploaded successfully.")

    force_ocr = st.checkbox("Force OCR (for scanned PDFs/images)?", value=False)

    if st.button("📤 Extract & Embed"):
        with st.spinner("Extracting text and embedding into Pinecone..."):
            try:
                text = load_file(file_path, force_ocr=force_ocr)
                logging.info(
                    f"📄 Extracted text length = {len(text)} characters from {uploaded_file.name}"
                )

                embed_result = embed_and_store(text, namespace=uploaded_file.name)
                logging.info(embed_result)

                st.success(embed_result)
            except Exception as e:
                logging.error(f"❌ Extract/Embed failed: {str(e)}")
                st.error(f"Extraction or embedding failed: {e}")


st.subheader("Ask a question about your uploaded file")
question = st.text_input("❓ Your Question", key="question_input")

if st.button("Get Answer", key="answer_btn"):
    if not uploaded_file:
        st.warning("Please upload and embed a file first.")
    elif not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving answer from Gemini…"):
            try:
                logging.info(f"❓ Question asked: {question}")
                answer = answer_question(question, namespace=uploaded_file.name)
                st.markdown("### 💬 Gemini's Answer")
                st.info(answer)
                logging.info(f"🤖 Answer: {answer[:120]}…")
            except Exception as e:
                logging.error(f"❌ Answer generation failed: {str(e)}")
                st.error(f"Answer generation failed: {e}")
