from core.config import get_settings

settings = get_settings()

def _mock_document(document_type, party_a, party_b, effective_date, terms):
    return f'''# {document_type}

## Agreement

This {document_type} is entered into between:

**First Party:** {party_a}

**Second Party:** {party_b}

**Effective Date:** {effective_date}

## 1. Purpose

The parties agree to enter into this agreement for the purpose described
by the terms provided below.

## 2. Key Terms

{terms}

## 3. General Provisions

The parties agree to act in good faith and comply with the obligations
set out in this agreement.

## 4. Confidentiality

Where applicable, confidential information shared between the parties
should be protected and used only for the agreed purpose.

## 5. Termination

The parties may terminate this agreement according to mutually agreed
written terms.

## 6. Signatures

First Party: {party_a}

Signature: __________________________

Date: ______________________________


Second Party: {party_b}

Signature: __________________________

Date: ______________________________
'''

def _build_prompt(document_type, party_a, party_b, effective_date, terms):
    return f'''You are an AI legal-document drafting assistant.

Create a professional draft of the following document.

Document type: {document_type}
First party: {party_a}
Second party: {party_b}
Effective date: {effective_date}
User-provided terms:
{terms}

Instructions:
1. Create a clear, professional legal-document draft.
2. Do not invent material facts, addresses, amounts, dates, obligations, laws, or other details not provided.
3. Use [INSERT INFORMATION] for important missing information.
4. Preserve the meaning of the user's terms.
5. Use numbered sections and useful headings.
6. Include signature blocks where appropriate.
7. Make the document easy to edit.
8. Do not claim jurisdiction-specific legal validity.
9. Do not fabricate legal citations.
10. Return only the document draft.
'''

def generate_document(document_type, party_a, party_b, effective_date, terms):
    document_type, party_a, party_b, effective_date, terms = (
        document_type.strip(), party_a.strip(), party_b.strip(),
        effective_date.strip(), terms.strip()
    )
    if not document_type:
        raise ValueError("Document type is required.")
    if not party_a:
        raise ValueError("First party is required.")
    if not party_b:
        raise ValueError("Second party is required.")
    if not terms:
        raise ValueError("Key terms are required.")

    if settings.mock_mode:
        return _mock_document(document_type, party_a, party_b, effective_date, terms)

    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is missing. Add it to .env or enable MOCK_MODE.")

    try:
        from google import genai
        client = genai.Client(api_key=settings.gemini_api_key)
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=_build_prompt(document_type, party_a, party_b, effective_date, terms),
        )
        generated_text = getattr(response, "text", None)
        if not generated_text:
            raise RuntimeError("Gemini returned an empty response.")
        return generated_text.strip()[:settings.max_document_chars]
    except Exception as exc:
        raise RuntimeError(f"Gemini generation failed: {exc}") from exc
