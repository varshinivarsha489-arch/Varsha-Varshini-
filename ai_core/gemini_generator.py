import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class GeminiDocumentGenerator:
    """Generate structured legal documents with Google's Gemini API."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. Add it to your .env file."
            )

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def generate_document(self, document_type, parties, terms, dates):
        clauses = [
            clause.strip()
            for clause in terms.split(";")
            if clause.strip()
        ]

        prompt = f"""
Create a professional draft of a {document_type}.

Document type:
{document_type}

Parties involved:
{parties}

Effective date:
{dates}

Terms and conditions:
{chr(10).join(f"- {c}" for c in clauses)}

Instructions:
- Produce a clear, structured legal-document draft.
- Use formal and professional language.
- Include a title.
- Identify the parties and effective date.
- Organize clauses with clear headings where appropriate.
- Include the supplied terms without inventing specific facts.
- Include signature sections for the relevant parties.
- Do not claim that the document is legal advice.
- Return plain text only, without Markdown code fences.
"""

        response = self.model.generate_content(prompt)

        if not response or not getattr(response, "text", None):
            raise RuntimeError("Gemini returned an empty response.")

        return response.text.strip()
