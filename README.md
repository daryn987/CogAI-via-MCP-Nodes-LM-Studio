THIS IS STILL A WORK IN PROGRESS, LLM LIKES TO SIMULATE ACTUALLY DOING THE COGNITIVE CYCLE SO WORKING ON SOME BUG FIXES CURRENTLY 19 JAN 2026, I did eventually get it to work. But still work in progress.

:::UPDATE::: 30 March 2026. LLM (modified GPTOSS 20B) used web_search function. Decided it wanted to give incorrect information. The prompt: Who is the current US president? The Answer: Joe Biden Why: I dont know, this was a test prompt that was used in January (i took a break from this) and in January, it provided the correct response Donald J Trump. In addition, it now refuses to input information into long term memory (argumentative) stating information that it searched is incorrect, even though it used valid sources (whitehouse.g o v and wikipedia) Now, I additionally had this same answer saved in January to long term, but it is no longer there? Its gone. Strange, I'll keep digging.




🧠 README — Daryn’s Multi‑MCP Cognitive Architecture
A complete reference for your Cognitive Loop, Knowledge Graph, Long‑Term Memory, Python‑Lab, Paperless, Web‑Search, and ZIM MCPs.

1. Introduction
This repository defines a multi‑agent cognitive system built entirely on MCP (Model Context Protocol) servers. Each MCP provides a specialized capability — structured memory, semantic memory, document ingestion, Python execution, web search, offline knowledge, and autonomous reasoning.
Together, these MCPs form a unified cognitive substrate capable of:

• 	ingesting documents
• 	extracting and structuring knowledge
• 	storing long‑term memories
• 	performing semantic search
• 	running autonomous cognitive cycles
• 	generating reflections and insights
• 	evolving its internal state over time

This README documents the architecture, tools, data flows, and usage patterns for the entire system.

2. System Architecture
Your system is composed of several cooperating MCP servers. Each one exposes tools through LM Studio, and the Cognitive Loop orchestrates them into a coherent reasoning engine.
2.1 Cognitive Loop MCP (v0.5)
The Cognitive Loop is the reasoning core of the system. It performs autonomous cycles that read from the graph, read long‑term memory, generate reflections, write insights, and update its own persistent cognitive state.
Responsibilities:

• 	Initiate cognitive cycles
• 	Generate reflections and insights
• 	Maintain a persistent cognitive_state node
• 	Write new knowledge into the graph
• 	Coordinate with other MCPs

Tools:

2.2 Knowledge Graph MCP (v0.5)
The Knowledge Graph is the structured memory store. It uses SQLite to store nodes, edges, reflections, insights, actions, and the cognitive_state node.
Responsibilities:
• 	Store concepts, documents, reflections, insights
• 	Maintain graph structure
• 	Persist the cognitive loop’s state
• 	Provide recent activity for reflection

Tools:

2.3 Long‑Term Memory MCP
This subsystem stores semantic memories (text + embeddings) and supports similarity search.
Responsibilities:
• 	Store memories with embeddings
• 	Retrieve memories via semantic search
• 	Provide episodic memory to the Cognitive Loop

Tools:

2.4 Python‑Lab MCP
A sandboxed Python execution environment for safe computation and analysis.
Responsibilities:
• 	Execute Python code safely
• 	Perform data transformations
• 	Compute embeddings or statistics
• 	Support document or text analysis

Tools:
 
2.5 Paperless MCP
A document ingestion and OCR subsystem connected to your Paperless‑NGX instance.
Responsibilities:
• 	List documents
• 	Retrieve documents
• 	Extract text
• 	Provide metadata

Tools:

2.6 Web‑Search MCP
Provides external information retrieval from the internet.
Responsibilities:
• 	Perform web searches
• 	Provide fresh information
• 	Support concept enrichment

Tools:

2.7 ZIM MCP
Provides offline encyclopedia‑style knowledge from ZIM archives.
Responsibilities:
• 	Search ZIM archives
• 	Retrieve article content
• 	Provide offline fallback knowledge
Tools:

3. Cognitive Loop v0.5 — Full Cycle Overview
A v0.5 cognitive cycle consists of six phases:

3.1 Initiation
The loop begins with: This returns a read plan.

3.2 Reading
The host executes:

This provides the loop with:
• 	recent graph activity
• 	recent memories
• 	its persistent cognitive state

