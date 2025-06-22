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

