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


- [ ] 🧠 **Add confidence bands to embedding-based matcher**
  - Enhance `FieldMatcher.match()` to return both match key and similarity score
  - Categorize results into confidence levels (`high`, `medium`, `low`)
  - Allow downstream logic (e.g. autofill) to vary behavior based on confidence
  - Log or flag low-confidence matches for review or active learning
  - Consider future UI: display warnings or allow manual override when confidence is low
  - Estimated Time: 1.5–2 hrs
  - Priority: Medium – improves matching safety, debugging, and user feedback
  - Tags: `matching`, `AI`, `autofill`, `refactor`, `future`

  - [ ] 🧪 Improve test coverage across matcher logic paths
  - Add explicit tests for:
    - Pure embedding match (already done ✅)
    - Pure rule match (existing ✅)
    - Fallback to heuristic rules after failed embedding
    - Fallback to fuzzy match (Levenshtein)
  - Include debug assertions if needed to ensure fallbacks are triggering correctly
  - Estimated Time: 30 mins
  - Priority: Medium
  - Tags: `testing`, `matching`, `fallbacks`
  
- [ ] 🔍 Explore resume field type classification (text vs. upload vs. URL)
  - Recognize that some labels (e.g. "Upload your resume") require different handling
  - Design a system to detect or infer expected field type based on label + input type
  - Could involve DOM inspection, label heuristics, or ML classification
  - Estimated Time: 2–3 hrs
  - Priority: High (affects autofill correctness)
  - Tags: `autofill`, `form-intent`, `field-types`