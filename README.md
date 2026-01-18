# 📧 Email RAG System

A Retrieval-Augmented Generation (RAG) system built on top of email data to enable semantic search and question answering over emails.

This project focuses on **high-quality chunking, embedding, and retrieval** so that questions about *people, subjects, and conversations* can be answered accurately.

---

## 🧠 Chunking Strategy

### Fixed Chunk Size

Each email is chunked using a **maximum of 350 words per chunk**. This limit is strictly enforced to balance:

* Semantic completeness
* Embedding quality
* Retrieval precision

We intentionally use **word-based chunking (not token-based)** because emails are typically conversational and sentence-oriented.

**Chunk size used:** `350 words per chunk`

This is implemented directly in code using a rolling word counter that flushes a chunk once the limit is reached.

The effectiveness of any RAG system depends heavily on how the data is chunked. For emails, we apply a **custom chunking strategy** designed specifically for email conversations.

### What we include in each chunk

Each email chunk contains:

* **From** (sender)
* **To** (recipient(s))
* **Subject**
* **Email body (cleaned)**

This ensures that:

* Questions about **specific people** can be answered
* Questions about **specific subjects or threads** can be retrieved
* Context is preserved even when emails are short

### What we remove

* **Salutations and greetings** (e.g., *Hi*, *Hello*, *Dear Team*)

These typically do not carry semantic value and add noise to embeddings. Removing them improves retrieval precision and embedding quality.

---

## 🔍 Embedding Strategy

### Embedding Model Used

We use the following sentence embedding model:

```
sentence-transformers/all-MiniLM-L6-v2
```

**Why this model?**

* Lightweight and fast
* Strong semantic performance for short and medium-length text
* Well-suited for sentence- and paragraph-level embeddings
* Can be run locally without GPU

This model provides an excellent trade-off between **speed, memory usage, and retrieval quality**, making it ideal for email RAG systems.

We generate embeddings for each email chunk and store them locally for fast retrieval.

Why embeddings?

* Enables **semantic search**, not keyword-based search
* Handles paraphrased and natural-language questions
* Works well for unstructured text like emails

The embeddings are stored in a serialized file:

```
email_index.pkl
```

This avoids recomputing embeddings every time the system runs.

---

## 🚀 How to Run the Project

### 1️⃣ Install Dependencies

Install all required packages using:

```bash
pip install -r requirements.txt
```

---

### 2️⃣ Index Emails (Create Embeddings)

To generate embeddings and build the index:

```bash
python index_emails.py
```

📌 **Important notes**:

* If `email_index.pkl` already exists, you **do not need to run this step**
* If you want to **re-embed emails** (for example, after changing the chunking or embedding logic):

  * Delete `email_index.pkl`
  * Re-run `index_emails.py`

---

### 3️⃣ Set OpenAI API Key

Before querying, set your OpenAI API key by doing the change in .env file
---

### 4️⃣ Query Emails

Run the query interface using:

```bash
python query_emails.py
```

This script:

* Loads `email_index.pkl`
* Retrieves the most relevant email chunks
* Uses an LLM to generate a final answer

---

## 🤖 LLM Choice

### Model Used: **gpt-4o-mini**

**Why gpt-4o-mini?**

* ✅ Very low latency
* ✅ Cost-effective for frequent queries
* ✅ Strong reasoning and summarization abilities
* ✅ More than sufficient for answering questions over retrieved email context

Since the RAG pipeline already provides **high-quality, relevant context**, we do not need a very large or expensive model for generation.

This makes the system:

* Faster
* Cheaper
* More production-friendly

---

## 📌 Current Capabilities

* Semantic search over emails
* Questions about:

  * A specific **person**
  * A specific **subject**
  * A specific **conversation context**
* Accurate retrieval due to rich chunk metadata (`from`, `to`, `subject`)

---

## 🔮 Future Improvements

### 1️⃣ Role-Aware Email Retrieval

We can assign **organizational roles** (e.g., Manager, Engineer, HR) to users and support questions like:

* "Show emails between managers and engineers about deployment"
* "What did HR communicate to employees about policy updates?"

This would involve:

* Maintaining a role mapping
* Adding a **pre-query LLM step** to detect role-based intent

---

### 2️⃣ Person-to-Person Email Retrieval

Support queries such as:

* "Show emails between Alice and Bob"
* "What did John tell Sarah about the deadline?"

This is already partially supported because:

* Each chunk includes **from** and **to** metadata

We can further improve this by:

* Using an LLM before retrieval to **extract people/entities** from the question
* Applying structured filters before semantic search

---

### 3️⃣ Smarter Intent Detection

For external users or more complex queries:

* Add an **LLM-based intent classifier** before retrieval
* Decide whether the query is about:

  * People
  * Roles
  * Subjects
  * Time ranges

This would make retrieval more precise and scalable.

---

## ✅ Summary

This project demonstrates how thoughtful chunking and lightweight LLM usage can build a **high-quality, efficient Email RAG system**.

Key strengths:

* Email-specific chunking strategy
* Metadata-rich embeddings
* Cost-effective and fast LLM generation
* Clear path for future enhancements

---

Happy building 🚀
