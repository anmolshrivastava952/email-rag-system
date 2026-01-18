import pickle
from sentence_transformers import SentenceTransformer
from preprocessor import preprocess_email_dir


EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMAIL_DIR = "emails/"
OUTPUT_PATH = "email_index.pkl"


def index_emails():
    print("📥 Preprocessing emails...")
    chunks = preprocess_email_dir(EMAIL_DIR)

    print(f"🔢 Generating embeddings using {EMBEDDING_MODEL}...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True)

    for i, emb in enumerate(embeddings):
        chunks[i]["embedding"] = emb

    print(f"💾 Saving index to {OUTPUT_PATH}...")
    with open(OUTPUT_PATH, "wb") as f:
        pickle.dump({
            "model_name": EMBEDDING_MODEL,
            "chunks": chunks
        }, f)

    print(f"✅ Indexed {len(chunks)} chunks successfully")


if __name__ == "__main__":
    index_emails()
