"""
BearDiary AI - Hero Section 🐻✨
Mask reveal effect + working analog clock
"""

import streamlit as st
import base64
from datetime import datetime
from pathlib import Path


def _get_image_b64(filename: str) -> str:
    """Load image from assets folder as base64"""
    try:
        path = Path(__file__).parent.parent / "assets" / filename
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""


def render_hero():
    """Render the hero section with mask reveal + working clock"""
    
    # Get current time for the clock hands
    now = datetime.now()
    hour = now.hour % 12
    minute = now.minute
    second = now.second
    
    # Calculate rotation angles (12 o'clock = 0deg)
    hour_deg = (hour * 30) + (minute * 0.5)
    minute_deg = minute * 6
    second_deg = second * 6
    
    # Load the sticker background image
    stickers_b64 = _get_image_b64("stickers-bg.jpg")
    sticker_bg_url = f"data:image/jpeg;base64,{stickers_b64}" if stickers_b64 else ""
    
    hero_html = f"""
    <div class="hero-wrapper">
        <!-- Mask Reveal Hero -->
        <div class="hero-mask" id="heroMask">
            <!-- Sticker background image layer (bottom) -->
            <div class="sticker-bg"></div>
            
            <!-- Top layer with mask reveal -->
            <div class="hero-cover" id="heroCover">
                <!-- Cute Clock (INSIDE hero, top right) -->
                <div class="clock-container">
                    <div class="clock-face">
                        <div class="marker marker-12">12</div>
                        <div class="marker marker-3">3</div>
                        <div class="marker marker-6">6</div>
                        <div class="marker marker-9">9</div>
                        <div class="clock-center">🐻</div>
                        <div class="hand hour-hand" style="transform: translateX(-50%) rotate({hour_deg}deg);"></div>
                        <div class="hand minute-hand" style="transform: translateX(-50%) rotate({minute_deg}deg);"></div>
                        <div class="hand second-hand" style="transform: translateX(-50%) rotate({second_deg}deg);"></div>
                        <div class="clock-dot"></div>
                    </div>
                    <div class="clock-label">cozy time ✨</div>
                </div>

                <div class="hero-content">
                    <div class="hero-tagline">✍️ your cozy corner ✍️</div>
                    <h1 class="hero-title">Bear<span class="title-accent">Diary</span></h1>
                    <p class="hero-subtitle">a little journal, a warm hug, an AI bestie 🧸</p>
                    <p class="hero-hint">✨ hover me to peek inside ✨</p>
                </div>
            </div>
        </div>
    </div>

    <style>
    /* ============================================
       🎪 HERO WRAPPER
    ============================================ */
    .hero-wrapper {{
        position: relative;
        width: 100%;
        padding: 1rem 0;
        animation: fadeInUp 0.8s ease-out;
    }}

    /* ============================================
       🕰️ CUTE CLOCK
    ============================================ */
    .clock-container {{
        position: absolute;
        top: 20px;
        right: 25px;
        z-index: 50;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
        pointer-events: none;
    }}

    .clock-face {{
        position: relative;
        width: 95px;
        height: 95px;
        border-radius: 50%;
        background: linear-gradient(135deg, #FDF2F0, #F5E1DC);
        border: 3px solid #E8A0BF;
        box-shadow: 
            3px 3px 0 rgba(0, 0, 0, 0.3),
            inset 0 0 12px rgba(212, 134, 156, 0.2);
    }}

    .marker {{
        position: absolute;
        font-family: 'Fraunces', serif;
        font-weight: 700;
        color: #5C3A21;
        font-size: 0.75rem;
    }}

    .marker-12 {{ top: 6px; left: 50%; transform: translateX(-50%); }}
    .marker-3  {{ right: 8px; top: 50%; transform: translateY(-50%); }}
    .marker-6  {{ bottom: 6px; left: 50%; transform: translateX(-50%); }}
    .marker-9  {{ left: 8px; top: 50%; transform: translateY(-50%); }}

    .clock-center {{
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 1.2rem;
        z-index: 1;
    }}

    .hand {{
        position: absolute;
        left: 50%;
        bottom: 50%;
        transform-origin: 50% 100%;
        border-radius: 4px;
        z-index: 2;
    }}

    .hour-hand   {{ width: 4px; height: 25px; background: #5C3A21; }}
    .minute-hand {{ width: 3px; height: 35px; background: #8B6914; }}
    .second-hand {{ width: 2px; height: 38px; background: #E8A0BF; }}

    .clock-dot {{
        position: absolute;
        top: 50%;
        left: 50%;
        width: 8px;
        height: 8px;
        background: #5C3A21;
        border-radius: 50%;
        transform: translate(-50%, -50%);
        z-index: 3;
    }}

    .clock-label {{
        font-family: 'Caveat', cursive;
        font-size: 1rem;
        color: #E8A0BF;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    }}

    /* ============================================
       🎭 MASK REVEAL HERO
    ============================================ */
    .hero-mask {{
        position: relative;
        width: 100%;
        height: 450px;
        border-radius: 30px;
        overflow: hidden;
        border: 3px solid #5C3A21;
        box-shadow: 8px 8px 0 #5C3A21;
        cursor: none;
    }}

    /* Sticker background (bottom layer — always there) */
    .sticker-bg {{
        position: absolute;
        inset: 0;
        background-image: url('{sticker_bg_url}');
        background-size: cover;
        background-position: center;
        z-index: 1;
    }}

    /* Top cover layer (this gets the "hole" cut into it) */
    .hero-cover {{
        position: absolute;
        inset: 0;
        z-index: 2;
        background: linear-gradient(135deg, 
            #3E2118 0%, 
            #5C3A21 50%,
            #2D1810 100%);
        -webkit-mask-image: radial-gradient(circle 0px at 50% 50%, transparent 99%, black 100%);
        mask-image: radial-gradient(circle 0px at 50% 50%, transparent 99%, black 100%);
        -webkit-mask-repeat: no-repeat;
        mask-repeat: no-repeat;
        transition: -webkit-mask-image 0.08s linear, mask-image 0.08s linear;
    }}

    .hero-content {{
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: #FDF2F0;
        pointer-events: none;
    }}

    .hero-tagline {{
        font-family: 'Caveat', cursive;
        font-size: 1.5rem;
        color: #E8A0BF;
        margin-bottom: 0.5rem;
        letter-spacing: 2px;
    }}

    .hero-title {{
        font-family: 'Fraunces', serif;
        font-size: 5.5rem;
        font-weight: 900;
        margin: 0;
        line-height: 1;
        letter-spacing: -0.03em;
        color: #FDF2F0;
        text-shadow: 3px 3px 0 rgba(232, 160, 191, 0.4);
    }}

    .title-accent {{
        color: #E8A0BF;
        font-style: italic;
    }}

    .hero-subtitle {{
        font-family: 'Quicksand', sans-serif;
        font-size: 1.3rem;
        font-weight: 500;
        margin-top: 1rem;
        color: #F5E1DC;
    }}

    .hero-hint {{
        font-family: 'Caveat', cursive;
        font-size: 1.4rem;
        color: #E8A0BF;
        margin-top: 2rem;
        animation: pulse 2s ease-in-out infinite;
    }}

    /* Custom cursor when hovering */
    .hero-mask:hover {{
        cursor: crosshair;
    }}

    @keyframes pulse {{
        0%, 100% {{ opacity: 0.6; }}
        50% {{ opacity: 1; }}
    }}

    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    </style>

    <script>
    (function() {{
        // Wait for DOM to be ready
        function initMask() {{
            const hero = document.getElementById('heroMask');
            const cover = document.getElementById('heroCover');
            if (!hero || !cover) {{
                setTimeout(initMask, 100);
                return;
            }}
            
            const REVEAL_RADIUS = 200;
            
            hero.addEventListener('mousemove', function(e) {{
                const rect = hero.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const maskValue = 'radial-gradient(circle ' + REVEAL_RADIUS + 'px at ' + x + 'px ' + y + 'px, transparent 0%, transparent 55%, black 100%)';
                cover.style.webkitMaskImage = maskValue;
                cover.style.maskImage = maskValue;
            }});
            
            hero.addEventListener('mouseleave', function() {{
                cover.style.webkitMaskImage = 'radial-gradient(circle 0px at 50% 50%, transparent 99%, black 100%)';
                cover.style.maskImage = 'radial-gradient(circle 0px at 50% 50%, transparent 99%, black 100%)';
            }});
        }}
        
        initMask();
    }})();
    </script>
    """
    
    # Use components.html for proper JS execution!
    st.components.v1.html(hero_html, height=500, scrolling=False)