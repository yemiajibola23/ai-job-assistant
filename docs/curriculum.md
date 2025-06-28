📅 AI Job Assistant Curriculum (Day-by-Day Roadmap)

    This document tracks the daily breakdown of tasks, goals, and deliverables for the AI Job Application Assistant project. Modeled after the Full Stack NBA curriculum.

    ✅ Legend

    🔄 In Progress

    ✅ Completed

    ⬜️ Not Started

    🟩 Week 1: Job Discovery + Resume Matching

    Day 1 – Job API Setup & First Query



    Day 2 – Job Filtering & Database Storage



    Day 3 – Resume Embedding + Job Matching



    Day 4 – Resume Parsing & Structuring



    Day 5 – Cover Letter Generator



    🟥 Week 2: Tracking + Streamlit UI + Automation

    Day 6 – Application Tracker DB



    Day 7 – Streamlit Dashboard



    Day 8 – Scheduler / Watchdog Alerts



    Day 9 – Autofill Setup



    Day 10 – Notion Sync + Polish

🔄 Day 14 – Tracker View

- Display saved jobs from DB in Streamlit
- Include title, company, location, and score
- Filter by score

✅ Day 15 – Application Status & UI Enhancements

- Add editable status (e.g. Interested, Applied, Rejected)
- Use `st.selectbox()` for inline editing
- Add optional notes field

✅ Day 16 – Application Autofill Setup

- Use Playwright to fill demo job forms
- Map resume data to fields
- Add submit confirmation

✅ Day 17 – Auto Query Mode

- Use resume to generate structured query
- Run query → match → save flow with no manual input
- Trigger via button or background sync

✅ Day 18 – Alerts + Watchdog Automation

- Use `watchdog` or `schedule` for timed syncs
- Alert user or log when new jobs are found
- Run `Auto Query Mode` on a loop

✅ Day 19 – Notion Sync (Revisited)

- Push saved jobs (and status) to Notion
- Sync new/updated jobs only
- Reconnect to existing Notion schema

⬜️ Day 20 – Streamlit Polish & UX Flow

- Add tabs/sidebar for views: Query, Tracker, History
- Improve UI layout and spacing
- Add loading spinners and headers

🟨 Week 3: Advanced Job Automation & Data Resilience

✅ Day 21 – Hybrid Job Fetching with Scraper + SerpAPI Fallback

- Implement `scraper_manager.py` to orchestrate job board scrapers (e.g., Lever, Greenhouse)
- Build 1–2 scraper modules and normalize their outputs
- Handle scraper edge cases: bot detection, rate limiting, broken selectors
- Add fallback: use SerpAPI if scraper fails or returns nothing
- Ensure unified job format and error-tolerant flow

⬜️ Day 22 – Infra Cleanup: Schema + Test Init Refactor

- Centralize table creation using `initialize_all_tables(conn)`
- Replace scattered raw `cursor.execute()` calls in tests/scripts
- Ensure test DBs initialize consistently and cleanly
- Optionally prepare for future migration tools (e.g. Alembic)
- Add CLI-friendly DB init hook (optional)

✅ Day 23 – Engine-Agnostic Autofill System + Essay Question Handling

- Build a generic DOM-based autofill engine to parse inputs, dropdowns, checkboxes, and file fields
- Match field labels to internal resume data using heuristics or embeddings
- Detect long-form essay questions and answer them using:
  - User-defined responses
  - Templates with job/resume variables
  - GPT fallback
- Submit forms via Playwright and log submission results
- Scaffold plug-in system for platform-specific enhancements (e.g. Greenhouse, Lever)
- Set up key files: `essay_handler.py`, `field_matcher.py`, `form_interactor.py`

⬜️ Day 24 – Email Inbox Monitor + Status Sync

- Monitor email inbox (e.g. Gmail via IMAP or Gmail API) for new application-related messages
- Parse emails to infer job application outcomes or interview invitations
- Match emails to known applications in DB
- Update application status (e.g. Interviewing, Rejected, Offer) in SQLite + Notion
- Create interview entries in Notion if detected
- Set up core files: `watcher.py`, `parser.py`, `matcher.py`, `status_rules.json`

⬜️ Day 26 – Lever Scraper Implementation

- Use requests or httpx to fetch jobs from Lever job boards
- Parse JSON or HTML structure to extract job listings
- Implement `fetch_jobs(query)` in `lever_scraper.py`
- Normalize output format (title, company, location, url, source)
- Write integration test with mocked page response


⬜️ Day 27 – Ashby Scraper Implementation

- Identify Ashby job board structure and query format
- Use requests + BeautifulSoup to extract listings
- Handle pagination or filters if present
- Implement `fetch_jobs(query)` in `ashby_scraper.py`
- Write integration test for core functionality


⬜️ Day 28 – Greenhouse Scraper Implementation

- Scrape from public Greenhouse-hosted job boards
- Handle embedded JSON or predictable HTML structure
- Implement `fetch_jobs(query)` in `greenhouse_scraper.py`
- Normalize structure and test with fallback logic
- Add edge case handling: expired postings, missing data


  🔁 Ongoing Daily Workflow

🛠️ Note:

- Plan a general tracker refactor checkpoint before the polish phase on Day 10
- Include VSCode terminal fixes in ongoing tech debt review
