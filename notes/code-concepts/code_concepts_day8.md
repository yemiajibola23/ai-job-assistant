
# 📘 Code Concepts – Day 8

## `st.session_state`

**What it does**: Persists variables (like sets, lists, flags) between Streamlit reruns  
**When to use it**: To avoid resetting data (e.g., `seen_ids`) every time a user toggles something  
**Example**:
```python
if "seen_ids" not in st.session_state:
    st.session_state.seen_ids = set()
```

---

## `schedule` module

**What it does**: Allows you to run functions at regular intervals using human-readable syntax  
**When to use it**: For polling jobs, alerts, or refreshing background tasks  
**Example from today**:
```python
schedule.every(5).seconds.do(lambda: run_scheduler_job(...))
```

---

## Lambda as a deferred function

**What it does**: Wraps function calls so they're not executed immediately  
**When to use it**: When scheduling or passing a function that takes arguments  
**Example**:
```python
schedule.every(10).seconds.do(lambda: run_scheduler_job(fetcher, handler, seen_ids))
```

---

## Using stubs in tests

**What it does**: Simulates external functions in unit tests  
**When to use it**: To test logic that depends on inputs or side effects without using mocks  
**Example**:
```python
flags = {"called": False}
def fake_handler(_): flags["called"] = True
```
