"""
session_manager.py — Read, write, and reset Mirror Jury session state.

Usage:
    python _automations/scripts/session_manager.py           # print current state
    python _automations/scripts/session_manager.py --reset   # start fresh
    python _automations/scripts/session_manager.py --personas  # list the panel only
    python _automations/scripts/session_manager.py --log      # show workflow log
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

STATE_FILE = Path(__file__).parent.parent / "state" / "session.json"

EMPTY_STATE = {
    "session_id": "",
    "started_at": "",
    "last_updated": "",
    "question": "",
    "user_context": "",
    "topic_domain": "",
    "guardrail_facts": [],
    "personas": [],
    "active_persona_index": None,
    "conversations": {},
    "group_exchanges": [],
    "synthesis_complete": False,
    "workflow_log": [],
}


def load() -> dict:
    if not STATE_FILE.exists():
        return EMPTY_STATE.copy()
    with open(STATE_FILE) as f:
        return json.load(f)


def save(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state["last_updated"] = datetime.utcnow().isoformat()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def reset() -> dict:
    state = EMPTY_STATE.copy()
    state["session_id"] = f"mirror_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    state["started_at"] = datetime.utcnow().isoformat()
    save(state)
    print(f"Session reset. New ID: {state['session_id']}")
    return state


def print_state(state: dict) -> None:
    print(f"\n{'='*50}")
    print(f"Session: {state.get('session_id', 'none')}")
    print(f"Question: {state.get('question', '—')}")
    print(f"Topic: {state.get('topic_domain', '—')}")
    print(f"Personas: {len(state.get('personas', []))}")
    print(f"Group exchanges: {len(state.get('group_exchanges', []))}")
    print(f"1-on-1 conversations: {len(state.get('conversations', {}))}")
    print(f"Synthesis complete: {state.get('synthesis_complete', False)}")
    print(f"{'='*50}\n")


def print_personas(state: dict) -> None:
    personas = state.get("personas", [])
    if not personas:
        print("No panel assembled yet.")
        return
    print(f"\nPanel ({len(personas)} people):")
    for p in personas:
        print(f"  [{p['index']}] {p['brief']}")
    print()


def print_log(state: dict) -> None:
    log = state.get("workflow_log", [])
    if not log:
        print("No workflow log entries.")
        return
    print("\nWorkflow Log:")
    for entry in log:
        print(f"  {entry}")
    print()


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--reset" in args:
        reset()
    elif "--personas" in args:
        print_personas(load())
    elif "--log" in args:
        print_log(load())
    else:
        print_state(load())
