# 🐻 BearDiary AI

> Your cozy AI journal companion 🎀📔

BearDiary AI is a warm, whimsical journaling app built with Streamlit. It helps you write honestly, reflect on your emotions, and receive a gentle AI-generated comfort letter from your digital companion, BearBestie.

Made with 🧸 by Vivi

---

## ✨ Features

- 🪄 Magical mask-reveal hero experience
- 🕰️ Working vintage analog clock with a teddy-bear theme
- 📝 AI-powered journal analysis using Groq and Llama 3.3 70B
- 💌 Personalized comfort letters and affirmations
- 📅 A beautiful timeline of past journal entries
- 🌸 Mood garden analytics with Plotly charts and achievements
- 🏆 Badge-based journaling rewards
- 🎀 A cozy multi-page experience with a scrapbook-inspired design
- 💾 Persistent storage with SQLite

---

## 🎨 Design Theme

BearDiary AI follows a cozy “Teddy Plaid” aesthetic inspired by:

- Cream, blush pink, dusty rose, warm brown, and deep chocolate
- Fraunces, Quicksand, and Caveat fonts
- Vintage scrapbook + cottagecore + café vibes
- Rounded sticker badges, plaid textures, and soft mood dots

---

## 🛠️ Tech Stack

- Python 3.11
- Streamlit for the multi-page UI
- Groq API with Llama 3.3 70B
- SQLite for local data storage
- Plotly for mood visualizations
- Custom CSS for the full design system

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/bistighosh16/beardiary-ai.git
cd beardiary-ai
```

### 2. Create a virtual environment

```bash
py -3.11 -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

You can get a free API key from [Groq Console](https://console.groq.com).

### 5. Run the app

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## 📁 Project Structure

```text
beardiary-ai/
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── assets/
├── pages/
│   ├── 1_📝_Write.py
│   ├── 2_📅_My_Diary.py
│   └── 3_🌸_Mood_Garden.py
└── utils/
    ├── ai.py
    ├── database.py
    ├── hero.py
    ├── sidebar.py
    └── styles.py
```

---

## 🎯 How It Works

1. Write a journal entry on the Write page.
2. BearBestie analyzes your mood and creates:
   - a detected mood
   - a cozy vibe word for the day
   - a warm comfort letter
   - a personalized affirmation
3. Your entry is saved in SQLite with the AI-generated metadata.
4. The My Diary page shows your timeline of entries.
5. The Mood Garden page visualizes your emotional patterns over time.

---

## 🐻 About BearBestie

BearBestie is the heart of the app: gentle, supportive, and non-judgmental. The experience is designed to feel like journaling with a soft, caring friend who helps you reflect without pressure.

---

## 🌐 Live Demo

A live demo link will be added once the app is deployed.

---

## 📄 License

This project is licensed under the MIT License.

---

## 💌 Connect

- GitHub: [@bistighosh16](https://github.com/bistighosh16)
- LinkedIn: https://www.linkedin.com/in/bisti-ghosh-660488387/

---

Your cozy corner of the internet ✨

Made with 🧸 by Vivi
