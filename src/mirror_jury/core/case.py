from dataclasses import dataclass, field


@dataclass
class Case:
    question: str
    context: str = ""
    options: list[str] = field(default_factory=list)

    def render(self) -> str:
        parts = []
        if self.context:
            parts.append(f"BACKGROUND:\n{self.context}\n")
        parts.append(f"QUESTION:\n{self.question}")
        if self.options:
            opts = "\n".join(f"  {i+1}. {o}" for i, o in enumerate(self.options))
            parts.append(f"\nOPTIONS:\n{opts}")
        return "\n".join(parts)
