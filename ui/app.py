import streamlit as st
import requests

API_URL = "http://localhost:8001"

st.set_page_config(page_title="PDF AI Assistant", layout="centered")

st.title("PDF AI Assistant")
st.markdown("Upload a PDF to process it, then ask questions about its content.")

uploaded_file = st.file_uploader("PDF Upload", type=["pdf"])
if st.button("Process Document"):
    if uploaded_file is None:
        st.warning("Please upload a PDF file first.")
    else:
        with st.spinner("Processing document..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                response = requests.post(f"{API_URL}/upload", files=files)
                response.raise_for_status()
                data = response.json()
                st.success(f"{data.get('message', 'Document processed successfully.')}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error processing document: {e}")

st.divider()

question = st.text_input("Question Input", placeholder="What methodology was used?")

col1, col2 = st.columns([1, 5])
with col1:
    ask_clicked = st.button("Ask")

if ask_clicked:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Generating answer..."):
            try:
                response = requests.post(f"{API_URL}/query", json={"question": question})
                response.raise_for_status()
                data = response.json()
                
                st.subheader("Answer")
                st.write(data.get("answer", ""))
                
            except requests.exceptions.RequestException as e:
                st.error(f"Error querying document: {e}")
