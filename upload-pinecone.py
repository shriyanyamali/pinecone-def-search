import os
import json
from tqdm import tqdm

import openai
from pinecone.pinecone import Pinecone
from pinecone.db_control.models.serverless_spec import ServerlessSpec

OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME       = os.getenv("PINECONE_INDEX", "verdictr-semantic")

EMBED_MODEL      = "text-embedding-3-small"
EMBED_DIM        = 1536

openai.api_key = OPENAI_API_KEY
pc = Pinecone(api_key=PINECONE_API_KEY)

pc.create_index(
    name=INDEX_NAME,
    dimension=EMBED_DIM,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)
print(f"Created index: {INDEX_NAME} ({EMBED_DIM} dims)")

index = pc.Index(INDEX_NAME)

with open("database.json", encoding="utf-8") as f:
    data = json.load(f)

BATCH_SIZE = 100
for offset in range(0, len(data), BATCH_SIZE):
    batch = data[offset : offset + BATCH_SIZE]
    texts = [f"{item.get('topic','')}. {item.get('text','')}" for item in batch]

    resp = openai.embeddings.create(model=EMBED_MODEL, input=texts)
    embs = [record.embedding for record in resp.data]

    vectors = []
    for i, item in enumerate(batch):
        idx = offset + i
        vectors.append({
            "id": f"item-{idx}",
            "values": embs[i],
            "metadata": {
                "case_number": item.get("case_number",""),
                "year":        item.get("year",""),
                "policy_area": item.get("policy_area",""),
                "link":        item.get("link",""),
                "topic":       item.get("topic",""),
                "text":        item.get("text","")
            }
        })

    index.upsert(vectors=vectors)
    print(f"Upserted items {offset}–{offset+len(batch)-1}")

print("All data embedded with OpenAI and uploaded to Pinecone.")