import os
import requests
import streamlit as st
from dotenv import load_dotenv

from utils.document_generator import format_docx, format_pdf, format_txt, sanitize_text

load_dotenv()

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")

API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.markdown(
    """
    <style>
    .main-title {text-align:center; font-size:42px; font-weight:700;}
    .subtitle {text-align:center; color:#777; margin-bottom:25px;}
    .preview {
        background:#111827; color:#f9fafb; padding:24px; border-radius:12px;
        white-space:pre-wrap; max-height:600px; overflow-y:auto;
        border:1px solid #374151;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Generator</div>',
    unsafe_allow_html=True,
)

with st.form("legal_form"):
    col1, col2 = st.columns(2)

    with col1:
        document_type = st.text_input(
            "Document Type",
            placeholder="e.g. Employment Contract, NDA, Lease Agreement",
        )
        parties = st.text_area(
            "Parties Involved",
            placeholder="e.g. Jane Doe (Employee), ABC Corp (Employer)",
            height=120,
        )

    with col2:
        dates = st.text_input(
            "Effective Date",
            placeholder="e.g. October 10, 2026",
        )
        terms = st.text_area(
            "Terms & Conditions",
            placeholder="Separate each clause using a semicolon (;)",
            height=120,
        )

    submitted = st.form_submit_button("Generate Document", use_container_width=True)

if submitted:
    if not all([document_type.strip(), parties.strip(), terms.strip(), dates.strip()]):
        st.error("Please fill in all fields.")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates,
        }

        try:
            with st.spinner("Generating your legal document..."):
                response = requests.post(
                    f"{API_URL}/generate",
                    json=payload,
                    timeout=120,
                )
            response.raise_for_status()
            data = response.json()
            st.session_state["generated_text"] = data["document"]
            st.session_state["document_type"] = document_type
            st.success("Document generated successfully.")
        except requests.RequestException as exc:
            st.error(
                "Could not connect to the FastAPI backend. "
                "Make sure the backend is running on http://127.0.0.1:8000."
            )
            st.caption(str(exc))

if "generated_text" in st.session_state:
    st.subheader("Document Generated")

    if "edited_text" not in st.session_state:
        st.session_state["edited_text"] = st.session_state["generated_text"]

    preview = st.session_state["edited_text"]
    st.markdown(
        f'<div class="preview">{sanitize_text(preview)}</div>',
        unsafe_allow_html=True,
    )

    if st.button("Click to Edit Document"):
        st.session_state["editing"] = True

    if st.session_state.get("editing", False):
        edited = st.text_area(
            "Edit Document",
            value=st.session_state["edited_text"],
            height=500,
        )
        if st.button("Save Edits"):
            st.session_state["edited_text"] = edited
            st.session_state["editing"] = False
            st.rerun()

    st.subheader("Download / Save")
    final_text = st.session_state["edited_text"]
    doc_type = st.session_state.get("document_type", "Legal Document")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button(
            "Download TXT",
            data=format_txt(final_text),
            file_name="LegalEase_Document.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with c2:
        st.download_button(
            "Download DOCX",
            data=format_docx(final_text, doc_type),
            file_name="LegalEase_Document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with c3:
        st.download_button(
            "Download PDF",
            data=format_pdf(final_text, doc_type),
            file_name="LegalEase_Document.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

st.divider()
st.caption(
    "LegalEase is an AI-assisted drafting tool. Generated content should be "
    "reviewed by a qualified legal professional before legal use."
)
