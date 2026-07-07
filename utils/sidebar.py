"""
BearDiary AI - Cozy Sidebar 🎀🐻
Reusable adorable sidebar for all pages
"""

import streamlit as st
import random
from datetime import datetime
from utils.database import get_mood_stats, get_all_entries


# ============================================
# 💌 DAILY AFFIRMATIONS POOL
# ============================================
AFFIRMATIONS = [
    "you are doing better than you think 💕",
    "your feelings are valid, sweet soul 🎀",
    "today is a soft page in your story 🌸",
    "you are loved beyond measure 🧸",
    "rest is productive too, dear one ☕",
    "small steps still move you forward ✨",
    "you deserve gentleness today 🌷",
    "your heart is a garden — tend to it 🌸",
    "you belong exactly where you are 💌",
    "your softness is a superpower 🎀",
    "every day you show up matters 🌟",
    "you are the main character today ✨",
]


def get_daily_affirmation() -> str:
    """Pick an affirmation based on day-of-year (consistent per day!)"""
    day_seed = datetime.now().timetuple().tm_yday
    random.seed(day_seed)
    return random.choice(AFFIRMATIONS)


def render_sidebar():
    """Render the cozy sidebar on every page"""
    
    with st.sidebar:
        # ============================================
        # 🐻 LOGO + TAGLINE
        # ============================================
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0.5rem; border-bottom: 2px dashed #D4869C; margin-bottom: 1rem;">
            <div style="font-size: 3rem; margin-bottom: 0.3rem;">🐻</div>
            <div style="font-family: 'Fraunces', serif; font-size: 1.6rem; font-weight: 900; color: #3E2118; line-height: 1;">
                Bear<span style="color: #D4869C; font-style: italic;">Diary</span>
            </div>
            <div style="font-family: 'Caveat', cursive; font-size: 1.15rem; color: #8B6914; margin-top: 0.3rem;">
                your cozy corner ✨
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ============================================
        # 🎀 NAVIGATION
        # ============================================
        st.markdown("""
        <div style="font-family: 'Caveat', cursive; font-size: 1.3rem; color: #D4869C; margin: 0.5rem 0 0.3rem 0; font-weight: 700;">
            ✿ where to go
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠  Home", use_container_width=True, key="nav_home"):
            st.switch_page("app.py")
        if st.button("📝  Write in Diary", use_container_width=True, key="nav_write"):
            st.switch_page("pages/1_📝_Write.py")
        if st.button("📅  My Diary", use_container_width=True, key="nav_diary"):
            st.switch_page("pages/2_📅_My_Diary.py")
        if st.button("🌸  Mood Garden", use_container_width=True, key="nav_garden"):
            st.switch_page("pages/3_🌸_Mood_Garden.py")
        
        # ============================================
        # 📊 LIVE STATS
        # ============================================
        st.markdown("""
        <div style="font-family: 'Caveat', cursive; font-size: 1.3rem; color: #D4869C; margin: 1.5rem 0 0.5rem 0; font-weight: 700;">
            ✿ your cozy stats
        </div>
        """, unsafe_allow_html=True)
        
        try:
            stats = get_mood_stats()
            all_entries = get_all_entries()
            total = stats.get("total_entries", 0)
            top_mood = stats.get("top_mood") or "—"
            
            # Simple streak: consecutive days from today going back
            entry_dates = sorted(set(e["entry_date"] for e in all_entries), reverse=True)
            streak = 0
            if entry_dates:
                today = datetime.now().strftime("%Y-%m-%d")
                if entry_dates[0] == today:
                    streak = 1
                    for i in range(1, len(entry_dates)):
                        prev = datetime.strptime(entry_dates[i-1], "%Y-%m-%d")
                        curr = datetime.strptime(entry_dates[i], "%Y-%m-%d")
                        if (prev - curr).days == 1:
                            streak += 1
                        else:
                            break
            
            st.markdown(f"""
            <div style="background: rgba(253, 242, 240, 0.8); border: 2px solid #D4869C; border-radius: 15px; padding: 0.8rem; margin: 0.3rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.3rem 0;">
                    <span style="font-family: 'Quicksand', sans-serif; font-weight: 600; color: #3E2118;">📖 entries</span>
                    <span style="font-family: 'Fraunces', serif; font-weight: 900; color: #D4869C; font-size: 1.2rem;">{total}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.3rem 0; border-top: 1px dashed #E8A0BF;">
                    <span style="font-family: 'Quicksand', sans-serif; font-weight: 600; color: #3E2118;">🔥 streak</span>
                    <span style="font-family: 'Fraunces', serif; font-weight: 900; color: #D4869C; font-size: 1.2rem;">{streak}d</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.3rem 0; border-top: 1px dashed #E8A0BF;">
                    <span style="font-family: 'Quicksand', sans-serif; font-weight: 600; color: #3E2118;">🌸 top mood</span>
                    <span style="font-family: 'Fraunces', serif; font-weight: 700; color: #D4869C; text-transform: capitalize; font-size: 0.95rem;">{top_mood}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        except Exception:
            st.markdown("""
            <div style="text-align: center; padding: 0.5rem; color: #8B6914; font-family: 'Caveat', cursive; font-size: 1.1rem;">
                write your first entry to see stats! 🎀
            </div>
            """, unsafe_allow_html=True)
        
        # ============================================
        # 💌 DAILY AFFIRMATION
        # ============================================
        affirmation = get_daily_affirmation()
        st.markdown(f"""
        <div style="font-family: 'Caveat', cursive; font-size: 1.3rem; color: #D4869C; margin: 1.5rem 0 0.5rem 0; font-weight: 700;">
            ✿ today's whisper
        </div>
        <div style="background: linear-gradient(135deg, #F5E1DC, #E8A0BF); border: 2px solid #3E2118; border-radius: 15px; padding: 1rem; text-align: center; box-shadow: 3px 3px 0 #3E2118;">
            <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">💌</div>
            <div style="font-family: 'Caveat', cursive; font-size: 1.2rem; color: #3E2118; font-weight: 700; line-height: 1.4;">
                {affirmation}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ============================================
        # 🍵 COZY QUOTE (rotating)
        # ============================================
        cozy_quotes = [
            ("🍵", "sip slowly, savor deeply"),
            ("🌸", "bloom in your own time"),
            ("📖", "one page at a time"),
            ("☕", "warm hands, warm heart"),
            ("🕯️", "you glow softly"),
            ("🌙", "rest is holy work"),
        ]
        quote_seed = datetime.now().timetuple().tm_yday
        random.seed(quote_seed + 100)
        emoji, quote = random.choice(cozy_quotes)
        
        st.markdown(f"""
        <div style="margin: 1.5rem 0; text-align: center; padding: 0.8rem; background: rgba(253, 242, 240, 0.6); border-radius: 12px; border: 1.5px dashed #D4869C;">
            <div style="font-size: 1.5rem;">{emoji}</div>
            <div style="font-family: 'Caveat', cursive; font-size: 1.1rem; color: #8B6914; font-style: italic;">
                "{quote}"
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ============================================
        # 🧸 FOOTER SIGNATURE
        # ============================================
        st.markdown("""
        <div style="margin-top: 2rem; padding-top: 1rem; border-top: 2px dashed #D4869C; text-align: center;">
            <div style="font-family: 'Caveat', cursive; font-size: 1.1rem; color: #8B6914;">
                made with 🧸<br>by <strong style="color: #D4869C;">Vivi</strong>
            </div>
            <div style="margin-top: 0.5rem; font-size: 0.85rem; color: #8B6914; opacity: 0.7;">
                v1.0 · cozy edition
            </div>
        </div>
        """, unsafe_allow_html=True)