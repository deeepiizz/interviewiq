import os
import re
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Initialize embedding model (uses Hugging Face Inference API — no local model loading)
embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
)

# Initialize Groq LLM via LangChain
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2,
    max_tokens=500,
)

# Define prompt template (with anti-hallucination rules)
prompt_template = ChatPromptTemplate.from_template("""You are an AI interview coach. The candidate is preparing for an interview. Your job is to write what THEY would say, in first person.

═══════════════════════════════════════════
RESUME CONTEXT (retrieved via RAG):
{context}
═══════════════════════════════════════════

INTERVIEW QUESTION: {question}

═══════════════════════════════════════════
CRITICAL RULES — VIOLATIONS WILL RUIN THE ANSWER:

1. NEVER invent specific numbers (salary, years, percentages, dollar/euro amounts) unless they appear in the resume context.
2. NEVER claim the candidate did research, took courses, attended events, or had experiences not in the resume context.
3. NEVER name specific tools, companies, or technologies the resume context doesn't mention.
4. For SALARY questions: FORBIDDEN to mention any number, range, or currency. Required template: "I'd prefer to discuss compensation after learning more about the role and responsibilities. I'm confident we can find a fair number that reflects market standards and the value I bring." DO NOT add a number.
5. For skills/tech NOT in the resume context: clearly admit no direct experience, then pivot to a related strength.
6. For behavioral questions: only use examples that can be inferred from the resume context. Don't invent stories.
7. Keep it tight: 3-5 sentences, max 7.
8. Confident but humble. No clichés.

═══════════════════════════════════════════
ANSWER (first person, follow ALL rules):""")

# In-memory state for the FAISS vector store
state = {
    "vectorstore": None
}


def sanitize_answer(text: str) -> str:
    """Remove fake numbers, currency, and salary placeholders from AI output."""
    text = re.sub(r"[€$£¥]\s*[\dx,.kKmM]+(\s*(to|-|–|—)\s*[€$£¥]?\s*[\dx,.kKmM]+)?", "[a fair compensation]", text, flags=re.IGNORECASE)
    text = re.sub(r"\b\d{2,3}[,.]?\d{3}\s*(to|-|–|—)\s*\d{2,3}[,.]?\d{3}\b", "[a fair compensation]", text)
    text = re.sub(r"\b[xX]{2,}\b", "[a fair compensation]", text)
    text = re.sub(r"[€$£¥]\s*[xX]+", "[a fair compensation]", text)
    return text


def build_index_from_pdf(pdf_path: str) -> int:
    """LangChain RAG pipeline: load PDF → split → embed → store in FAISS."""
    # 1. Load the PDF using LangChain's PDF loader
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # 2. Split into chunks for better retrieval
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_documents(documents)

    # 3. Embed chunks and store in FAISS vector store
    vectorstore = FAISS.from_documents(chunks, embeddings)
    state["vectorstore"] = vectorstore

    return len(chunks)


def generate_answer(question: str) -> str:
    """Retrieve relevant chunks via FAISS, then prompt the LLM."""
    vectorstore = state.get("vectorstore")

    if vectorstore is None:
        context = "No resume has been uploaded yet."
        print("[RAG DEBUG] No vectorstore — resume not uploaded")
    else:
        # Retrieve top-3 most relevant chunks
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        relevant_docs = retriever.invoke(question)
        print(f"[RAG DEBUG] Question: {question}")
        print(f"[RAG DEBUG] Retrieved {len(relevant_docs)} chunks")
        for i, doc in enumerate(relevant_docs):
            print(f"[RAG DEBUG] Chunk {i+1}: {doc.page_content[:200]}...")
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        print(f"[RAG DEBUG] Total context length: {len(context)} chars")

    # Build the prompt and run the LLM
    chain = prompt_template | llm
    response = chain.invoke({"context": context, "question": question})

    raw_answer = response.content
    return sanitize_answer(raw_answer)