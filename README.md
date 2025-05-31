# 🤖 AI Job Application Assistant

An intelligent assistant to help you automate job discovery, tailor your resume and cover letters, auto-fill applications, and track your progress — all in one streamlined dashboard.

---

## 🔍 Features

- 🔎 **Job Search**: Pull listings from APIs like SerpAPI or RapidAPI
- 📄 **Resume Parsing**: Extract structured data from your resume
- 🤝 **Job Matching**: Match jobs to your skills using AI embeddings
- ✍️ **Cover Letter Generation**: Auto-write tailored letters using GPT
- 🧠 **Application Autofill**: Use Playwright to auto-fill job forms
- 🗂 **Tracker & Alerts**: Log applications and get notified of new matches
- 📊 **Dashboard**: View your status and progress via Streamlit
- 🔄 **Notion Sync**: Push application data into your Notion workspace

---

## ⚙️ Tech Stack

| Category       | Tools                              |
| -------------- | ---------------------------------- |
| Language       | Python 3.10+                       |
| AI/ML          | OpenAI GPT-4, SentenceTransformers |
| Job APIs       | SerpAPI, RapidAPI                  |
| Resume Parsing | PyMuPDF, pdfplumber                |
| Browser Bot    | Playwright or Selenium             |
| Storage        | SQLite or Supabase                 |
| UI             | Streamlit                          |
| Syncing        | Notion API                         |
| Automation     | cron, watchdog, schedule           |

---

## 🛠 Local Setup

```bash
git clone https://github.com/yourname/ai-job-assistant.git
cd ai-job-assistant
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```
OPENAI_API_KEY=your-key
SERPAPI_KEY=your-key
NOTION_TOKEN=your-token
NOTION_DB_ID=your-db-id
```

Then launch the Streamlit app:

```bash
streamlit run app/main.py
```

---

## 🧩 Project Structure

```
app/          # Streamlit UI
backend/      # Core logic modules
scripts/      # Scheduled jobs and CLI tools
```

---

## 🧭 Roadmap

Check `SSOT.md` and `curriculum.md` for day-by-day goals and architecture.
