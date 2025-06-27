# 🧹 Tech Debt Tracker

## Pending Cleanup & Improvements

- [ ] Fix VSCode shell and venv issues (e.g. terminal stuck reactivating, read-only config)
- [ ] Schedule tracker module refactor review before polish phase (around Day 10)
- [ ] Revisit and improve general code organization and cleanup post-CRUD

- [ ] 🔍 **Improve `parse_query()` job title extraction using ML or NLP**
  - Replace fragile keyword matching with a more flexible approach
  - Options:
    - spaCy `en_core_web_trf` with enhanced NER
    - HuggingFace zero-shot classification
    - GPT-4 fallback (cost-aware)
  - Goal: Extract titles like "ML engineer", "full stack developer", "software architect" without hardcoding
  - Estimated Time: 1.5–2 hrs
  - Priority: Medium – not blocking current flow but valuable for production
  - Tags: `nlp`, `job parsing`, `title extraction`, `ml-upgrade`

- [ ] Refactor app_db.py to support full dependency injection and testability for all functions (not just update_application_status_and_notes)
- [ ] Move `RESUME_FIELD_MAP` from `autofill.py` to `constants.py` for reuse across modules
- [ ] Log unmapped `resume_field` keys returned by GPT in `call_gpt_function` for visibility and debugging
- [ ] Add fallback handling for GPT fields not present in resume (e.g. cover letter text or derived summary)
- [ ] Consider caching GPT mapping responses per domain to reduce API calls
- [ ] Add unit tests for `autofill_application()` and `call_gpt_function()` with mock form input

- [ ] 📁 **Organize tests into logical subfolders and layers**
  - Separate `unit/` and `integration/` tests for clarity and CI targeting
  - Move Notion integration test to `tests/integration/test_notion_sync.py`
  - Consider subfolders per domain (e.g. `notion`, `db`, `matching`)
  - Add `__init__.py` to make test folders import-safe
  - Optionally: Add `conftest.py` for shared fixtures or cleanup hooks
  - Estimated Time: 1 hr
  - Priority: Medium – improves structure and future test scaling
  - Tags: `testing`, `structure`, `refactor`, `integration`



