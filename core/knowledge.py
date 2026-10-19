class KnowledgeBase:
    """
    Self-Learning Knowledge Base using a mock Vector Embedding approach.
    In a real production environment, this would use ChromaDB, FAISS, or Pinecone.
    """
    def __init__(self):
        self.memory = {} # Stores {category: [documents]}

    def add_knowledge(self, category: str, text: str):
        if category not in self.memory:
            self.memory[category] = []
        self.memory[category].append(text)
        print(f"Learned new info in {category}: {text[:30]}...")

    def query(self, user_input: str) -> str:
        # Simulated semantic search
        # In reality: embed(user_input) -> search vector DB -> retrieve top K
        if not self.memory:
            return "I don't have any knowledge yet. Please teach me!"
        
        # Improved keyword-based retrieval with basic stop-word filtering
        stop_words = {"the", "is", "at", "which", "on", "and", "a", "an", "of", "to", "in", "for", "with", "it", "that", "this", "of", "el", "la", "los", "las", "un", "una", "y", "o", "en", "de", "con", "por", "para", "que", "es"}
        user_words = [word for word in user_input.lower().split() if word not in stop_words]
        
        if not user_words:
            return "Could you please be more specific?"

        for category, docs in self.memory.items():
            for doc in docs:
                if any(word in doc.lower() for word in user_words):
                    return doc
        
        return "I'm not sure about that, but I'm learning. Can you explain it to me?"
