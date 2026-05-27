# Streamlit placeholder

Streamlit is intentionally disabled in V1.

Reason:

- the CLI pipeline is the source of truth;
- Streamlit must only read produced outputs;
- no scoring logic should live inside the dashboard.

To activate later, rename `app.py.disabled` to `app.py` and add a separate Docker Compose profile.
