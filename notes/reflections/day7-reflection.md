# 📝 Day 7 Reflection

**Date:** 2025-06-05  
**Status:** ✅ Completed  
**Focus:** Streamlit Dashboard + DB Refactor + Enum Integration

---

### 1. What was the most challenging part of today’s work?

The most challenging part of the day was refactoring the db usage. I was striving to keep the code testable through DI.

---

### 2. What was the most satisfying part?

The most satisfying part was being in complete flow in our pair + TDD methodology. I learned a lot and I never felt lost until the hairy refactor but even then it was not bad.

---

### 3. What concept(s) do you feel more confident in now?

I feel more confident about db connections and how to use them.

---

### 4. What was confusing, surprising, or unexpected?

The most confusing part wrapping my head around the changes we were making to the db usage. I struggled understanding which db was used where I think.

---

### 5. Tech Debt Logged

- [x] ✅ Ensure all `INSERT` statements include `updated_at` if no default is set
- [x] ✅ Confirmed explicit DB injection to avoid global `DEFAULT_DB_PATH` state leakage
