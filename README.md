This revised documentation consolidates the redundant sections from your original notes into a single, cohesive guide. I have organized it by **Concept** (What it is), **Operation** (How it works), **Deployment** (How to set it up), and **Reference** (Quick lookup).

***

# 🧠 Daryn’s Multi‑MCP Cognitive Architecture
**A modular, extensible system for autonomous reasoning and knowledge evolution.**

> **Status:** Work in Progress (Active Development)
> **Note:** Currently refining the cognitive cycle and debugging `web_search` behavior and `long_term_memory` persistence.

## 1. Overview
This repository defines a multi-agent cognitive system built on the **Model Context Protocol (MCP)**. By integrating specialized MCP servers, the system creates a unified "cognitive substrate" capable of:
*   **Ingestion:** Extracting and structuring knowledge from documents (Paperless) and the web.
*   **Persistence:** Storing structured data (Knowledge Graph) and semantic embeddings (Long-Term Memory).
*   **Reasoning:** Executing autonomous cognitive cycles to generate reflections, insights, and state updates.
*   **Computation:** Running sandboxed Python code for data analysis and complex transformations.

---

## 2. System Architecture (The MCP Subsystems)

### 2.1 Core Reasoning & Memory
*   **Cognitive Loop MCP (v0.5):** The reasoning engine. It orchestrates the autonomous cycles of perception, reflection, and knowledge synthesis.
*   **Knowledge Graph MCP (v0.5):** The structured memory store. Uses **SQLite** to persist nodes, edges, reflections, insights, and the persistent `cognitive_state`.
*   **Long‑Term Memory MCP:** The semantic memory system. Stores text + embeddings to support similarity searches and episodic recall.

### 2.2 Supporting Capabilities
*   **Python‑Lab MCP:** A sandboxed environment for safe computation, statistics, and data transformation.
*   **Paperless MCP:** A document ingestion pipeline connected to Paperless‑NGX for OCR, metadata extraction, and retrieval.
*   **Web‑Search MCP:** Provides external information retrieval for concept enrichment.
*   **ZIM MCP:** Provides offline, encyclopedia-style knowledge from ZIM archives as a fallback.

---

## 3. The Cognitive Cycle (v0.5)
The system operates through a six-phase autonomous loop to evolve its internal state:

1.  **Initiation:** The loop requests a "read plan."
2.  **Reading:** The host fetches recent graph activity, memories, and the current `cognitive_state`.
3.  **Reflection:** The loop synthesizes inputs to produce a reflection, summary, and cycle-aware insights.
4.  **Insight Generation:** The loop converts reflections into actionable graph updates (a "write plan").
5.  **Writing:** The host executes the write plan, updating the graph with new reflections, insights, actions, and the updated `cognitive_state`.
6.  **Inspection:** The user can verify the new nodes and the updated state in the graph.

### Cognitive State Node Structure
The `cognitive_state` node is updated every cycle to maintain continuity:
```json
{
  "cycle_count": "number",
  "last_cycle_time": "timestamp",
  "last_mode": "string",
  "last_reflection": "text",
  "last_summary": "text",
  "last_written_nodes": ["node_ids"],
  "last_written_edges": ["edge_ids"],
  "last_active_concepts": ["concept_ids"],
  "last_memory_snapshot": "summary"
}
```

---

## 4. Developer Onboarding & Setup

### Prerequisites
*   **OS:** Windows 11
*   **Python:** 3.12 (Path: `C:\Users\Daryn\AppData\Local\Programs\Python\Python312\python.exe`)
*   **Tools:** LM Studio (MCP-enabled), Node.js (for Web-Search), Paperless‑NGX instance.

### Repository Structure
*   `/cognitive-loop-mcp` (server.py)
*   `/knowledgegraph` (server.py, knowledge_graph.db)
*   `/longterm` (long-term-memory-mcp.py)
*   `/sandboxed-python-lab` (server.py)
*   `/open-webSearch` (build/index.js)
*   `/zim-mcp-server` (server.py)

### Configuration (LM Studio)
Use the following Python command for all relevant MCPs:
`"command": "C:\\Users\\Daryn\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"`

### Starting the System
1.  Fully quit and restart **LM Studio**.
2.  Navigate to **Settings → MCP Servers**.
3.  Toggle each MCP **OFF $\rightarrow$ ON**.
4.  **Verification:** Test the Knowledge Graph:
    `knowledge-graph: list_recent_nodes({ "limit": 5 })`

---

## 5. Quick Reference Cheat Sheet

| MCP Name | Purpose | Key Tools |
| :--- | :--- | :--- |
| **Cognitive Loop** | Reasoning Engine | `run_cycle`, `reflect`, `apply_insights`, `heartbeat` |
| **Knowledge Graph** | Structured Memory | `add_node`, `add_edge`, `list_recent_nodes`, `update_node_data` |
| **Long-Term Memory**| Semantic Memory | `store_memory`, `search_memories`, `list_memories` |
| **Python-Lab** | Safe Execution | `run_python` |
| **Paperless** | Doc Ingestion | `list_documents`, `get_document`, `extract_text` |
| **Web-Search** | Online Info | `search` |
| **ZIM** | Offline Knowledge| `zim_search`, `zim_get` |

---

## 6. Debugging & Development Logs

### Common Issues
*   **Tools Fail to Load:** Restart LM Studio; verify the Python interpreter path is correct.
*   **KG Tools Fail:** Ensure the DB path is valid and the KG MCP server is actually running.
*   **State Not Updating:** Check if `node_id` is correct or if `update_node_data` is properly implemented.

### Known Issues (Work in Progress)
*   **Web Search Behavior:** Observed instances of the LLM providing incorrect information or refusing to input searched data into long-term memory (argumentative behavior).
*   **Memory Persistence:** Investigating issues where previously saved memories in long-term storage appear to disappear.
