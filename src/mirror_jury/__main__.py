from __future__ import annotations
"""
Interactive CLI for AI Mirror Jury.

    python -m mirror_jury
"""

import sys
import textwrap

from mirror_jury.datasets.persona_hub import PersonaHubDataset
from mirror_jury.session.mirror_jury import MirrorJury


DIVIDER = "─" * 60
HELP = textwrap.dedent("""\
    Commands:
      speak <N>   — 1-on-1 with person N (conversation persists)
      ask all     — Ask everyone the same question at once
      list        — Show the panel again
      help        — Show this menu
      quit        — Exit
""")


def _print_panel(personas: list[dict]) -> None:
    print(f"\n{DIVIDER}")
    print("  YOUR PANEL")
    print(DIVIDER)
    for p in personas:
        print(f"  [{p['index']}] {p['brief']}")
    print(DIVIDER)


def _one_on_one(jury: MirrorJury, index: int) -> None:
    persona = jury.cohort.get(index)
    print(f"\n{DIVIDER}")
    print(f"  1-on-1 with person [{index}]")
    print(f"  {persona.brief}")
    print(f"  (type 'back' to return to the panel)")
    print(DIVIDER)
    while True:
        try:
            msg = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not msg:
            continue
        if msg.lower() in ("back", "exit", "quit"):
            break
        response = jury.speak_to(index, msg)
        print(f"\n[{index}]: {response.message}\n")


def _ask_all(jury: MirrorJury) -> None:
    try:
        msg = input("Your message to everyone: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return
    if not msg:
        return
    print("\nAsking everyone…\n")
    responses = jury.speak_to_all(msg)
    for r in responses:
        idx = next(
            p["index"]
            for p in jury.list_personas()
            if p["id"] == r.persona_id
        )
        print(f"[{idx}] {r.persona_brief}")
        wrapped = textwrap.fill(r.message, width=72, initial_indent="    ", subsequent_indent="    ")
        print(wrapped)
        print()


def main() -> None:
    print("\n" + "=" * 60)
    print("  AI MIRROR JURY")
    print("  Hear from a diverse panel — on any question.")
    print("=" * 60 + "\n")

    try:
        question = input("What question do you want to explore?\n> ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)

    if not question:
        print("No question entered. Exiting.")
        sys.exit(0)

    try:
        size_input = input("How many people in your panel? (5–10, default 7): ").strip()
        cohort_size = int(size_input) if size_input else 7
        cohort_size = max(5, min(10, cohort_size))
    except (ValueError, EOFError, KeyboardInterrupt):
        cohort_size = 7

    print(f"\nAssembling a panel of {cohort_size} people…")
    dataset = PersonaHubDataset()
    jury = MirrorJury(question=question, cohort_size=cohort_size, dataset=dataset).assemble()
    print("Done.\n")

    _print_panel(jury.list_personas())
    print(HELP)

    while True:
        try:
            cmd = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not cmd:
            continue

        lower = cmd.lower()

        if lower in ("quit", "exit", "q"):
            print("Goodbye.")
            break

        if lower in ("help", "h", "?"):
            print(HELP)
            continue

        if lower in ("list", "ls"):
            _print_panel(jury.list_personas())
            continue

        if lower.startswith("speak "):
            parts = lower.split()
            if len(parts) == 2 and parts[1].isdigit():
                _one_on_one(jury, int(parts[1]))
            else:
                print("Usage: speak <N>  (e.g. 'speak 3')")
            continue

        if lower in ("ask all", "ask everyone", "all"):
            _ask_all(jury)
            continue

        # Allow bare numbers as shorthand for speak <N>
        if lower.isdigit():
            _one_on_one(jury, int(lower))
            continue

        print("Unknown command. Type 'help' for options.")


if __name__ == "__main__":
    main()
