# English ↔ Indonesian Translator (Streamlit)

Simple Streamlit app for English ⇄ Indonesian translation using Hugging Face models.

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

If `torch` causes issues, install a CPU or CUDA wheel from PyTorch's site suitable for your system.

## Run

Start the app:

```bash
streamlit run app.py
```

Open the URL printed by Streamlit (usually http://localhost:8501) and use the UI to translate between English and Indonesian. 

## Notes

- Models used: `Helsinki-NLP/opus-mt-en-id` and `Helsinki-NLP/opus-mt-id-en`.
- First run downloads the models (requires internet).
- For offline use, pre-download or cache models in your Hugging Face cache.
