# ✅ MVP Completion Checklist

## 📦 Modules & Tasks

---

### 🔍 job_search

- [x] Resume parsed into structured fields
- [x] Resume embedded as vector for profile matching
- [x] Search query auto-generated from resume
- [x] API fallback works (SerpAPI)
- [x] Ranked results returned based on similarity
- [x] Jobs stored in DB
- [ ] Unit tests for query, match, scraper logic

---

### 🧠 generation

- [x] Tailored cover letter using GPT
- [x] Tailored resume using GPT
- [x] Prompts centralized
- [x] Markdown export
- [x] PDF export logic verified
- [ ] GPT fallback / retry
- [ ] Test coverage for generation logic

---

### 🤖 autofill

- [x] Text input fields autofilled
- [x] Radio, dropdowns, and multistep flows handled
- [x] Resume + cover letter upload
- [x] Essay prompts sent to GPT and filled
- [x] Field matching (rule + fuzzy + GPT)
- [x] Final confirmation of submission
- [ ] Batch autofill / CLI entry
- [x] Autofill result logging
- [ ] Tests with mock forms or headless Playwright

#### 🔄 ATS-Specific Autofillers (Greenhouse First)
- [ ] Create `BaseAutofiller` class with shared interface
- [ ] Build `GreenhouseAutofiller` with multistep + upload logic
- [ ] Implement `autofill_router.py` to select autofiller based on URL
- [ ] Refactor current Playwright logic to delegate to selected autofiller
- [ ] Write unit tests for `GreenhouseAutofiller` using mock Playwright page
- [ ] Log ATS name + autofill strategy used (for future debugging)
- [ ] Add placeholder files for Lever, Ashby with `NotImplementedError`

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
