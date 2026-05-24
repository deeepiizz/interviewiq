from openai import OpenAI
from app.config import OPENAI_API_KEY, MODEL_NAME

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are an interview assistant.
Generate a strong, professional, resume-aware answer.
Use the candidate's resume context when relevant.
Prefer STAR format for behavioral questions.
"""

def generate_answer(question: str, context_chunks: list[str]):
    context = "\n\n".join(context_chunks)

    prompt = f"""
Interview Question:
{question}

Candidate Resume Context:
{context}

Return:
1. Best answer
2. Shorter answer
3. Key talking points
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content