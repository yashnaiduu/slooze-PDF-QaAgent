import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import requests

API_URL = "http://localhost:8001"

st.set_page_config(page_title="PDF AI Assistant", layout="wide", page_icon="📄")

# --- Custom Default Streamlit Styling Fix ---
st.markdown("""
<style>
    /* Remove red hover from buttons */
    .stButton > button[kind="primary"]:hover {
        border-color: #AECBFA !important;
        background-color: #1B66C9 !important;
        color: white !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        border-color: #AECBFA !important;
        color: #1A73E8 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📄 PDF AI Assistant")
st.markdown("Upload a PDF in the sidebar, then ask questions about its content here.")

# --- Sidebar for Document Management ---
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
    
    # Clear Chat Button
    st.header("💬 Chat Controls")
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Main Chat Interface ---
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question about your PDF (Press Enter to send)..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(f"{API_URL}/query", json={"question": prompt})
                response.raise_for_status()
                data = response.json()
                answer = data.get("answer", "No answer found.")
                
                st.markdown(answer)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except requests.exceptions.RequestException as e:
                error_msg = f"Error querying document: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
