"""
BearDiary AI - Teddy Plaid Design System 🐻🎀
Cozy pink + brown + cream aesthetic with plaid vibes
"""

import streamlit as st
import base64
from pathlib import Path

# ============================================
# 🎨 COLOR PALETTE
# ============================================
COLORS = {
    "cream": "#FDF2F0",
    "blush": "#F5E1DC",
    "soft_pink": "#E8A0BF",
    "dusty_rose": "#D4869C",
    "warm_brown": "#A0522D",
    "cocoa": "#8B6914",
    "deep_brown": "#5C3A21",
    "chocolate": "#4A2C17",
    "ink_brown": "#3E2118",
    "sage_accent": "#B8C4A0",
}

# ============================================
# 🖼️ IMAGE HELPER
# ============================================
def get_base64_image(image_path: str) -> str:
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return ""


def get_plaid_bg() -> str:
    plaid_path = Path(__file__).parent.parent / "assets" / "plaid-bg.jpg"
    return get_base64_image(str(plaid_path))


# ============================================
# 🎀 MAIN CSS INJECTION
# ============================================
def inject_base_styles():
    """Inject the base Teddy Plaid styles into every page"""
    
    plaid_b64 = get_plaid_bg()
    plaid_bg = f"url('data:image/jpeg;base64,{plaid_b64}')" if plaid_b64 else "none"
    
    st.markdown(f"""
    <style>
    /* ============================================
       🌸 GOOGLE FONTS
    ============================================ */
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700;9..144,900&family=Quicksand:wght@400;500;600;700&family=Caveat:wght@400;600;700&display=swap');

    /* ============================================
       🎨 CSS VARIABLES
    ============================================ */
    :root {{
        --cream: {COLORS['cream']};
        --blush: {COLORS['blush']};
        --soft-pink: {COLORS['soft_pink']};
        --dusty-rose: {COLORS['dusty_rose']};
        --warm-brown: {COLORS['warm_brown']};
        --cocoa: {COLORS['cocoa']};
        --deep-brown: {COLORS['deep_brown']};
        --chocolate: {COLORS['chocolate']};
        --ink-brown: {COLORS['ink_brown']};
        --sage: {COLORS['sage_accent']};
        
        --font-serif: 'Fraunces', serif;
        --font-body: 'Quicksand', sans-serif;
        --font-handwritten: 'Caveat', cursive;
    }}

    /* ============================================
       🌍 GLOBAL RESETS + BASE
    ============================================ */
    html, body, [class*="css"] {{
        font-family: var(--font-body);
        color: var(--ink-brown);
    }}

    .stApp {{
        background: 
            linear-gradient(180deg, 
                rgba(245, 225, 220, 0.82) 0%, 
                rgba(232, 200, 195, 0.78) 100%),
            {plaid_bg};
        background-size: 350px 350px;
        background-attachment: fixed;
    }}

    /* Hide Streamlit defaults BUT KEEP sidebar toggle! */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display: none;}}

    /* 🔑 KEEP the header transparent but visible so sidebar toggle works */
    header {{
        background: transparent !important;
    }}

    /* Make sidebar toggle button ADORABLE and always visible! */
    [data-testid="stSidebarCollapsedControl"] {{
        background: linear-gradient(135deg, #E8A0BF, #D4869C) !important;
        border: 2px solid #3E2118 !important;
        border-radius: 12px !important;
        box-shadow: 3px 3px 0 #3E2118 !important;
        padding: 4px !important;
        margin: 10px !important;
        transition: all 0.2s ease !important;
    }}

    [data-testid="stSidebarCollapsedControl"]:hover {{
        transform: translate(-2px, -2px);
        box-shadow: 5px 5px 0 #3E2118 !important;
    }}

    [data-testid="stSidebarCollapsedControl"] button svg {{
        color: white !important;
        stroke: white !important;
    }}

    /* Sidebar close button styling too */
    [data-testid="stSidebarHeader"] button {{
        color: #3E2118 !important;
    }}

    /* ============================================
       ✍️ TYPOGRAPHY — BIGGER + DARKER
    ============================================ */
    h1, h2, h3, h4, h5, h6 {{
        font-family: var(--font-serif) !important;
        color: var(--ink-brown) !important;
        letter-spacing: -0.02em;
        font-weight: 700 !important;
    }}

    h1 {{
        font-weight: 900 !important;
        font-size: 3.2rem !important;
    }}

    h2 {{ font-size: 2.3rem !important; }}
    h3 {{ font-size: 1.7rem !important; }}
    h4 {{ font-size: 1.35rem !important; }}

    p, span, div, label, li {{
        font-family: var(--font-body);
        color: var(--ink-brown);
        font-size: 1.05rem;
    }}

    .stMarkdown p {{
        font-size: 1.1rem !important;
        color: var(--ink-brown) !important;
        line-height: 1.7;
    }}

    /* ============================================
       🎀 STREAMLIT BUTTONS — BIGGER + BOLDER
    ============================================ */
    .stButton > button {{
        background: linear-gradient(135deg, var(--soft-pink), var(--dusty-rose)) !important;
        color: white !important;
        border: 2.5px solid var(--ink-brown) !important;
        border-radius: 20px !important;
        padding: 0.8rem 2rem !important;
        font-family: var(--font-body) !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 4px 4px 0 var(--ink-brown) !important;
    }}

    .stButton > button:hover {{
        transform: translate(-2px, -2px) !important;
        box-shadow: 6px 6px 0 var(--ink-brown) !important;
        background: linear-gradient(135deg, var(--dusty-rose), var(--soft-pink)) !important;
    }}

    .stButton > button:active {{
        transform: translate(1px, 1px) !important;
        box-shadow: 2px 2px 0 var(--ink-brown) !important;
    }}

    /* ============================================
       📝 TEXT INPUTS + TEXTAREAS — BIGGER
    ============================================ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        background: var(--cream) !important;
        border: 2.5px solid var(--dusty-rose) !important;
        border-radius: 15px !important;
        color: var(--ink-brown) !important;
        font-family: var(--font-body) !important;
        font-size: 1.1rem !important;
        padding: 1rem !important;
        line-height: 1.6 !important;
    }}

    .stTextArea > div > div > textarea {{
        font-family: 'Caveat', cursive !important;
        font-size: 1.5rem !important;
        line-height: 1.5 !important;
    }}

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: var(--warm-brown) !important;
        box-shadow: 0 0 0 3px rgba(232, 160, 191, 0.3) !important;
    }}

    /* ============================================
       🐻 CUSTOM COMPONENT CLASSES
    ============================================ */
    
    /* Cozy Card — with cute decorative corner */
    .cozy-card {{
        background: rgba(253, 242, 240, 0.97);
        border: 2.5px solid var(--ink-brown);
        border-radius: 22px;
        padding: 2rem;
        box-shadow: 5px 5px 0 var(--ink-brown);
        margin: 1rem 0;
        position: relative;
    }}

    /* Cute corner sticker — floating bow */
    .cozy-card::before {{
        content: "🎀";
        position: absolute;
        top: -18px;
        left: 20px;
        font-size: 1.8rem;
        background: var(--cream);
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2.5px solid var(--ink-brown);
        box-shadow: 2px 2px 0 var(--ink-brown);
    }}

    /* Card variant WITHOUT the corner sticker */
    .cozy-card-plain {{
        background: rgba(253, 242, 240, 0.97);
        border: 2.5px solid var(--ink-brown);
        border-radius: 22px;
        padding: 2rem;
        box-shadow: 5px 5px 0 var(--ink-brown);
        margin: 1rem 0;
    }}

    /* Handwritten accent text — BIGGER */
    .handwritten {{
        font-family: var(--font-handwritten);
        font-size: 1.8rem;
        color: var(--warm-brown);
    }}

    /* Cute signature */
    .signature {{
        text-align: center;
        font-family: var(--font-handwritten);
        font-size: 1.5rem;
        color: var(--warm-brown);
        margin-top: 3rem;
        padding: 1rem;
        opacity: 0.85;
    }}

    /* Mood badge — bigger + bolder */
    .mood-badge {{
        display: inline-block;
        background: var(--blush);
        color: var(--ink-brown);
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-weight: 700;
        border: 2.5px solid var(--dusty-rose);
        font-size: 1rem;
        margin: 0.2rem;
    }}

    /* Success/warning message styling */
    .stAlert {{
        background: rgba(253, 242, 240, 0.95) !important;
        border: 2px solid var(--dusty-rose) !important;
        border-radius: 15px !important;
        color: var(--ink-brown) !important;
        font-weight: 600 !important;
    }}

    /* ============================================
       🎀 SIDEBAR STYLING
    ============================================ */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, var(--cream), var(--blush)) !important;
        border-right: 3px solid var(--ink-brown);
    }}

    section[data-testid="stSidebar"] * {{
        color: var(--ink-brown) !important;
    }}

    section[data-testid="stSidebar"] a {{
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }}

    /* Hide default Streamlit sidebar page nav (we have our own cute one!) */
    [data-testid="stSidebarNav"] {{
        display: none !important;
    }}

    /* ============================================
       ✨ ANIMATIONS
    ============================================ */
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .fade-in {{
        animation: fadeInUp 0.6s ease-out;
    }}

    @keyframes float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}

    .floating {{
        animation: float 3s ease-in-out infinite;
    }}

    /* ============================================
       💌 SPECIAL LETTER CARD (for AI response)
    ============================================ */
    .letter-card {{
        background: 
            linear-gradient(135deg, rgba(253, 242, 240, 0.98), rgba(245, 225, 220, 0.98));
        border: 2.5px solid var(--ink-brown);
        border-radius: 22px;
        padding: 2.5rem;
        box-shadow: 5px 5px 0 var(--ink-brown);
        margin: 1.5rem 0;
        position: relative;
    }}

    .letter-card::before {{
        content: "💌";
        position: absolute;
        top: -20px;
        left: 30px;
        font-size: 1.8rem;
        background: var(--cream);
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2.5px solid var(--ink-brown);
        box-shadow: 2px 2px 0 var(--ink-brown);
    }}

    .letter-card::after {{
        content: "🧸";
        position: absolute;
        bottom: -20px;
        right: 30px;
        font-size: 1.8rem;
        background: var(--cream);
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 2.5px solid var(--ink-brown);
        box-shadow: 2px 2px 0 var(--ink-brown);
    }}
    </style>
    """, unsafe_allow_html=True)


# ============================================
# 🧸 SIGNATURE COMPONENT
# ============================================
def render_signature():
    """Cute signature at the bottom of pages"""
    st.markdown("""
    <div class="signature">
        Made with 🧸 by Vivi
    </div>
    """, unsafe_allow_html=True)