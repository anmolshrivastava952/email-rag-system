import pickle
from sentence_transformers import SentenceTransformer
from retrieval import retrieve_top_k
from generation import generate_answer


INDEX_PATH = "email_index.pkl"


def load_index():
    with open(INDEX_PATH, "rb") as f:
        data = pickle.load(f)

    model = SentenceTransformer(data["model_name"])
    chunks = data["chunks"]

    return model, chunks


def main():
    model, chunks = load_index()

    question = input("\n❓ Enter your question: ").strip()

    retrieved = retrieve_top_k(
        query=question,
        chunks=chunks,
        model=model,
        k=3
    )

    context_chunks = [r["text"] for r in retrieved]

    answer = generate_answer(context_chunks, question)

    print("\n--- ANSWER ---\n")
    print(answer)


if __name__ == "__main__":
    main()
