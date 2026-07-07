"""
BearDiary AI - My Diary Page 📅
Timeline of all your past entries + AI letters
"""

import streamlit as st
from datetime import datetime
from utils.styles import inject_base_styles, render_signature
from utils.sidebar import render_sidebar
from utils.database import (
    init_db, 
    get_all_entries, 
    delete_entry, 
    get_mood_stats
)

# Page config
st.set_page_config(
    page_title="My Diary · BearDiary 🐻",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject styles + initialize DB
inject_base_styles()
init_db()
render_sidebar()

# Mood emoji fallback map (if any entry has missing emoji)
MOOD_EMOJIS = {
    "happy": "😊",
    "sad": "🥺",
    "anxious": "😰",
    "peaceful": "🌸",
    "excited": "🥳",
    "tired": "😴",
    "angry": "😤",
    "grateful": "🙏",
    "hopeful": "🌈",
    "confused": "😵‍💫",
}


def format_date(date_str: str) -> str:
    """Convert YYYY-MM-DD to 'Monday, Jan 15' style"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%A, %B %d, %Y")
    except:
        return date_str


def format_time(datetime_str: str) -> str:
    """Convert full datetime to time only"""
    try:
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%I:%M %p").lstrip("0")
    except:
        return ""


# ============================================
# 🎀 PAGE HEADER
# ============================================
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;" class="fade-in">
    <h1>📅 My Diary</h1>
    <p class="handwritten">every entry, every mood, every letter 💌</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# 📊 STATS ROW
# ============================================
stats = get_mood_stats()
all_entries = get_all_entries()

if stats["total_entries"] > 0:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="cozy-card-plain fade-in" style="text-align: center; padding: 1.5rem;">
            <div style="font-family: 'Caveat', cursive; font-size: 1.3rem; color: #8B6914;">total entries</div>
            <div style="font-size: 2.5rem; margin: 0.3rem 0;">📖</div>
            <div style="font-family: 'Fraunces', serif; font-size: 2rem; font-weight: 900; color: #3E2118;">
                {stats['total_entries']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        top_mood = stats.get("top_mood") or "peaceful"
        top_emoji = MOOD_EMOJIS.get(top_mood, "💕")
        st.markdown(f"""
        <div class="cozy-card-plain fade-in" style="text-align: center; padding: 1.5rem;">
            <div style="font-family: 'Caveat', cursive; font-size: 1.3rem; color: #8B6914;">top mood</div>
            <div style="font-size: 2.5rem; margin: 0.3rem 0;">{top_emoji}</div>
            <div style="font-family: 'Fraunces', serif; font-size: 1.6rem; font-weight: 700; color: #3E2118; text-transform: capitalize;">
                {top_mood}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Get most recent entry date
        most_recent = all_entries[0]["entry_date"] if all_entries else "—"
        recent_display = format_date(most_recent).split(",")[0] if most_recent != "—" else "—"
        st.markdown(f"""
        <div class="cozy-card-plain fade-in" style="text-align: center; padding: 1.5rem;">
            <div style="font-family: 'Caveat', cursive; font-size: 1.3rem; color: #8B6914;">last entry</div>
            <div style="font-size: 2.5rem; margin: 0.3rem 0;">🎀</div>
            <div style="font-family: 'Fraunces', serif; font-size: 1.4rem; font-weight: 700; color: #3E2118;">
                {recent_display}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# 📖 ENTRIES TIMELINE
# ============================================
if not all_entries:
    # Empty state — SO cute!
    st.markdown("""
    <div class="cozy-card fade-in" style="text-align: center; padding: 3rem;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">🧸</div>
        <h3 style="color: #3E2118;">your diary is empty (for now)</h3>
        <p class="handwritten" style="margin-top: 1rem;">
            once you write your first entry, it'll live here forever ✨
        </p>
        <p style="color: #8B6914; margin-top: 1rem;">
            head over to the <strong>Write</strong> page to get started!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📝 Start Writing", use_container_width=True):
            st.switch_page("pages/1_📝_Write.py")

else:
    # Timeline header
    st.markdown(f"""
    <div style="text-align: center; margin: 1rem 0 2rem 0;">
        <p class="handwritten" style="color: #8B6914;">
            ✨ your cozy timeline ({len(all_entries)} {'entry' if len(all_entries) == 1 else 'entries'}) ✨
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show each entry
    for idx, entry in enumerate(all_entries):
        entry_id = entry["id"]
        entry_date = format_date(entry["entry_date"])
        entry_time = format_time(entry["created_at"])
        mood = entry.get("mood") or "peaceful"
        mood_emoji = entry.get("mood_emoji") or MOOD_EMOJIS.get(mood, "💕")
        vibe_word = entry.get("vibe_word") or "cozy"
        entry_text = entry["entry_text"]
        letter = entry.get("letter") or "(no letter available)"
        affirmation = entry.get("affirmation") or ""
        
        # Preview: first 120 chars of entry
        preview = entry_text[:120].strip()
        if len(entry_text) > 120:
            preview += "..."
        
        # Entry card
        st.markdown(f"""
        <div class="cozy-card-plain fade-in" style="margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <div style="font-family: 'Fraunces', serif; font-size: 1.4rem; font-weight: 700; color: #3E2118;">
                        {mood_emoji} {entry_date}
                    </div>
                    <div style="font-family: 'Caveat', cursive; font-size: 1.2rem; color: #8B6914; margin-top: 0.2rem;">
                        {entry_time} · vibe: <span style="color: #D4869C; font-style: italic; font-weight: 700;">{vibe_word}</span>
                    </div>
                </div>
                <div>
                    <span class="mood-badge">{mood_emoji} {mood.capitalize()}</span>
                </div>
            </div>
            <div style="margin-top: 1rem; font-family: 'Quicksand', sans-serif; font-size: 1.1rem; color: #3E2118; line-height: 1.6; font-style: italic;">
                "{preview}"
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Expand + Delete buttons row
        col_a, col_b, col_c = st.columns([2, 1, 1])
        
        with col_b:
            show_full = st.button(
                "📖 Read Full",
                key=f"read_{entry_id}",
                use_container_width=True
            )
        
        with col_c:
            delete_clicked = st.button(
                "🗑️ Delete",
                key=f"delete_{entry_id}",
                use_container_width=True
            )
        
        # Handle delete with confirmation
        if delete_clicked:
            st.session_state[f"confirm_delete_{entry_id}"] = True
        
        if st.session_state.get(f"confirm_delete_{entry_id}", False):
            st.warning(f"🥺 Are you sure you want to delete this entry from {entry_date}?")
            col_x, col_y, col_z = st.columns([1, 1, 1])
            with col_x:
                if st.button("Yes, delete it", key=f"yes_del_{entry_id}", use_container_width=True):
                    delete_entry(entry_id)
                    st.session_state[f"confirm_delete_{entry_id}"] = False
                    st.success("Entry deleted 🎀")
                    st.rerun()
            with col_y:
                if st.button("No, keep it 💕", key=f"no_del_{entry_id}", use_container_width=True):
                    st.session_state[f"confirm_delete_{entry_id}"] = False
                    st.rerun()
        
        # Show full entry + letter (only if button clicked in this session)
        if st.session_state.get(f"show_full_{entry_id}", False) or show_full:
            st.session_state[f"show_full_{entry_id}"] = True
            
            # Full entry
            st.markdown(f"""
            <div class="cozy-card fade-in" style="margin-top: 0.5rem;">
                <div style="font-family: 'Caveat', cursive; font-size: 1.5rem; color: #D4869C; text-align: center; margin-bottom: 1rem; font-weight: 700;">
                    ✍️ what you wrote
                </div>
                <div style="font-family: 'Caveat', cursive; font-size: 1.5rem; color: #3E2118; line-height: 1.6; padding: 0 1rem; white-space: pre-wrap;">
                    {entry_text}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # AI Letter
            st.markdown(f"""
            <div class="letter-card fade-in" style="margin-top: 0.5rem;">
                <div style="font-family: 'Caveat', cursive; font-size: 1.8rem; color: #D4869C; text-align: center; margin-bottom: 1rem; font-weight: 700;">
                    a letter from BearBestie
                </div>
                <div style="font-family: 'Quicksand', sans-serif; font-size: 1.2rem; line-height: 1.8; color: #3E2118; padding: 0 1rem; font-weight: 500;">
                    {letter}
                </div>
                <div style="border-top: 2px dashed #E8A0BF; margin: 1.5rem 0 1rem 0;"></div>
                <div style="text-align: center; font-family: 'Caveat', cursive; font-size: 1.6rem; color: #8B6914; font-weight: 700;">
                    ✨ {affirmation} ✨
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Hide again button
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🎀 Collapse", key=f"hide_{entry_id}", use_container_width=True):
                    st.session_state[f"show_full_{entry_id}"] = False
                    st.rerun()
        
        # Divider between entries
        st.markdown("""
        <div style="text-align: center; margin: 1.5rem 0; color: #D4869C; font-size: 1.5rem;">
            ⋆ ˚｡⋆୨୧˚ ˚୨୧⋆｡˚ ⋆
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# 🏠 NAVIGATION BUTTONS
# ============================================
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("app.py")
with col3:
    if st.button("📝 Write New Entry", use_container_width=True):
        st.switch_page("pages/1_📝_Write.py")

render_signature()