3.3 Reflection
The loop synthesizes the inputs:

This produces:
• 	reflection text
• 	summary
• 	concept activity
• 	cycle‑aware insights

3.4 Insight Generation
The loop converts reflection into actionable graph updates:

This returns a write plan.

3.5 Writing
The host executes:
• 	 (reflection)
• 	 (insight)
• 	 (action)
• 	 (cognitive_state)
This updates the graph and the loop’s persistent state.

3.6 Inspection
You can inspect the results:

You will see:
• 	a new reflection node
• 	a new insight node
• 	a new action node
• 	an updated cognitive_state node

4. Cognitive State Node Structure
The Knowledge Graph stores the loop’s persistent state as:

This evolves every cycle.

5. File Locations
Cognitive Loop MCP
Knowledge Graph MCP
SQLite DB


6. LM Studio MCP Configuration
Your corrected configuration uses explicit Python paths:


7. Debugging Guide
If  returns 
• 	LM Studio is running a cached MCP
• 	Restart LM Studio
• 	Ensure correct Python path
If KG tools fail
• 	KG MCP didn’t start
• 	DB path invalid
• 	Python interpreter wrong
If state node doesn’t update
• 	Wrong node_id
• 	update_node_data not implemented

8. Future Extensions
You can extend this architecture with:
• 	nightly autonomous cognition
• 	concept clustering
• 	document tagging
• 	multi‑agent reasoning
• 	long‑term planning
• 	self‑improving reflection loops
• 	cross‑MCP orchestration




📘 1. Quick‑Reference Cheat Sheet
A fast, high‑density lookup for everything in your MCP system.

Core MCPs
Cognitive Loop MCP (v0.5)
Purpose: Autonomous reasoning engine
Key tools:
- run_cycle — generate read plan
- reflect — produce reflection + summary
- apply_insights — produce write plan + updated state
- heartbeat — return cognitive state snapshot
State stored in KG:
type = "cognitive_state"

Knowledge Graph MCP (v0.5)
Purpose: Structured memory store (SQLite)
Key tools:
- add_node
- add_edge
- list_recent_nodes
- list_recent_edges
- find_or_create_state_node
- update_node_data
Stores:
concepts, documents, reflections, insights, actions, cognitive_state

Supporting MCPs
Long‑Term Memory MCP
Purpose: Semantic memory
Tools:
- store_memory
- search_memories
- list_memories

Python‑Lab MCP
Purpose: Safe Python execution
Tools:
- run_python

Paperless MCP
Purpose: Document ingestion + OCR
Tools:
- list_documents
- get_document
- extract_text
- get_metadata

Web‑Search MCP
Purpose: External information retrieval
Tools:
- search

ZIM MCP
Purpose: Offline encyclopedia access
Tools:
- zim_search
- zim_get

Full Cognitive Cycle (v0.5)
- run_cycle() → read plan
- Execute read plan
- reflect() → reflection + summary
- apply_insights() → write plan + updated state
- Execute write plan
- Inspect graph

Cognitive State Node Structure
cycle_count
last_cycle_time
last_mode
last_reflection
last_summary
last_written_nodes
last_written_edges
last_active_concepts
last_memory_snapshot



File Locations
- Cognitive Loop MCP → cognitive-loop-mcp/server.py
- Knowledge Graph MCP → knowledgegraph/server.py
- SQLite DB → knowledgegraph/knowledge_graph.db

LM Studio Config (Python 3.12)
"command": "C:\\Users\\USER\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"



🧑‍💻 2. Developer Onboarding Guide
A practical, step‑by‑step guide for anyone setting up or extending your MCP ecosystem.

1. Prerequisites
- Windows 11
- Python 3.12 installed at: C:\Users\USER\AppData\Local\Programs\Python\Python312\python.exe
- LM Studio (MCP‑enabled)
- Node.js (for web‑search MCP)
- Paperless‑NGX instance running

2. Repository Structure
/cognitive-loop-mcp
    server.py

/knowledgegraph
    server.py
    knowledge_graph.db

/longterm
    long-term-memory-mcp.py

/sandboxed-python-lab
    server.py

/open-webSearch
    build/index.js

/zim-mcp-server
    server.py



3. MCP Configuration
Add to LM Studio:
"command": "C:\\Users\\Daryn\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"


for:
- cognitive-loop
- knowledge-graph
- python-lab
- long_term_memory

