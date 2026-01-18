import os
import re
from typing import List, Dict

OPENING_SALUTATIONS = [
    "hi", "hello", "dear", "good morning", "good afternoon",
    "hi there", "hey", "greetings", "good day"
]

CLOSING_SALUTATIONS = [
    "best regards", "best", "sincerely", "regards", "thanks",
    "thank you", "warm regards", "best wishes", "cheers",
    "take care", "looking forward to your response", "talk soon",
    "all the best", "yours truly", "respectfully", "cordially",
    "with appreciation", "many thanks", "appreciatively",
    "with best regards"
]


def read_email(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    subject = re.search(r"Subject:\s*(.*)", text).group(1).strip()
    sender = re.search(r"From:\s*(.*)", text).group(1).strip()
    receiver = re.search(r"To:\s*(.*)", text).group(1).strip()

    body = text.split("\n\n", 3)[-1].strip()

    return {
        "subject": subject,
        "sender": sender,
        "receiver": receiver,
        "body": body
    }


def remove_salutations(body: str, sender: str, receiver: str) -> str:
    lines = [l.strip() for l in body.splitlines() if l.strip()]

    # remove opening salutation
    first_line = lines[0].lower()
    for sal in OPENING_SALUTATIONS:
        if sal in first_line:
            lines = lines[1:]
            break

    # remove closing salutation + sender name
    cleaned = []
    for line in lines:
        l = line.lower()
        if any(l.startswith(c) for c in CLOSING_SALUTATIONS):
            break
        if sender.lower() in l:
            break
        cleaned.append(line)

    return " ".join(cleaned)


def sentence_split(text: str) -> List[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_sentences(
    sentences: List[str],
    subject: str,
    sender: str,
    receiver: str,
    max_words: int = 350
) -> List[Dict]:

    chunks = []
    current = []
    word_count = 0
    chunk_idx = 0

    for sent in sentences:
        words = sent.split()
        if word_count + len(words) > max_words and current:
            chunk_text = build_chunk_text(
                subject, sender, receiver, " ".join(current)
            )
            chunks.append({
                "chunk_id": chunk_idx,
                "text": chunk_text
            })
            chunk_idx += 1
            current = []
            word_count = 0

        current.append(sent)
        word_count += len(words)

    if current:
        chunk_text = build_chunk_text(
            subject, sender, receiver, " ".join(current)
        )
        chunks.append({
            "chunk_id": chunk_idx,
            "text": chunk_text
        })

    return chunks


def build_chunk_text(subject: str, sender: str, receiver: str, content: str) -> str:
    return f"""Subject: {subject}
From: {sender}
To: {receiver}

Content:
{content}
"""


def preprocess_email_file(path: str) -> List[Dict]:
    email = read_email(path)
    cleaned_body = remove_salutations(
        email["body"], email["sender"], email["receiver"]
    )
    sentences = sentence_split(cleaned_body)
    chunks = chunk_sentences(
        sentences,
        email["subject"],
        email["sender"],
        email["receiver"]
    )
    return chunks


def preprocess_email_dir(email_dir: str) -> List[Dict]:
    all_chunks = []
    for file in os.listdir(email_dir):
        if file.endswith(".txt"):
            path = os.path.join(email_dir, file)
            chunks = preprocess_email_file(path)
            for c in chunks:
                c["source_file"] = file
                all_chunks.append(c)
    return all_chunks
