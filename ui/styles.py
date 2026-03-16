def load_css():
    return """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Outfit:wght@400;600;700&display=swap');

    /* Variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        --surface-color: #f8fafc;
        --text-main: #1e293b;
        --text-muted: #64748b;
    }

    /* Global reset for Streamlit */
    .main {
        background-color: var(--surface-color);
        font-family: 'Inter', sans-serif;
    }

    /* Page Header */
    .agent-header {
        font-family: 'Outfit', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .agent-subtitle {
        color: var(--text-muted);
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }

    /* Chat Elements */
    .stChatMessage {
        border-radius: 12px !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1) !important;
    }
    
    /* Source Tags */
    .source-tag {
        display: inline-block;
        padding: 4px 12px;
        margin: 4px;
        border-radius: 20px;
        background: #f1f5f9;
        color: #475569;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid #e2e8f0;
        text-decoration: none !important;
        transition: background 0.2s;
    }
    .source-tag:hover {
        background: #e2e8f0;
    }
    </style>
    """
