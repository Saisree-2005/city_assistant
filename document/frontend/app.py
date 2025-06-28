import streamlit as st
import requests

st.set_page_config(page_title="Smart City Assistant")
st.title("Smart City Assistant – Summarizer")

backend_url = "http://127.0.0.1:8000"

# Health‑check so the user knows when the backend is ready
try:
    status = requests.get(backend_url).json()["status"]
    st.success(f"Backend status: {status}")
except Exception:
    st.warning("Backend not reachable yet… "
               "Start it with `uvicorn backend.main:app --reload` "
               "or wait until the model finishes loading.")
    st.stop()

input_text = st.text_area("Enter a city report or document:")

if st.button("Summarize"):
    if not input_text.strip():
        st.error("Please paste some text to summarize.")
    else:
        try:
            r = requests.post(f"{backend_url}/summarize",
                              json={"text": input_text})
            r.raise_for_status()
            st.subheader("Summary:")
            st.write(r.json()["summary"])
        except Exception as e:
            st.error(f"Request failed: {e}")
