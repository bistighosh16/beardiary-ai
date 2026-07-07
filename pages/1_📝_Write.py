"""
BearDiary AI - Write Page 📝
Where you write your cozy thoughts + AI analyzes them
"""


import streamlit as st
from datetime import datetime
from utils.styles import inject_base_styles, render_signature
from utils.sidebar import render_sidebar
from utils.ai import analyze_entry
from utils.database import init_db, save_entry

# Page config
st.set_page_config(
    page_title="Write · BearDiary 🐻",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject styles + initialize DB
inject_base_styles()
init_db()

# Then render sidebar (needs DB ready for stats!)
render_sidebar()

# ============================================
# 🎀 PAGE HEADER
# ============================================
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;" class="fade-in">
    <h1>📝 Write in Your Diary</h1>
    <p class="handwritten">Pour your heart out, sweet soul ✨</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# 📅 DATE + PROMPT ROW
# ============================================
col_date, col_prompt = st.columns([1, 2])

with col_date:
    today = datetime.now().strftime("%A, %B %d")
    st.markdown(f"""
    <div class="cozy-card" style="text-align: center; padding: 1rem;">
        <div style="font-family: 'Caveat', cursive; font-size: 1.2rem; color: #8B6914;">today is</div>
        <div style="font-family: 'Fraunces', serif; font-size: 1.4rem; font-weight: 700; color: #5C3A21;">{today}</div>
    </div>
    """, unsafe_allow_html=True)

with col_prompt:
    st.markdown("""
    <div class="cozy-card" style="padding: 1rem;">
        <div style="font-family: 'Caveat', cursive; font-size: 1.2rem; color: #8B6914;">✨ gentle prompt</div>
        <div style="font-family: 'Quicksand', sans-serif; font-size: 1rem; color: #5C3A21;">
            How are you feeling today? What made you smile? What's weighing on your heart? 
            No pressure — just write what feels right 🎀
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# ✍️ THE JOURNAL TEXTAREA
# ============================================
entry_text = st.text_area(
    label="Your entry",
    placeholder="dear diary...\n\ntoday i felt...",
    height=300,
    label_visibility="collapsed",
    key="entry_input"
)

# Character counter
char_count = len(entry_text)
st.markdown(f"""
<div style="text-align: right; font-family: 'Caveat', cursive; color: #8B6914; font-size: 1.1rem;">
    {char_count} characters written 🎀
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# 🎀 SAVE + ANALYZE BUTTON
# ============================================
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    analyze_clicked = st.button(
        "💌 Save & Get AI Letter",
        use_container_width=True,
        type="primary"
    )

# ============================================
# 🤖 AI ANALYSIS + SAVE FLOW
# ============================================
if analyze_clicked:
    if not entry_text.strip():
        st.warning("🎀 Write something first, sweet friend!")
    elif len(entry_text.strip()) < 10:
        st.warning("🧸 Try writing a little more so I can understand you better!")
    else:
        with st.spinner("🐻 BearBestie is reading your entry with care..."):
            try:
                # 1️⃣ Analyze with AI
                result = analyze_entry(entry_text)
                
                # 2️⃣ Save to database
                entry_id = save_entry(
                    entry_text=entry_text,
                    mood=result["mood"],
                    mood_emoji=result["mood_emoji"],
                    vibe_word=result["vibe_word"],
                    letter=result["letter"],
                    affirmation=result["affirmation"]
                )
                
                # 3️⃣ Celebrate + display!
                st.balloons()
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Mood + Vibe row
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"""
                    <div class="cozy-card fade-in" style="text-align: center;">
                        <div style="font-family: 'Caveat', cursive; font-size: 1.2rem; color: #8B6914;">today's mood</div>
                        <div style="font-size: 3rem; margin: 0.5rem 0;">{result['mood_emoji']}</div>
                        <div style="font-family: 'Fraunces', serif; font-size: 1.5rem; font-weight: 700; color: #5C3A21; text-transform: capitalize;">
                            {result['mood']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_b:
                    st.markdown(f"""
                    <div class="cozy-card fade-in" style="text-align: center;">
                        <div style="font-family: 'Caveat', cursive; font-size: 1.2rem; color: #8B6914;">vibe of the day</div>
                        <div style="font-size: 2rem; margin: 0.5rem 0;">✨</div>
                        <div style="font-family: 'Fraunces', serif; font-size: 1.5rem; font-weight: 700; font-style: italic; color: #D4869C; text-transform: lowercase;">
                            {result['vibe_word']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # The AI Letter
                st.markdown(f"""
                <div class="letter-card fade-in" style="margin-top: 1.5rem;">
                    <div style="font-family: 'Caveat', cursive; font-size: 1.8rem; color: #D4869C; text-align: center; margin-bottom: 1rem; font-weight: 700;">
                        a letter from BearBestie
                    </div>
                    <div style="font-family: 'Quicksand', sans-serif; font-size: 1.2rem; line-height: 1.8; color: #3E2118; padding: 0 1rem; font-weight: 500;">
                        {result['letter']}
                    </div>
                    <div style="border-top: 2px dashed #E8A0BF; margin: 1.5rem 0 1rem 0;"></div>
                    <div style="text-align: center; font-family: 'Caveat', cursive; font-size: 1.6rem; color: #8B6914; font-weight: 700;">
                        ✨ {result['affirmation']} ✨
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.success(f"🎀 Entry #{entry_id} saved to your diary!")
                
            except ValueError as e:
                st.error(f"🔐 {str(e)}")
            except Exception as e:
                st.error(f"🥺 Something went wrong: {str(e)}")

st.markdown("<br><br>", unsafe_allow_html=True)

# Back to home button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("app.py")

render_signature()