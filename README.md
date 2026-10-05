# LegalEase: AI-Powered Legal Document Generator

LegalEase is an AI-powered application for generating structured legal-document drafts from user-provided information.

## Features

- Employment contracts
- Lease agreements
- NDAs
- General agreements and contracts
- Editable document preview
- TXT, DOCX and PDF downloads
- Streamlit frontend
- FastAPI backend
- Google Gemini AI integration

## Technology Stack

- Python 3.10+
- Streamlit
- FastAPI
- Uvicorn
- Google Gemini API
- python-docx
- FPDF
- Pillow
- Requests
- python-dotenv

## Project Structure

```text
LegalEase/
├── app.py
├── main.py
├── routes.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
└── utils/
    ├── __init__.py
    └── document_generator.py
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create `.env`

Copy `.env.example` to `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
BACKEND_URL=http://127.0.0.1:8000
```

**Never upload your real `.env` file or API key to GitHub.**

### 3. Start the FastAPI backend

```bash
uvicorn main:app --reload
```

### 4. Start the Streamlit frontend

Open another terminal and run:

```bash
streamlit run app.py
```

## Workflow

1. Enter the document type.
2. Enter the parties involved.
3. Enter the terms and conditions, separated with semicolons.
4. Enter the effective date.
5. Click **Generate Document**.
6. Preview and edit the generated content.
7. Download it as TXT, DOCX or PDF.

## API

### `GET /`

Health check for the backend.

### `POST /generate`

Example JSON:

```json
{
  "document_type": "Non-Disclosure Agreement",
  "parties": "Jane Doe (Disclosing Party), ABC Corp (Receiving Party)",
  "terms": "Confidential information must be protected; Disclosure is prohibited without permission",
  "dates": "October 10, 2026"
}
```

## Important Note

LegalEase is an AI-assisted drafting tool. Generated content should be carefully reviewed and, where appropriate, verified by a qualified legal professional before use.

## Project Documentation

The project report can be added to this repository as `LegalEase.pdf`.
