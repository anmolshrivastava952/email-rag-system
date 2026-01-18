import numpy as np


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve_top_k(query, chunks, model, k=5):
    query_embedding = model.encode(query, convert_to_numpy=True)

    scores = []
    for chunk in chunks:
        score = cosine_similarity(query_embedding, chunk["embedding"])
        scores.append(score)

    top_k_idx = np.argsort(scores)[::-1][:k]

    results = []
    for idx in top_k_idx:
        results.append({
            "score": scores[idx],
            "text": chunks[idx]["text"],
            "source_file": chunks[idx]["source_file"]
        })

    return results
