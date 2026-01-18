import os
from dotenv import load_dotenv

load_dotenv()


def build_prompt(context_chunks, question):
    context = "\n\n".join(context_chunks)

    print("context_retrieved", context)

    return f"""
You are an AI assistant helping answer user questions by extracting and inferring information from internal email communications.

You are given a set of email excerpts retrieved based on semantic similarity to the user's question.

Instructions:
- The context consists of email subjects and email body content.
- Use ONLY the information present in the context.
- You MAY make reasonable inferences that a human reader would naturally make from emails
  (e.g., project status, progress, blockers, next steps, intent).
- Do NOT introduce facts that are not supported or implied by the context.
- Do NOT say "I don't know" if the context is clearly related to the question.
- If the context is relevant but incomplete, explain what can be inferred and state any limitations.
- Say "I don't know" ONLY if the context is completely unrelated to the question.

Context (email excerpts):
{context}

User Question:
{question}

Answer:
- Provide a concise, clear answer.
- Prefer summarization over quotation.
- If multiple emails say similar things, synthesize them into a single coherent response.
"""

def generate_answer(context_chunks, question):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "GIVE_API_KEY":
        return ask_for_api_key(context_chunks, question)

    return call_openai(api_key, context_chunks, question)


def ask_for_api_key(context_chunks, question):
    print("\n⚠️ OpenAI API key not found.")
    user_key = input("Please enter your OpenAI API key (or press Enter to skip): ").strip()

    if not user_key:
        return (
            "LLM step skipped because no API key was provided.\n\n"
            "The retrieved context contains the information needed to answer the question."
        )

    return call_openai(user_key, context_chunks, question)


def call_openai(api_key, context_chunks, question):
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    prompt = build_prompt(context_chunks, question)

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # safe + cheap
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()
