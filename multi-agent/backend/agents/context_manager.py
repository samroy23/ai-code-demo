# TODO 3: Implement the ContextManager class
class ContextManager:
    def __init__(self):
        self.history = []

    def add_interaction(self, interaction: str):
        self.history.append(interaction)

    def get_context(self) -> str:
         return "\n".join(self.history)


