import os
import re
from pypdf import PdfReader
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# In-memory storage for the current resume text
state = {
    "resume_text": ""
}


def sanitize_answer(text: str) -> str:
    """Remove fake numbers, currency, and salary placeholders from AI output."""
    # Strip any euro/dollar amounts: €50,000 or $50K or £20-30k
    text = re.sub(r"[€$£¥]\s*[\dx,.kKmM]+(\s*(to|-|–|—)\s*[€$£¥]?\s*[\dx,.kKmM]+)?", "[a fair compensation]", text, flags=re.IGNORECASE)
    # Strip salary-range patterns like "50,000 to 60,000"
    text = re.sub(r"\b\d{2,3}[,.]?\d{3}\s*(to|-|–|—)\s*\d{2,3}[,.]?\d{3}\b", "[a fair compensation]", text)
    # Strip "xx", "xxx", "xxxx", etc. (placeholder x's)
    text = re.sub(r"\b[xX]{2,}\b", "[a fair compensation]", text)
    # Catch leftover patterns like "€xxxx" or just "xxxx"
    text = re.sub(r"[€$£¥]\s*[xX]+", "[a fair compensation]", text)
    return text


def extract_text_from_pdf(pdf_path: str) -> str:
    """Read a PDF and return all its text as one string."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def build_index_from_pdf(pdf_path: str) -> int:
    """Extract resume text and store it in memory."""
    text = extract_text_from_pdf(pdf_path)
    state["resume_text"] = text
    return len(text)


def generate_answer(question: str) -> str:
    """Send resume + question to Groq LLM and return the answer."""
    resume_text = state.get("resume_text", "")

    if not resume_text:
        context = "No resume has been uploaded yet."
    else:
        context = resume_text

    prompt = f"""You are an AI interview coach. The candidate is preparing for an interview. Your job is to write what THEY would say, in first person.

═══════════════════════════════════════════
RESUME (the ONLY source of truth):
{context}
═══════════════════════════════════════════

INTERVIEW QUESTION: {question}

═══════════════════════════════════════════
CRITICAL RULES — VIOLATIONS WILL RUIN THE ANSWER:

1. NEVER invent specific numbers (salary figures, years of experience, percentages, dollar/euro amounts) unless they appear in the resume.

2. NEVER claim the candidate did research, took courses, attended events, or had experiences not in the resume.

3. NEVER name specific tools, companies, or technologies the resume doesn't mention.

4. For SALARY questions: FORBIDDEN to mention any number, range, or currency. Required response template: "I'd prefer to discuss compensation after learning more about the role and responsibilities. I'm confident we can find a fair number that reflects market standards and the value I bring." DO NOT deviate. DO NOT add a number.

5. For questions about skills/tech NOT in the resume: clearly admit no direct experience, then pivot to a related strength that IS in the resume.

6. For behavioral questions (failure, challenge, etc.): only use examples that can be inferred from the projects/roles in the resume. Don't invent stories.

7. Keep it tight: 3-5 sentences, max 7. No filler.

8. Confident but humble. No "I'm a quick learner" clichés unless tied to a specific resume detail.

═══════════════════════════════════════════
ANSWER (first person, follow ALL rules above):"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=500,
    )

    raw_answer = response.choices[0].message.content
    return sanitize_answer(raw_answer)