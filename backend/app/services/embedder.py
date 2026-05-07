from openai import OpenAI
from app.config import OPENAI_API_KEY, EMBED_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

def get_embeddings(texts: list[str]):
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=texts
    )
    return [item.embedding for item in response.data]