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

- [X] 🧱 **Create `BaseAutofiller` class**
  - Define shared methods like `_fill_fields`, `_extract_label`, `_handle_file_field`
  - Use abstract base class (ABC) or duck typing

- [ ] 🌿 **Implement `GreenhouseAutofiller`**
  - Handle multi-step forms (`Next` button detection)
  - Support essay field detection quirks (some are `<select>`)
  - Smart attach handler (resume/cover letter)
  - Add `_fill_fields()` override with Greenhouse-specific tweaks

- [ ] 🔀 **Create `autofill_router.py`**
  - Inspect page URL and DOM to determine ATS (`Greenhouse`, `Lever`, `Ashby`, etc.)
  - Return corresponding autofiller subclass
  - Fallback to `BaseAutofiller` or raise `NotImplementedError`

- [ ] 🛠️ **Refactor current `PlaywrightAutofiller` to delegate**
  - Replace internal logic with delegation to routed autofiller
  - Keep orchestration logic (e.g. dry run, log aggregation)

- [ ] 🧪 **Write unit tests for `GreenhouseAutofiller`**
  - Use mock Playwright page
  - Validate field matching, essay handling, and attach logic

- [ ] 🪪 **Log ATS name + strategy**
  - Add `ats_name` attribute to autofiller instance
  - Log selected strategy during execution for debugging and analytics

- [ ] 📦 **Add placeholder modules**
  - `LeverAutofiller`, `AshbyAutofiller`, etc.
  - Each should raise `NotImplementedError` in `_fill_fields`

- [ ] 🧠 **Improve essay detection heuristics**
  - Only treat as essay if:
    - Label contains essay-like terms (e.g. "why", "describe", "tell us")
    - AND tag is `textarea` or `contenteditable`
  - Add debug logs when skipping essays misclassified as select

- [ ] 📎 **Support generic attach fields**
  - Detect resume/cover uploads from ambiguous labels
  - Fallback to `_handle_file_field` when attach label logic fails


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
