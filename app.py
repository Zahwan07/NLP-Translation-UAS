# app.py
# Enhanced English <-> Indonesian Translation App using Streamlit

import logging
import streamlit as st
from transformers import pipeline

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="EN ↔ ID Translator",
    page_icon="🌐",
    layout="centered",
)

st.title("🌐 English ↔ Indonesian Translator")
st.write("Simple Machine Translation demo using Hugging Face + Streamlit")

# ---------------------------
# Load Models (Cached)
# ---------------------------
@st.cache_resource
def load_models():
    logging.info("Loading translation models")
    en_id = pipeline("translation", model="Helsinki-NLP/opus-mt-en-id")
    id_en = pipeline("translation", model="Helsinki-NLP/opus-mt-id-en")
    return en_id, id_en

en_id_translator, id_en_translator = load_models()

# ---------------------------
# UI Components
# ---------------------------
col1, col2 = st.columns([3, 1])

with col1:
    direction = st.selectbox(
        "Translation Direction",
        ("English → Indonesian", "Indonesian → English"),
    )

with col2:
    if st.button("Swap"):
        if "direction" in st.session_state:
            st.session_state.direction = (
                "Indonesian → English"
                if st.session_state.direction == "English → Indonesian"
                else "English → Indonesian"
            )

if "direction" not in st.session_state:
    st.session_state.direction = direction

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

input_text = st.text_area(
    "Input Text",
    value=st.session_state.input_text,
    placeholder="Type your sentence here...",
    height=180,
    key="input_text",
)

col_a, col_b = st.columns(2)
with col_a:
    translate_btn = st.button("Translate")
with col_b:
    if st.button("Clear"):
        st.session_state.input_text = ""
        st.experimental_rerun()

# ---------------------------
# Translation Logic
# ---------------------------
if translate_btn:
    text = input_text or ""
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("Translating..."):
            try:
                if st.session_state.get("direction", direction) == "English → Indonesian":
                    result = en_id_translator(text, max_length=512)
                    model_name = "Helsinki-NLP/opus-mt-en-id"
                else:
                    result = id_en_translator(text, max_length=512)
                    model_name = "Helsinki-NLP/opus-mt-id-en"

                output_text = result[0]["translation_text"]

                st.subheader("Translation Result")
                st.text_area("Output", value=output_text, height=180)

                st.download_button(
                    "Download translation",
                    data=output_text,
                    file_name="translation.txt",
                    mime="text/plain",
                )

                st.caption(f"Model: {model_name}")
            except Exception as e:
                st.error(f"Translation failed: {e}")

# ---------------------------
# Footer + Examples
# ---------------------------
st.markdown("---")
st.caption("Final Project – Machine Translation | Streamlit Demo")

with st.expander("Examples"):
    st.write("Click a sentence to load it into the input box")
    examples_en = [
        "Hello, how are you?",
        "The weather today is sunny and warm.",
        "Machine translation helps break language barriers."
    ]
    examples_id = [
        "Halo, apa kabar?",
        "Cuaca hari ini cerah dan hangat.",
        "Penerjemahan mesin membantu mengatasi hambatan bahasa."
    ]
    for s in examples_en:
        if st.button(s, key=f"ex_en_{s}"):
            st.session_state.input_text = s
            st.experimental_rerun()
    for s in examples_id:
        if st.button(s, key=f"ex_id_{s}"):
            st.session_state.input_text = s
            st.experimental_rerun()
