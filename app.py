"""
BearDiary AI 🐻📔
Your cozy AI journal companion
Made with 🧸 by Vivi
"""

import streamlit as st
from utils.styles import inject_base_styles, render_signature
from utils.sidebar import render_sidebar
from utils.hero import render_hero
from utils.database import init_db

# Page config
st.set_page_config(
    page_title="BearDiary AI 🐻",
    page_icon="🐻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject our gorgeous Teddy Plaid styles!
inject_base_styles()
init_db()
render_sidebar()

# 🐻 THE HERO SECTION (with mask reveal + working clock!)
render_hero()

# CTA Section below hero
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="cozy-card fade-in" style="text-align: center;">
        <h3>🌸 Ready to start your cozy journey?</h3>
        <p>Write your thoughts, track your moods, and get warm AI letters back 💌</p>
    </div>
    """, unsafe_allow_html=True)

# Buttons row
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col2:
    if st.button("📝 Write in Diary", use_container_width=True):
        st.switch_page("pages/1_📝_Write.py")
with col3:
    if st.button("📅 My Diary", use_container_width=True):
        st.switch_page("pages/2_📅_My_Diary.py")

# Signature
render_signature()

# Auto-refresh every second for clock (subtle trick!)
st.markdown("""
<script>
    setTimeout(function() {
        window.parent.location.reload();
    }, 60000);
</script>
""", unsafe_allow_html=True)