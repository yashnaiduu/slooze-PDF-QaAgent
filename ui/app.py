import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import requests
from ui.styles import load_css

API_URL = "http://localhost:8001"

st.set_page_config(page_title="PDF AI Assistant", layout="wide", page_icon="📄")

st.markdown(load_css(), unsafe_allow_html=True)

st.markdown('<div class="agent-header">📄 PDF AI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="agent-subtitle">Extract insights and ask questions about your documents</div>', unsafe_allow_html=True)


with st.sidebar:
    st.header("📂 Document Upload")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")
    
    if st.button("Process Document", use_container_width=True, type="primary"):
        if uploaded_file is None:
            st.warning("Please upload a PDF file first.")
        else:
            with st.spinner("Processing document..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    response = requests.post(f"{API_URL}/upload", files=files)
                    response.raise_for_status()
                    data = response.json()
                    st.success(f"✅ {data.get('message', 'Document processed successfully.')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Error processing document: {e}")
    
    st.divider()

    st.header("💬 Chat Controls")
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your PDF (Press Enter to send)..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(f"{API_URL}/query", json={"question": prompt})
                response.raise_for_status()
                data = response.json()
                answer = data.get("answer", "No answer found.")
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except requests.exceptions.RequestException as e:
                error_msg = f"Error querying document: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
