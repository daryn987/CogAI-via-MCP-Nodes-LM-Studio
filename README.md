🧠 README — Full MCP Ecosystem
A complete reference for architecture, tools, flows, and usage

📌 Overview
Your system is a multi‑MCP cognitive architecture composed of:
Core Cognitive Subsystems
- Cognitive Loop MCP (v0.5) — autonomous reasoning engine
- Knowledge Graph MCP (v0.5) — persistent graph memory
- Long‑Term Memory MCP — embeddings + semantic recall
Operational / Utility Subsystems
- Python‑Lab MCP — sandboxed Python execution
- Paperless MCP — document ingestion + OCR + metadata
- Web‑Search MCP — external information retrieval
- Zim MCP — local ZIM archive search
Together, these form a unified cognitive substrate capable of:
- reading documents
- extracting knowledge
- storing structured memory
- reflecting
- writing insights
- evolving over time
- running autonomous cycles

🧩 System Architecture
┌──────────────────────────────┐
│        Cognitive Loop        │
│            (v0.5)            │
│  - run_cycle                 │
│  - reflect                   │
│  - apply_insights            │
│  - heartbeat                 │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│       Knowledge Graph        │
│            (v0.5)            │
│  - add_node                  │
│  - add_edge                  │
│  - list_recent_*             │
│  - find_or_create_state_node │
│  - update_node_data          │
└───────────────┬──────────────┘
                │
                ▼
┌──────────────────────────────┐
│       Long‑Term Memory       │
│  - store_memory              │
│  - search_memories           │
│  - list_memories             │
└──────────────────────────────┘

┌──────────────────────────────┐
│         Python‑Lab           │
│  - run_python                │
│  - safe execution            │
└──────────────────────────────┘

┌──────────────────────────────┐
│          Paperless           │
│  - list_documents            │
│  - get_document              │
│  - extract_text              │
│  - metadata                  │
└──────────────────────────────┘

┌──────────────────────────────┐
│          Web‑Search          │
│  - search                    │
└──────────────────────────────┘

┌──────────────────────────────┐
│            ZIM               │
│  - zim_search                │
│  - zim_get                   │
└──────────────────────────────┘



🧠 Cognitive Loop MCP (v0.5)
Purpose
A persistent, stateful reasoning engine that:
- reads the graph
- reads long‑term memory
- reflects
- writes new nodes
- updates its own cognitive state
- maintains continuity across cycles
Tools
run_cycle
Returns a read plan:
- list_recent_nodes
- list_recent_edges
- list_memories
- find_or_create_state_node
reflect
Consumes:
- nodes
- edges
- memories
- cognitive_state
Produces:
- reflection text
- summary
apply_insights
Consumes:
- reflection
- summary
- state_node_id
- state
Produces:
- write_plan
- updated_state
heartbeat
Returns:
- last cycle
- last reflection
- last summary
- active concepts
- cycle count

🧩 Knowledge Graph MCP (v0.5)
Purpose
A SQLite‑backed graph database storing:
- nodes
- edges
- cognitive state
- reflection chains
- insights
- actions
Tools
add_node
Creates a node.
add_edge
Creates an edge.
list_recent_nodes
Returns latest nodes.
list_recent_edges
Returns latest edges.
find_or_create_state_node
Ensures a persistent cognitive_state node exists.
update_node_data
Updates the cognitive_state node.

🧠 Long‑Term Memory MCP
Purpose
Semantic memory storage + retrieval.
Tools
store_memory
Stores:
- text
- embedding
- metadata
search_memories
Semantic search over embeddings.
list_memories
Returns recent memory entries.
Typical Use
The Cognitive Loop uses this to:
- retrieve recent memories
- detect conceptual patterns
- enrich reflections

🧪 Python‑Lab MCP
Purpose
A sandboxed Python execution environment for:
- data processing
- embeddings
- CSV/JSON manipulation
- document analysis
- safe experimentation
Tools
run_python
Executes Python code under:
- curated whitelist imports
- restricted environment
- no filesystem access
- no network access
Typical Use
The Cognitive Loop can:
- preprocess documents
- compute embeddings
- analyze text
- cluster concepts

📄 Paperless MCP
Purpose
Document ingestion + OCR + metadata extraction.
Tools
list_documents
Returns all documents.
get_document
Fetches a specific document.
extract_text
OCR + text extraction.
get_metadata
Returns metadata (tags, dates, etc.)
Typical Use
The Cognitive Loop can:
- ingest new documents
- extract text
- create document nodes
- link documents to concepts

🌐 Web‑Search MCP
Purpose
External information retrieval.
Tools
search
Performs web search queries.
Typical Use
The Cognitive Loop can:
- enrich concepts
- validate facts
- expand knowledge

📚 ZIM MCP
Purpose
Local offline knowledge retrieval from ZIM archives.
Tools
zim_search
Searches ZIM content.
zim_get
Retrieves article content.
Typical Use
The Cognitive Loop can:
- pull offline encyclopedia data
- enrich graph nodes
- support reasoning without internet

🔄 Full v0.5 Cognitive Cycle (Step‑by‑Step)
1. Trigger cycle
cognitive-loop: run_cycle()


2. Execute read plan
knowledge-graph: list_recent_nodes(...)
knowledge-graph: list_recent_edges(...)
long_term_memory: list_memories(...)
knowledge-graph: find_or_create_state_node(...)


3. Reflect
cognitive-loop: reflect({...})


4. Apply insights
cognitive-loop: apply_insights({...})


5. Execute write plan
knowledge-graph: add_node(...)
knowledge-graph: add_node(...)
knowledge-graph: add_node(...)
knowledge-graph: update_node_data(...)


6. Inspect graph
knowledge-graph: list_recent_nodes()
knowledge-graph: list_recent_edges()



⚙️ LM Studio MCP Configuration
Your corrected config:
"knowledge-graph": {
  "command": "C:\\Users\\Daryn\\AppData\\Local\\Programs\\Python\\Python312\\python.exe",
  "args": [
    "C:\\Users\\Daryn\\knowledgegraph\\server.py"
  ]
},
"cognitive-loop": {
  "command": "C:\\Users\\Daryn\\AppData\\Local\\Programs\\Python\\Python312\\python.exe",
  "args": [
    "C:\\Users\\Daryn\\cognitive-loop-mcp\\server.py"
  ]
}



🛠 Debugging Checklist
If run_cycle returns []
- LM Studio is running an old cached MCP
- Restart LM Studio
- Ensure correct Python path
If KG tools fail
- KG MCP didn’t start
- DB path invalid
- Python interpreter wrong
If state node doesn’t update
- Wrong node_id
- update_node_data not implemented
