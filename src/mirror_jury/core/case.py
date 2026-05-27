from dataclasses import dataclass, field


@dataclass
class Case:
    question: str
    context: str = ""
    # Verified facts jurors MUST ground their reasoning in.
    # Prevents hallucination of statistics, studies, or events.
    facts: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    options: list[str] = field(default_factory=list)

    def render(self) -> str:
        parts = []
        if self.context:
            parts.append(f"BACKGROUND:\n{self.context}")
        if self.facts:
            lines = "\n".join(f"  • {f}" for f in self.facts)
            parts.append(f"\nVERIFIED FACTS (use only these — do not invent statistics or cite sources not listed here):\n{lines}")
        if self.sources:
            src_lines = "\n".join(f"  [{i+1}] {s}" for i, s in enumerate(self.sources))
            parts.append(f"\nSOURCES:\n{src_lines}")
        parts.append(f"\nQUESTION:\n{self.question}")
        if self.options:
            opts = "\n".join(f"  {i+1}. {o}" for i, o in enumerate(self.options))
            parts.append(f"\nOPTIONS:\n{opts}")
        return "\n".join(parts)