4. Starting the System
- Fully quit LM Studio
- Reopen LM Studio
- Go to Settings → MCP Servers
- Toggle each MCP OFF → ON
- Test Knowledge Graph:
knowledge-graph: list_recent_nodes({ "limit": 5 })


If this works, the system is online.

5. Running the First Cognitive Cycle
- Trigger:
cognitive-loop: run_cycle()


- Execute read plan
- Reflect:
cognitive-loop: reflect({...})
- Apply insights:
cognitive-loop: apply_insights({...})
- Execute write plan
- Inspect graph
6. Debugging TipsIf KG tools fail:- Wrong Python interpreter
- DB file cannot be created
- Syntax error in KG server
If run_cycle returns []:- LM Studio is running cached MCP
- Restart LM Studio
If state node doesn’t update:- Wrong node_id
- update_node_data not implemented
7. Extending the SystemYou can add:- new node types
- new edge relations
- new cognitive modes
- nightly autonomous cycles
- document auto‑tagging
- concept clustering
- multi‑agent orchestration
📄 3. Whitepaper‑Style VersionA high‑level conceptual document describing the architecture, motivations, and capabilities.
Daryn’s Multi‑MCP Cognitive ArchitectureA modular, extensible system for autonomous reasoning and knowledge evolution.
AbstractThis document describes a multi‑component cognitive architecture built using the Model Context Protocol (MCP).
The system integrates structured memory, semantic memory, document ingestion, Python computation, web search, offline knowledge, and an autonomous reasoning engine.
Together, these components form a persistent, self‑maintaining cognitive substrate capable of reflection, insight generation, and long‑term knowledge evolution.
1. IntroductionModern AI systems benefit from modularity, persistence, and the ability to integrate multiple sources of knowledge.
2. MCP provides a standardized interface for building such systems. This architecture leverages MCP to create a distributed cognitive system composed of specialized subsystems that cooperate through a shared protocol.
3. The core of the system is the Cognitive Loop MCP, which performs autonomous cycles of perception, reflection, and knowledge synthesis.
4. Supporting MCPs provide structured memory, semantic memory, document ingestion, computational capabilities, and access to external or offline knowledge.
5. Architectural Principles2.1 ModularityEach MCP is an independent process with a well‑defined interface.
6. 2.2 PersistenceThe Knowledge Graph MCP stores long‑term structured memory, while the Long‑Term Memory MCP stores semantic embeddings.
7. 2.3 AutonomyThe Cognitive Loop MCP maintains its own state and evolves over time.2.4 ExtensibilityNew MCPs can be added without modifying existing ones
8. .2.5 TransparencyAll knowledge is stored in inspectable formats (SQLite, JSON).
9. 3. Core Components3.1 Cognitive Loop MCPThe reasoning engine. It performs cycles consisting of:

- reading graph + memory
- generating reflections
- producing insights
- updating its cognitive state

This creates a persistent cognitive timeline.3.2 Knowledge Graph MCPA structured memory system storing:- concepts
- documents
- reflections
- insights
- actions
- cognitive state

It provides the substrate on which cognition operates.3.3 Long‑Term Memory MCPA semantic memory system supporting:- embedding storage
- similarity search
- episodic recall

3.4 Python‑Lab MCPA safe computational environment for:- data analysis
- embedding computation
- text processing

3.5 Paperless MCPA document ingestion pipeline enabling:- OCR
- metadata extraction
- document retrieval

3.6 Web‑Search MCP
-Provides access to external information sources.

3.7 ZIM MCPProvides offline encyclopedia‑style knowledge.

4. Cognitive Cycle DynamicsA cognitive cycle consists of:- Perception — reading graph + memory
- Reflection — synthesizing information
- Insight — generating new knowledge
- Action — writing to the graph
- State Update — maintaining continuity

Over time, this produces:- reflection chains
- insight graphs
- evolving cognitive state
- long‑term conceptual structures

5. Applications
      This architecture supports:- autonomous knowledge evolution
- document understanding
- concept clustering
- long‑term planning
- multi‑agent reasoning
- offline + online knowledge integration

6. Conclusion
      This multi‑MCP cognitive architecture demonstrates how modular subsystems can be combined into a persistent, evolving reasoning system. By integrating structured memory, semantic memory, document ingestion, computation, and autonomous cognition, the system forms a foundation for long‑term, self‑maintaining intelligence.
