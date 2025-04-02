# TODO 4: Implement the KnowledgeManager class
class KnowledgeManager:
    def __init__(self):
        self.knowledge_base = {}

    def add_knowledge(self, key: str, value: str):
        self.knowledge_base[key] = value

    def get_knowledge(self, key: str) -> str:
        return self.knowledge_base.get(key, "")

    def get_all_knowledge(self):
         return self.knowledge_base

knowledge_manager = KnowledgeManager()
