# server.py — Cognitive Loop MCP (Option 2 orchestration)

from fastmcp import FastMCP as Server
from datetime import datetime
import json
import os
from typing import List, Dict, Any

server = Server("cognitive-loop")

# ---------------------------------------------------------
# Persistent state (local JSON file)
# ---------------------------------------------------------

STATE_PATH = os.path.join(os.path.dirname(__file__), "cognitive_loop_state.json")

STATE_DEFAULT = {
    "cycle": 0,
    "active_goals": [],
    "last_plan": [],
    "last_reflection": [],
    "heartbeat": 0,
    "last_seen": None,
}


def _load_state_from_disk() -> Dict[str, Any]:
    if not os.path.exists(STATE_PATH):
        return dict(STATE_DEFAULT)
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return dict(STATE_DEFAULT)

    merged = dict(STATE_DEFAULT)
    merged.update(data)
    return merged


def _save_state_to_disk(state: Dict[str, Any]) -> None:
    try:
        with open(STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception:
        # Fail silently; state is best-effort
        pass


def load_state() -> Dict[str, Any]:
    return _load_state_from_disk()


def save_state(updates: Dict[str, Any]) -> None:
    state = load_state()
    state.update(updates)
    _save_state_to_disk(state)


# ---------------------------------------------------------
# Tools
# ---------------------------------------------------------

@server.tool()
def heartbeat() -> Dict[str, Any]:
    """
    Increment heartbeat and update last_seen.
    Used to confirm the loop is reachable and alive.
    """
    state = load_state()
    updates = {
        "heartbeat": state.get("heartbeat", 0) + 1,
        "last_seen": datetime.utcnow().isoformat(),
    }
    save_state(updates)
    return {"status": "ok", "state_updates": updates}


@server.tool()
def run_cycle(goal: str = "") -> Dict[str, Any]:
    """
    Generate a simple, declarative plan for the given goal.

    This MCP does NOT execute other tools itself.
    It only returns a plan that LM Studio (the orchestrator)
    should follow by calling other MCP tools.
    """
    state = load_state()
    cycle_num = state.get("cycle", 0) + 1

    # Example plan: LM Studio should execute these steps in order.
    plan: List[Dict[str, Any]] = []

    if goal:
        plan.append(
            {
                "step_id": "1",
                "tool": "knowledge-graph.add_node",
                "args": {
                    "type": "goal",
                    "content": goal,
                },
                "reasoning": "Record the user goal as a node in the knowledge graph.",
            }
        )

        plan.append(
            {
                "step_id": "2",
                "tool": "paperless.search",
                "args": {
                    "query": goal,
                },
                "reasoning": "Search documents for information relevant to the goal.",
            }
        )

        plan.append(
            {
                "step_id": "3",
                "tool": "long-term-memory.search_memories",
                "args": {
                    "query": goal,
                    "limit": 5,
                },
                "reasoning": "Retrieve prior memories related to this goal.",
            }
        )
    else:
        plan.append(
            {
                "step_id": "1",
                "tool": "noop",
                "args": {"message": "No goal provided; demonstration step only."},
                "reasoning": "Placeholder step when no explicit goal is given.",
            }
        )

    updates = {
        "cycle": cycle_num,
        "active_goals": [goal] if goal else state.get("active_goals", []),
        "last_plan": plan,
        "last_seen": datetime.utcnow().isoformat(),
    }

    save_state(updates)

    return {
        "plan": plan,
        "state_updates": updates,
    }


@server.tool()
def reflect(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Reflect on the results of a completed plan.

    `results` should be a list of objects like:
    {
      "tool": "paperless.search",
      "args": { ... },
      "output": { ... }
    }
    """
    insights: List[str] = []

    for r in results:
        tool_name = r.get("tool")
        output = r.get("output")
        insight = f"Observed output from {tool_name}: {output}"
        insights.append(insight)

    updates = {
        "last_reflection": insights,
        "last_seen": datetime.utcnow().isoformat(),
    }

    save_state(updates)

    return {
        "insights": insights,
        "state_updates": updates,
    }


@server.tool()
def get_state() -> Dict[str, Any]:
    """
    Return the current persistent state.
    """
    return load_state()


@server.tool()
def set_state(updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge updates into the current state and persist them.
    """
    save_state(updates)
    return {"updated": updates}


# ---------------------------------------------------------
# Run server
# ---------------------------------------------------------

if __name__ == "__main__":
    server.run()