"""
BearDiary AI - Mood Garden Page 🌸📊
Beautiful analytics + mood insights
"""

import streamlit as st
import base64
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px

from utils.styles import inject_base_styles, render_signature
from utils.sidebar import render_sidebar
from utils.database import init_db, get_all_entries, get_mood_stats

# Page config
st.set_page_config(
    page_title="Mood Garden · BearDiary 🌸",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_base_styles()
init_db()
render_sidebar()


# ============================================
# 🎨 COLOR PALETTE FOR CHARTS
# ============================================
MOOD_COLORS = {
    "happy": "#E8A0BF",
    "sad": "#A0B4CC",
    "anxious": "#C9A88E",
    "peaceful": "#B8C4A0",
    "excited": "#F5A5B8",
    "tired": "#B8A89E",
    "angry": "#D4869C",
    "grateful": "#E8A0BF",
    "hopeful": "#F5C2A5",
    "confused": "#C9B4CC",
}

MOOD_EMOJIS = {
    "happy": "😊", "sad": "🥺", "anxious": "😰", "peaceful": "🌸",
    "excited": "🥳", "tired": "😴", "angry": "😤", "grateful": "🙏",
    "hopeful": "🌈", "confused": "😵‍💫",
}


# ============================================
# 🖼️ LOAD HEADER IMAGE
# ============================================
def get_header_image_b64():
    path = Path(__file__).parent.parent / "assets" / "mood-garden-header.jpg"
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""


header_b64 = get_header_image_b64()
header_url = f"data:image/jpeg;base64,{header_b64}" if header_b64 else ""


# ============================================
# 🎀 GORGEOUS HEADER IMAGE BANNER
# ============================================
if header_url:
    st.markdown(f"""
    <div class="garden-header fade-in">
        <img src="{header_url}" alt="Mood Garden" />
        <div class="garden-header-overlay">
            <div class="garden-tagline">✿ ˚｡⋆ your cozy little garden ⋆｡˚ ✿</div>
            <p class="garden-subtitle">where feelings bloom into insights 🌸</p>
        </div>
    </div>
    
    <style>
    .garden-header {{
        position: relative;
        width: 100%;
        height: 320px;
        border-radius: 25px;
        overflow: hidden;
        border: 3px solid #3E2118;
        box-shadow: 6px 6px 0 #3E2118;
        margin-bottom: 2rem;
    }}
    
    .garden-header img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }}
    
    .garden-header-overlay {{
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        background: radial-gradient(ellipse at center, 
            rgba(0, 0, 0, 0.35) 0%, 
            rgba(0, 0, 0, 0.15) 60%,
            rgba(0, 0, 0, 0.05) 100%);
        color: #FFFFFF;
        padding: 2rem;
    }}
    
    .garden-header-overlay .garden-tagline {{
        font-family: 'Caveat', cursive !important;
        font-size: 2.5rem !important;
        color: #FFFFFF !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: 2px !important;
        text-shadow: 
            2px 2px 8px rgba(0, 0, 0, 0.9),
            0 0 20px rgba(0, 0, 0, 0.7) !important;
    }}
    
    .garden-header-overlay h1.garden-title {{
        font-family: 'Fraunces', serif !important;
        font-size: 5rem !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        margin: 0.5rem 0 !important;
        letter-spacing: -0.02em !important;
        text-shadow: 
            3px 3px 0 rgba(62, 33, 24, 1),
            4px 4px 15px rgba(0, 0, 0, 0.9),
            0 0 30px rgba(0, 0, 0, 0.7) !important;
    }}
    
    .garden-header-overlay .garden-subtitle {{
        font-family: 'Quicksand', sans-serif !important;
        font-size: 1.7rem !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        margin-top: 0.5rem !important;
        text-shadow: 
            2px 2px 8px rgba(0, 0, 0, 0.9),
            0 0 15px rgba(0, 0, 0, 0.7) !important;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;" class="fade-in">
        <h1>🌸 Mood Garden</h1>
        <p class="handwritten">where feelings bloom into insights 🌸</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# 📊 FETCH DATA
# ============================================
all_entries = get_all_entries()
stats = get_mood_stats()

# ============================================
# 🌸 EMPTY STATE
# ============================================
if not all_entries:
    st.markdown("""
    <div class="cozy-card fade-in" style="text-align: center; padding: 3rem;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">🌱</div>
        <h3 style="color: #3E2118;">your garden is waiting to bloom</h3>
        <p class="handwritten" style="margin-top: 1rem;">
            write a few entries and watch your feelings grow into a beautiful mood map ✨
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📝 Start Journaling", use_container_width=True):
            st.switch_page("pages/1_📝_Write.py")
    
    render_signature()
    st.stop()


# ============================================
# 📊 STAT CARDS ROW
# ============================================
st.markdown("""
<div style="text-align: center; margin: 1rem 0;">
    <p class="handwritten" style="color: #D4869C; font-size: 1.8rem;">
        ✿ your cozy overview ✿
    </p>
</div>
""", unsafe_allow_html=True)

# Calculate additional stats
total_entries = stats["total_entries"]
top_mood = stats.get("top_mood") or "peaceful"

# Streak calculation
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

# Average entries per week
if len(entry_dates) >= 2:
    first_date = datetime.strptime(entry_dates[-1], "%Y-%m-%d")
    last_date = datetime.strptime(entry_dates[0], "%Y-%m-%d")
    days_span = max((last_date - first_date).days, 1)
    weeks = max(days_span / 7, 0.14)  # min ~1 day
    avg_per_week = round(total_entries / weeks, 1)
else:
    avg_per_week = total_entries

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="cozy-card-plain fade-in" style="text-align: center; padding: 1.3rem;">
        <div style="font-size: 2.2rem;">📖</div>
        <div style="font-family: 'Fraunces', serif; font-size: 2.2rem; font-weight: 900; color: #3E2118; line-height: 1;">
            {total_entries}
        </div>
        <div style="font-family: 'Caveat', cursive; font-size: 1.2rem; color: #8B6914; margin-top: 0.3rem;">
            total entries
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="cozy-card-plain fade-in" style="text-align: center; padding: 1.3rem;">
        <div style="font-size: 2.2rem;">🔥</div>
        <div style="font-family: 'Fraunces', serif; font-size: 2.2rem; font-weight: 900; color: #3E2118; line-height: 1;">
            {streak}
        </div>
        <div style="font-family: 'Caveat', cursive; font-size: 1.2rem; color: #8B6914; margin-top: 0.3rem;">
            day streak
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    top_emoji = MOOD_EMOJIS.get(top_mood, "💕")
    st.markdown(f"""
    <div class="cozy-card-plain fade-in" style="text-align: center; padding: 1.3rem;">
        <div style="font-size: 2.2rem;">{top_emoji}</div>
        <div style="font-family: 'Fraunces', serif; font-size: 1.4rem; font-weight: 900; color: #3E2118; line-height: 1; text-transform: capitalize; margin-top: 0.5rem;">
            {top_mood}
        </div>
        <div style="font-family: 'Caveat', cursive; font-size: 1.2rem; color: #8B6914; margin-top: 0.3rem;">
            top mood
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="cozy-card-plain fade-in" style="text-align: center; padding: 1.3rem;">
        <div style="font-size: 2.2rem;">🌸</div>
        <div style="font-family: 'Fraunces', serif; font-size: 2.2rem; font-weight: 900; color: #3E2118; line-height: 1;">
            {avg_per_week}
        </div>
        <div style="font-family: 'Caveat', cursive; font-size: 1.2rem; color: #8B6914; margin-top: 0.3rem;">
            entries / week
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ============================================
# 🌈 MOOD DISTRIBUTION — PIE CHART
# ============================================
st.markdown("""
<div style="text-align: center; margin: 1.5rem 0 1rem 0;">
    <p class="handwritten" style="color: #D4869C; font-size: 1.8rem;">
        ✿ your mood garden ✿
    </p>
</div>
""", unsafe_allow_html=True)

col_chart, col_insights = st.columns([3, 2])

with col_chart:
    mood_counts = stats.get("mood_counts", {})
    
    if mood_counts:
        # Prepare data with emojis in labels
        labels = [f"{MOOD_EMOJIS.get(m, '💕')} {m.capitalize()}" for m in mood_counts.keys()]
        values = list(mood_counts.values())
        colors = [MOOD_COLORS.get(m, "#E8A0BF") for m in mood_counts.keys()]
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.55,
            marker=dict(
                colors=colors,
                line=dict(color='#3E2118', width=2.5)
            ),
            textfont=dict(
                family="Quicksand, sans-serif",
                size=14,
                color="#3E2118"
            ),
            hovertemplate="<b>%{label}</b><br>%{value} entries<br>%{percent}<extra></extra>",
        )])
        
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Quicksand, sans-serif", color="#3E2118", size=13),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05,
                bgcolor="rgba(0,0,0,0)",
                font=dict(size=12)
            ),
            margin=dict(t=20, b=20, l=20, r=20),
            height=380,
            annotations=[dict(
                text=f"<b>{total_entries}</b><br><span style='font-size:14px;'>entries</span>",
                x=0.5, y=0.5,
                font=dict(size=28, family="Fraunces, serif", color="#3E2118"),
                showarrow=False
            )]
        )
        
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

with col_insights:
    # Fun insight card
    if mood_counts:
        top_2 = sorted(mood_counts.items(), key=lambda x: -x[1])[:2]
        
        insight_text = f"you've felt <strong style='color: #D4869C;'>{top_mood}</strong> most often 🎀"
        if len(top_2) >= 2:
            second_mood = top_2[1][0]
            insight_text += f"<br><br>followed by moments of <strong style='color: #D4869C;'>{second_mood}</strong> {MOOD_EMOJIS.get(second_mood, '💕')}"
        
        st.markdown(f"""
        <div class="cozy-card-plain fade-in" style="padding: 1.8rem;">
            <div style="font-family: 'Caveat', cursive; font-size: 1.5rem; color: #D4869C; text-align: center; margin-bottom: 1rem; font-weight: 700;">
                ✨ garden insight ✨
            </div>
            <div style="font-family: 'Quicksand', sans-serif; font-size: 1.1rem; color: #3E2118; line-height: 1.7; text-align: center;">
                {insight_text}
            </div>
            <div style="border-top: 2px dashed #E8A0BF; margin: 1.2rem 0;"></div>
            <div style="text-align: center; font-family: 'Caveat', cursive; font-size: 1.3rem; color: #8B6914;">
                every mood is a flower in your garden 🌸
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================
# 🌸 MOOD JOURNEY STRIP (recent moods as cute dots!)
# ============================================
recent_entries_with_mood = [e for e in all_entries if e.get("mood")]

if recent_entries_with_mood:
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0 1rem 0;">
        <p class="handwritten" style="color: #D4869C; font-size: 1.8rem;">
            ✿ your recent mood journey ✿
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Build cute mood dots strip (last 14 entries)
    dots_html = ""
    for entry in reversed(recent_entries_with_mood[-14:]):
        mood = entry["mood"]
        emoji = MOOD_EMOJIS.get(mood, "💕")
        color = MOOD_COLORS.get(mood, "#E8A0BF")
        vibe = entry.get("vibe_word", "cozy")
        date_str = entry["entry_date"]
        
        dots_html += f'<div title="{date_str} · {mood} · {vibe}" style="display:inline-flex;flex-direction:column;align-items:center;margin:0.5rem;"><div style="width:60px;height:60px;border-radius:50%;background:{color};border:3px solid #3E2118;box-shadow:3px 3px 0 #3E2118;display:flex;align-items:center;justify-content:center;font-size:2rem;cursor:default;">{emoji}</div><div style="font-family:Caveat,cursive;font-size:1rem;color:#8B6914;margin-top:0.3rem;font-weight:700;">{date_str[-5:]}</div></div>'
    
    strip_html = f'<div class="cozy-card-plain fade-in" style="text-align:center;padding:1.5rem;"><div style="font-family:Caveat,cursive;font-size:1.2rem;color:#8B6914;margin-bottom:1rem;">each dot is a day, each color is a feeling 🎀</div><div style="display:flex;flex-wrap:wrap;justify-content:center;">{dots_html}</div></div>'
    
    st.markdown(strip_html, unsafe_allow_html=True)

# ============================================
# 🏆 ACHIEVEMENT BADGES
# ============================================
st.markdown("""
<div style="text-align: center; margin: 2rem 0 1rem 0;">
    <p class="handwritten" style="color: #D4869C; font-size: 1.8rem;">
        ✿ your cozy achievements ✿
    </p>
</div>
""", unsafe_allow_html=True)

achievements = [
    ("🌱", "First Bloom", "Write your first entry", total_entries >= 1),
    ("🌸", "Blooming", "Write 5 entries", total_entries >= 5),
    ("🌷", "Garden Grows", "Write 10 entries", total_entries >= 10),
    ("🌹", "Full Garden", "Write 25 entries", total_entries >= 25),
    ("🔥", "Cozy Streak", "3-day streak", streak >= 3),
    ("💫", "Journal Devotee", "7-day streak", streak >= 7),
    ("🎀", "Mood Explorer", "Log 5 different moods", len(mood_counts) >= 5),
    ("💌", "AI Bestie", "Get 10 comfort letters", total_entries >= 10),
]

# Display in a 4-column grid
badge_cols = st.columns(4)
for idx, (emoji, name, desc, earned) in enumerate(achievements):
    with badge_cols[idx % 4]:
        opacity = "1" if earned else "0.35"
        bg = "rgba(232, 160, 191, 0.15)" if earned else "rgba(200, 200, 200, 0.1)"
        border_style = "solid" if earned else "dashed"
        status = "earned!" if earned else "locked"
        status_color = "#D4869C" if earned else "#8B6914"
        
        st.markdown(f"""
        <div style="
            background: {bg};
            border: 2.5px {border_style} #3E2118;
            border-radius: 18px;
            padding: 1rem;
            text-align: center;
            margin: 0.4rem 0;
            opacity: {opacity};
            box-shadow: 3px 3px 0 rgba(62, 33, 24, 0.3);
            min-height: 160px;
        ">
            <div style="font-size: 2.5rem; margin-bottom: 0.3rem;">{emoji}</div>
            <div style="font-family: 'Fraunces', serif; font-weight: 700; color: #3E2118; font-size: 1rem;">
                {name}
            </div>
            <div style="font-family: 'Quicksand', sans-serif; font-size: 0.85rem; color: #5C3A21; margin: 0.4rem 0; line-height: 1.3;">
                {desc}
            </div>
            <div style="font-family: 'Caveat', cursive; color: {status_color}; font-size: 1rem; font-weight: 700; margin-top: 0.3rem;">
                ✨ {status}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ============================================
# ✨ VIBE VOCABULARY
# ============================================
st.markdown("""
<div style="text-align: center; margin: 2.5rem 0 1rem 0;">
    <p class="handwritten" style="color: #D4869C; font-size: 1.8rem;">
        ✿ your vibe vocabulary ✿
    </p>
</div>
""", unsafe_allow_html=True)

vibe_words = [e.get("vibe_word") for e in all_entries if e.get("vibe_word")]
vibe_counter = Counter(vibe_words)

if vibe_counter:
    max_count = max(vibe_counter.values())
    
    # Build all vibe pills as a single-line HTML string (avoids Streamlit sanitizer bugs!)
    vibe_pills = ""
    for vibe, count in vibe_counter.most_common(20):
        size = round(1.0 + (count / max_count) * 1.2, 2)
        opacity = round(0.6 + (count / max_count) * 0.4, 2)
        vibe_pills += f'<span style="display:inline-block;margin:0.4rem;padding:0.5rem 1.2rem;background:linear-gradient(135deg,#F5E1DC,#E8A0BF);color:#3E2118;font-family:Fraunces,serif;font-style:italic;font-weight:700;font-size:{size}rem;border-radius:25px;border:2px solid #3E2118;box-shadow:2px 2px 0 #3E2118;opacity:{opacity};">{vibe}</span>'
    
    full_html = f'<div class="cozy-card-plain fade-in" style="text-align:center;padding:2rem;"><div style="font-family:Caveat,cursive;font-size:1.3rem;color:#8B6914;margin-bottom:1rem;">words BearBestie has used to describe your days 💌</div><div>{vibe_pills}</div></div>'
    
    st.markdown(full_html, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# 🏠 NAVIGATION FOOTER
# ============================================
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🏠 Back to Home", use_container_width=True):
        st.switch_page("app.py")
with col2:
    if st.button("📝 Write New Entry", use_container_width=True):
        st.switch_page("pages/1_📝_Write.py")
with col3:
    if st.button("📅 My Diary", use_container_width=True):
        st.switch_page("pages/2_📅_My_Diary.py")

render_signature()