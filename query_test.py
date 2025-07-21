import os
from dotenv import load_dotenv
import openai
from pinecone.pinecone import Pinecone

load_dotenv()

OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME       = os.getenv("PINECONE_INDEX")
QUERY_TEXT       = os.getenv("QUERY_TEXT", "energy market")
EMBED_MODEL      = "text-embedding-3-small"

openai.api_key = OPENAI_API_KEY
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

resp = openai.embeddings.create(
    model=EMBED_MODEL,
    input=QUERY_TEXT
)
query_vector = resp.data[0].embedding

out = index.query(
    vector=query_vector,
    top_k=5,
    include_metadata=True
)

print(f"Top 5 results for “{QUERY_TEXT}”:")
for match in out.matches:
    md = match.metadata
    print(f"- [{match.score:.3f}] {md['case_number']} ({md['year']}): {md['topic']}")