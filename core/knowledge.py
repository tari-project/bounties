import numpy as np
from typing import List

class KnowledgeBase:
    """
    Self-Learning Knowledge Base using a mock Vector Embedding approach.
    In a real production environment, this would use ChromaDB, FAISS, or Pinecone.
    """
    def __init__(self):
        self.memory = {} # Stores {category: [documents]}
        self.embeddings = {} # Mock embeddings

    def add_knowledge(self, category: str, text: str):
        if category not in self.memory:
            self.memory[category] = []
        self.memory[category].append(text)
        print(f"Learned new info in {category}: {text[:30]}...")

    def query(self, user_input: str) -> str:
        # Simulated semantic search
        # In reality: embed(user_input) -> search vector DB -> retrieve top K
        all_text = " ".join([doc for docs in self.memory.values() for doc in docs])
        if not all_text:
            return "I don't have any knowledge yet. Please teach me!"
        
        # Simple keyword-based mock retrieval for the bounty demo
        for category, docs in self.memory.items():
            for doc in docs:
                if any(word in doc.lower() for word in user_input.lower().split()):
                    return doc
        
        return "I'm not sure about that, but I'm learning. Can you explain it to me?"
