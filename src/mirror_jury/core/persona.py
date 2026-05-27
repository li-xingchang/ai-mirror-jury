from dataclasses import dataclass, field


@dataclass
class Persona:
    id: str
    description: str
    source: str = "persona_hub"
    metadata: dict = field(default_factory=dict)

    def to_system_prompt(self) -> str:
        return (
            f"You are the following person:\n\n{self.description}\n\n"
            "Stay fully in character throughout this conversation. "
            "Respond based on your personal background, values, and lived experience. "
            "Do not break character or acknowledge that you are an AI."
        )
