import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.services.rag_service import generate_answer

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2,
    max_tokens=600,
)

def _run_agent(system_prompt: str, user_message: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    chain = prompt | llm
    response = chain.invoke({"input": user_message})
    return response.content


def run_crew(question: str, resume_text: str) -> dict:
    # Step 1: RAG — get resume context
    rag_context = generate_answer(question)

    # Agent 1: Researcher
    research_output = _run_agent(
        system_prompt="You are an expert resume analyst. Given an interview question and resume context, summarize the most relevant experience, skills, and projects the candidate should highlight.",
        user_message=f"Interview question: {question}\n\nResume context:\n{rag_context}\n\nSummarize the most relevant points."
    )

    # Agent 2: Answer Writer
    answer_output = _run_agent(
        system_prompt="You are a professional interview coach. Write a compelling first-person interview answer using the STAR method. Be specific, reference real experience, keep it 150-200 words.",
        user_message=f"Interview question: {question}\n\nResearch summary:\n{research_output}\n\nWrite the answer."
    )

    # Agent 3: Critic
    critic_output = _run_agent(
        system_prompt="You are a senior hiring manager evaluating interview answers. Score the answer 1-10 and give one concrete improvement suggestion. Respond ONLY in this format:\nSCORE: <number>/10\nFEEDBACK: <one sentence>",
        user_message=f"Interview question: {question}\n\nAnswer to evaluate:\n{answer_output}"
    )

    # Parse critic output
    score = "N/A"
    feedback = "N/A"
    for line in critic_output.splitlines():
        if line.startswith("SCORE:"):
            score = line.replace("SCORE:", "").strip()
        elif line.startswith("FEEDBACK:"):
            feedback = line.replace("FEEDBACK:", "").strip()

    return {
        "answer": answer_output,
        "score": score,
        "feedback": feedback
    }