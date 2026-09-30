from datetime import date
import requests
import streamlit as st
from core.config import get_settings
from core.exporters import to_docx, to_pdf, to_txt
from core.text_utils import markdownish_to_html

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")
settings = get_settings()

st.markdown("""<style>
.title{font-size:2.7rem;font-weight:700;margin-bottom:.1rem}
.subtitle{color:#666;font-size:1.05rem;margin-bottom:1.5rem}
.preview{border:1px solid #ddd;border-radius:10px;padding:28px;background:white;min-height:450px;line-height:1.65}
</style>""", unsafe_allow_html=True)

if "document" not in st.session_state:
    st.session_state.document = ""
if "editing" not in st.session_state:
    st.session_state.editing = False

st.markdown('<div class="title">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-assisted legal document drafting and export</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Document Details")
    document_type = st.selectbox("Document Type", [
        "Non-Disclosure Agreement", "Service Agreement", "Employment Agreement",
        "Rental Agreement", "Freelance Agreement", "Business Partnership Agreement",
        "General Legal Agreement"])
    party_a = st.text_input("First Party", placeholder="ABC Technologies Pvt. Ltd.")
    party_b = st.text_input("Second Party", placeholder="John Doe")
    effective_date = st.date_input("Effective Date", value=date.today())
    terms = st.text_area("Key Terms / Requirements", height=180)
    if settings.mock_mode:
        st.warning("MOCK_MODE is enabled. Gemini is not required.")
    else:
        st.success("Gemini AI mode is enabled.")

def generate():
    if not party_a.strip() or not party_b.strip() or not terms.strip():
        st.error("Please complete First Party, Second Party, and Key Terms.")
        return
    payload = {"document_type": document_type, "party_a": party_a.strip(),
               "party_b": party_b.strip(), "effective_date": effective_date.isoformat(),
               "terms": terms.strip()}
    try:
        with st.spinner("Generating document..."):
            response = requests.post(f"{settings.backend_url.rstrip('/')}/generate",
                                     json=payload, timeout=settings.request_timeout_seconds)
        if response.status_code != 200:
            try: detail = response.json().get("detail", response.text)
            except Exception: detail = response.text
            st.error(f"Generation failed ({response.status_code}): {detail}")
            return
        document = response.json().get("document", "").strip()
        if not document:
            st.error("Backend returned an empty document.")
            return
        st.session_state.document = document
        st.session_state.editing = False
        st.success("Document generated successfully.")
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to backend at {settings.backend_url}.")
    except requests.exceptions.Timeout:
        st.error("Backend request timed out.")
    except requests.exceptions.RequestException as exc:
        st.error(f"Request error: {exc}")

st.subheader("1. Create Your Document")
if st.button("Generate Legal Document", type="primary", use_container_width=True):
    generate()

if st.session_state.document:
    st.divider()
    st.subheader("2. Preview & Edit")
    if st.session_state.editing:
        edited = st.text_area("Edit the document", value=st.session_state.document, height=600)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Save Changes", type="primary", use_container_width=True):
                st.session_state.document = edited
                st.session_state.editing = False
                st.rerun()
        with c2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.editing = False
                st.rerun()
    else:
        st.markdown(f'<div class="preview">{markdownish_to_html(st.session_state.document)}</div>', unsafe_allow_html=True)
        if st.button("✏️ Edit Document", use_container_width=True):
            st.session_state.editing = True
            st.rerun()

    st.divider()
    st.subheader("3. Export Document")
    safe_a = "".join(c for c in party_a if c.isalnum() or c in " -_").strip() or "PartyA"
    safe_b = "".join(c for c in party_b if c.isalnum() or c in " -_").strip() or "PartyB"
    base = f"{document_type.replace(' ', '_')}_{safe_a}_{safe_b}"
    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("📄 Download TXT", to_txt(st.session_state.document), f"{base}.txt", "text/plain", use_container_width=True)
    with c2:
        st.download_button("📝 Download DOCX", to_docx(st.session_state.document, document_type), f"{base}.docx",
                           "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
    with c3:
        st.download_button("📕 Download PDF", to_pdf(st.session_state.document, document_type), f"{base}.pdf",
                           "application/pdf", use_container_width=True)

st.divider()
st.caption("LegalEase provides AI-assisted drafting for informational purposes and does not replace professional legal advice.")
