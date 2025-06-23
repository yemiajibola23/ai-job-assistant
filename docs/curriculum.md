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

⬜️ Day 15 – Application Status & UI Enhancements

- Add editable status (e.g. Interested, Applied, Rejected)
- Use `st.selectbox()` for inline editing
- Add optional notes field

⬜️ Day 16 – Application Autofill Setup

- Use Playwright to fill demo job forms
- Map resume data to fields
- Add submit confirmation

⬜️ Day 17 – Auto Query Mode

- Use resume to generate structured query
- Run query → match → save flow with no manual input
- Trigger via button or background sync

⬜️ Day 18 – Alerts + Watchdog Automation

- Use `watchdog` or `schedule` for timed syncs
- Alert user or log when new jobs are found
- Run `Auto Query Mode` on a loop

⬜️ Day 19 – Notion Sync (Revisited)

- Push saved jobs (and status) to Notion
- Sync new/updated jobs only
- Reconnect to existing Notion schema

⬜️ Day 20 – Streamlit Polish & UX Flow

- Add tabs/sidebar for views: Query, Tracker, History
- Improve UI layout and spacing
- Add loading spinners and headers

  🔁 Ongoing Daily Workflow

🛠️ Note:

- Plan a general tracker refactor checkpoint before the polish phase on Day 10
- Include VSCode terminal fixes in ongoing tech debt review
