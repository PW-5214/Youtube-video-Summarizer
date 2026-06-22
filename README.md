# 🦜 YouTube + Website Summarizer

A Streamlit web application that summarizes content from:

- ▶️ YouTube videos
- 🌐 Websites

The app extracts transcript/content and generates a concise **pointwise summary (max ~300 words)** using **Groq + LangChain**.

---

## ✨ Features

- Summarize YouTube videos
- Summarize websites
- Supports English and Hindi transcripts
- Automatic fallback to video description if transcript fails
- Clean Streamlit UI
- Uses Groq LLM for fast response generation

---

## 🛠 Tech Stack

- Python
- Streamlit
- LangChain
- Groq API
- YouTube Transcript API
- yt-dlp
- BeautifulSoup

---

## 📂 Project Structure

```bash
youtube-video-summarizer/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

Clone repository:

```bash
git clone https://github.com/YOUR_USERNAME/youtube-video-summarizer.git
```

Move into project:

```bash
cd youtube-video-summarizer
```

Create virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📦 Requirements

```txt
streamlit
validators
python-dotenv

langchain
langchain-community
langchain-core
langchain-groq

beautifulsoup4
lxml

youtube-transcript-api
yt-dlp

unstructured
numexpr
```

---

## 🔑 Get GROQ API Key

1. Open:
   
   :contentReference[oaicite:0]{index=0}

2. Login

3. Generate API Key

4. Copy API Key

---

## ▶️ Run Project

Start application:

```bash
streamlit run app.py
```

Open browser:

```text
http://localhost:8501
```

---

## 🚀 Deployment (Streamlit Cloud)

Push code to GitHub.

Open:

:contentReference[oaicite:1]{index=1}

Steps:

1. Sign in
2. New App
3. Select Repository
4. Select Branch
5. Set `app.py`
6. Deploy

---

## 📖 How It Works

### Website Flow

```text
URL
↓
WebBaseLoader
↓
Extract Content
↓
Groq LLM
↓
Summary
```

### YouTube Flow

```text
Video URL
↓
YoutubeLoader
↓
Transcript
↓
(If unavailable)
↓
yt-dlp Description
↓
Groq LLM
↓
Summary
```

---

## 🧪 Example Input

### YouTube

```text
https://www.youtube.com/watch?v=XXXXXXXXXXX
```

### Website

```text
https://example.com
```

---

## 📷 UI Preview

```text
🦜 Summarize YouTube or Website Content

Enter URL:
[________________]

[Summarize]
```

---

## ⚠️ Limitations

- Some YouTube videos block transcript access
- Private videos are unsupported
- Large websites may take longer
- Depends on GROQ API availability

---

## 🔮 Future Improvements

- PDF summarization
- Multi-language output
- Download summary as PDF
- Chat with summarized content
- Save history

---

## 👨‍💻 Author

Prathmesh Wavhal

Built using Streamlit + LangChain + Groq
