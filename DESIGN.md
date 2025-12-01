# DESIGN.md
# Catalyst Agent Framework – Design Document (CAF)

**Version:** 1.0  
**Status:** Final Draft  
**Last Updated:** Nov 2025  

---

## 1. Purpose of This Document
This design document defines the implementation strategy, naming conventions, module responsibilities, coding standards, and extensibility patterns for the Catalyst Agent Framework (CAF). It complements `ARCHITECTURE.md` by detailing **how** to implement the system predictably and professionally.

---

## 2. Design Principles
### 2.1 Modularity
Each component operates independently and can be tested in isolation.

### 2.2 Provider-Agnostic
All LLM calls must go through `LLMEngine`, enabling Gemini, LLaMA, OpenAI, and future engines without refactoring.

### 2.3 Framework-Light
No LangChain, DSPy, LlamaIndex, or large abstractions in v1. Maintain control through pure Python.

### 2.4 Observability-First
Logging, events, and metrics are mandatory in all agents and tools.

### 2.5 Predictable Extensibility
Clear patterns for adding tools, engines, agents, and multi-agent orchestrators.

---

## 3. Naming Conventions

### 3.1 Repository Name
```
catalyst_agent_framework
```

### 3.2 Python Package Name
```
catalyst_agent_framework
```

### 3.3 CLI Command
```
caf
```

### 3.4 Directory & Module Naming
| Component | Convention | Example |
|----------|------------|---------|
| Agents | `<name>_agent.py` | `task_agent.py` |
| Tools | `<name>.py` | `search.py` |
| Engines | `<provider>_engine.py` | `gemini_engine.py` |
| Utils | lowercase | `logger.py` |
| Config | lowercase | `settings.py` |

### 3.5 Class Naming
CamelCase:
- `BaseAgent`
- `GeminiEngine`
- `SearchTool`
- `AgentResponse`

### 3.6 Function Naming
snake_case:
- `run_step()`
- `emit_event()`
- `parse_json()`

### 3.7 Event Naming (dot notation)
- `agent.start`
- `agent.finish`
- `llm.call`
- `tool.call`
- `tool.error`

### 3.8 Metrics Naming (Prometheus)
- `caf_requests_total`
- `caf_errors_total`
- `caf_tool_calls_total`
- `caf_agent_latency_seconds`

### 3.9 Logging
All logs must be JSON-structured.

Example:
```json
{
  "timestamp": "2025-12-01T10:00:00Z",
  "level": "INFO",
  "component": "agent",
  "event": "agent.start",
  "agent": "task_agent",
  "params": {}
}
```

---

## 4. Module Responsibilities

### 4.1 core/
#### agent.py
- BaseAgent  
- step orchestration  
- tool handling  
- termination rules  
- event emission  
- metrics updates  

#### llm_engine.py
Defines the unified provider interface.

#### response.py
Defines the structured agent response.

#### events.py
Defines event schema & dispatcher.

---

### 4.2 engines/
Each engine implements `LLMEngine`.

Rules:
- No agent logic  
- No file system logic  
- Must normalize provider responses  

---

### 4.3 tools/
Tools inherit from `BaseTool` and must:
- validate inputs  
- produce JSON-friendly outputs  
- raise tool-specific errors  

---

### 4.4 utils/
Generic utilities such as:
- logger.py  
- metrics.py  
- error_handler.py  
- json_parser.py  

---

### 4.5 config/
- settings.py  
- loaders.py  

Config overrides:
1. env vars  
2. YAML  
3. defaults  

---

### 4.6 cli/
Implements:
- `caf run ...`
- `caf tools`
- `caf agents`

Clean output only; logs must not pollute stdout.

---

## 5. LLM Engine Contract
All engines must implement:

```python
class LLMEngine:
    def generate(self, prompt: str) -> dict: ...
    def call_tools(self, prompt: str, tools: list) -> dict: ...
```

Requirements:
- no print statements  
- exceptions must be normalized  
- structured dict response only  

---

## 6. Tool Design Protocol

### Structure:
```python
class SearchTool(BaseTool):
    name = "search"
    input_schema = {...}
    output_schema = {...}

    def execute(self, query: str):
        ...
```

Rules:
- tools never assume agent details  
- tools must validate inputs  
- tool output must be structured  

---

## 7. Agent Execution Model

### 7.1 Loop
1. Build initial prompt  
2. LLM call  
3. Parse for tool calls  
4. Execute tools if required  
5. Append step  
6. Check termination conditions  
7. Return final response  

### 7.2 Step Object
Every step is a structured dict including:
- prompt  
- model output  
- tool use  
- metadata  

---

## 8. Observability

### 8.1 Logging
JSON structured logs only.

### 8.2 Metrics
Counters, histograms, gauges.

### 8.3 Events
Emitted for:
- agent lifecycle  
- LLM calls  
- tool execution  
- errors  

---

## 9. AgentOps Design

### 9.1 Agent Registry
```
registry/
  agents.json
  tools.json
```

### 9.2 Versioning
Semantic:
```
major.minor.patch
```

### 9.3 Governance
Enforces:
- allowed tools  
- max_steps  
- provider  
- rate limits  

---

## 10. Extensibility Rules

### Add a tool:
- implement BaseTool  
- update tools.json  

### Add an engine:
- implement LLMEngine contract  

### Add an agent:
- inherit BaseAgent  
- register in agents.json  

### Add multi-agent orchestration:
- orchestrator = "super-agent"  
- multiple internal agent invocations  

---

## 11. Testing Strategy

### Unit tests:
- tools  
- engines  
- utils  
- agents  

### Integration tests:
- LLM engine + agent  
- agent + tool  
- CLI  

### Mocking:
- All LLM calls must be mocked  

---

## 12. Deployment Considerations

### Docker
- python:3.14-slim  
- minimal dependencies  

### FastAPI (Phase 2)
- `/run-agent`  
- `/metrics`  

### CI/CD
- GitHub Actions  
- lint → test → build → deploy  

---

# **End of DESIGN.md**
