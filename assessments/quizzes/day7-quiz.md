# 📚 Day 7 Quiz – Streamlit Dashboard + DB Refactor

---

### 1. True/False: SQLite columns must be explicitly declared as `NOT NULL` to reject nulls during insert.  
**✅ Correct Answer:** False  
**🧠 Explanation:** SQLite allows `NULL` unless explicitly marked as `NOT NULL`.

---

### 2. What’s one reason your test might return no rows from a query even after inserting valid-looking data?  
**✅ Correct Answer:** A column may be left out (like `updated_at`) or contain null values that impact queries or sorting.  

---

### 3. In TDD, what are the three key phases we cycle through?  
**✅ Correct Answer:** Red → Green → Refactor  

---

### 4. You’re seeing data from a different test leak into your test. What’s a likely cause?  
**✅ Correct Answer:** Shared global state or resource — e.g., setting a global DB path like `DEFAULT_DB_PATH` that isn't reset between tests.  

---

### 5. How do you ensure test isolation when working with an in-memory SQLite database?  
**✅ Correct Answer:** Use `:memory:` DBs and inject the same connection into all dependent functions. Optionally clear data or reset schema if needed.  

---

**✅ Score: 5 / 5**
