# ✅ MVP Completion Checklist

## 📦 Modules & Tasks

---

### 🔍 job_search

- [x] Resume parsed into structured fields
- [ ] Resume embedded as vector for profile matching
- [x] Search query auto-generated from resume
- [x] API fallback works (SerpAPI)
- [ ] Scrapers implemented (Lever, Greenhouse, Ashby)
- [x] Ranked results returned based on similarity
- [x] Jobs stored in DB
- [ ] Retry / bot protection handling for scrapers
- [ ] Unit tests for query, match, scraper logic

---

### 🧠 generation

- [x] Tailored cover letter using GPT
- [x] Tailored resume using GPT
- [x] Prompts centralized
- [x] Markdown export
- [ ] PDF export logic verified
- [ ] GPT fallback / retry
- [ ] Test coverage for generation logic

---

### 🤖 autofill

- [x] Text input fields autofilled
- [ ] Radio, dropdowns, and multistep flows handled
- [ ] Resume + cover letter upload
- [ ] Essay prompts sent to GPT and filled
- [x] Field matching (rule + fuzzy + GPT)
- [ ] Final confirmation of submission
- [ ] Batch autofill / CLI entry
- [ ] Autofill result logging
- [ ] Tests with mock forms or headless Playwright

---

### 🗃️ db

- [x] SQLite schema setup with `jobs` and `applications`
- [x] DAO for job + application logic
- [x] Deduplication logic
- [x] Enum support for status
- [ ] Filters for recent apps, status, etc.
- [ ] Support for Supabase (future proof)
- [ ] Better migration/versioning strategy
- [ ] Full test coverage

---

### 🔄 notion

- [x] Push local apps to Notion
- [x] Pull Notion apps into SQLite
- [x] Avoid resyncing unchanged records
- [ ] Error/retry handling on API fail
- [ ] CLI script (e.g., `scripts/sync_notion.py`)
- [ ] Sync tests with mocked Notion API

---

### 📊 UI

- [x] Home view with resume preview
- [x] Tracker view with filters
- [ ] Score badges / progress indicators
- [ ] Edit + update application status from UI
- [ ] Job discovery view
- [ ] Analytics (charts, breakdowns)
- [ ] Sidebar navigation or tabbed views
- [ ] “Apply Now” button (runs full generation → autofill)

---

### 🧩 Miscellaneous

- [x] `scheduler.py` runs sync + query
- [x] Constants file present
- [x] Dashboard file generates visuals
- [ ] Refactor `constants.py` into logical subfiles
- [ ] Add logging across scripts
- [ ] Create CLI runners for key flows
