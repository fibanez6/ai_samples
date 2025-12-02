import os

import chromadb
import rich
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

from agents.openAIClient import OpenAIClient
from utils.openAI_print_utils import print_agent_messages, print_agent_response

load_dotenv(override=True)

# Initialize Agent Client
agent = OpenAIClient()

# -----------------------------
# 1. Setup Embedding Function
# -----------------------------
# We define this FIRST so we can pass it to the collection
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.environ.get("OPENAI_API_KEY"),
    model_name="text-embedding-3-small",
)

current_dir = os.path.dirname(os.path.abspath(__file__))

# -----------------------------
# 2. Setup Chroma vector store
# -----------------------------
chroma_client = chromadb.PersistentClient(path=os.path.join(current_dir, "chroma_db"))

# This ensures queries are embedded using the same model as the documents.
collection = chroma_client.get_or_create_collection(
    name="docs_collection", embedding_function=openai_ef
)

# -----------------------------
# 3. Add documents
# -----------------------------
docs = [
    {
        "id": "1",
        "text": "Python is a programming language that emphasizes readability.",
    },
    {
        "id": "2",
        "text": "OpenAI provides powerful LLM APIs for text generation and embeddings.",
    },
    {
        "id": "3",
        "text": "RAG pipelines combine retrieval and generation for more accurate answers.",
    },
]

# Chroma uses the 'openai_ef' defined in the collection to do it automatically.
collection.upsert(  # 'upsert' is safer than 'add' (prevents duplicate ID errors)
    documents=[doc["text"] for doc in docs], ids=[doc["id"] for doc in docs]
)


# -----------------------------
# 4. RAG Functions
# -----------------------------
def retrieve(query, top_k=2):
    results = collection.query(
        query_texts=[query], n_results=top_k  # Chroma embeds this automatically now
    )
    # Returns a list of list of strings, so we grab the first list
    return results["documents"][0]


def rag_answer(query):
    # 1. Retrieve relevant docs
    retrieved_docs = retrieve(query)

    # 2. Build prompt
    context_text = "\n\n".join(retrieved_docs)

    system_prompt = "You are a helpful AI assistant."
    user_prompt = f"""Answer the question based ONLY on the following context:
    
    Context:
    {context_text}

    Question: 
    {query}
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    panel_title = (
        f"RAG Basic - (Agent: {agent.name.upper()} - Model: {agent.model.upper()})"
    )

    print_agent_messages(messages, title=panel_title)
    rich.print(messages)

    # 3. Generate response
    agent_response = agent.chat_completion_parse(
        model=agent.model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    print_agent_response(agent_response)

    return agent_response.choices[0].message.content


# -----------------------------
# Test RAG
# -----------------------------
if __name__ == "__main__":
    query_text = "What is RAG in AI?"
    answer = rag_answer(query_text)

    print("-" * 30)
    print(f"Query: {query_text}")
    print(f"Retrieved Context: {retrieve(query_text)}")
    print("-" * 30)
    print(f"Answer: {answer}")
