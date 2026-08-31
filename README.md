# AIOS — AI Agent Operating System 🤖

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Status](https://img.shields.io/badge/Status-Active%20Development-yellow)]()
[![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey)]()

**AIOS** is an LLM-powered agentic runtime that turns natural-language instructions into structured, executable actions on a local machine — a lightweight "operating system" layer for AI agents. It parses user intent, plans an action sequence, routes it through a modular tool-execution layer, and runs real system-level operations (code execution, application control, web interaction) with logging, guardrails, and extensibility built in.

Think of it as a minimal, from-scratch version of the orchestration layer behind tools like AutoGPT, LangChain Agents, or OpenAI's function-calling agents — built to understand the full request → plan → act → observe loop rather than just wrapping an API call.

---

## 📌 Why I Built This

Most LLM demos stop at "chat with a model." AIOS goes further: it explores the systems-level problem of letting a language model **safely and reliably control a real computer** — parsing ambiguous natural language into deterministic, typed actions, validating those actions before execution, and handling failure gracefully. It's a hands-on deep-dive into agentic AI architecture, structured output generation, sandboxing, and tool-use design patterns that underpin modern AI agent frameworks.

---

## 🚀 Features

- **Natural language → structured action parsing** — converts free-form user input into validated JSON actions using constrained/structured output from an LLM (Gemini 2.5 Flash)
- **Real tool execution**, not simulated: runs Python code, opens native macOS applications, and performs web search/browser automation
- **Modular tool-router architecture** — each tool is a self-contained, independently testable module registered with the router, so adding a new capability doesn't touch core logic
- **Schema validation layer** — every LLM-generated action is validated against a strict JSON schema before execution, rejecting malformed or unsafe actions
- **Safe fallback handling** — a `general_response` path catches ambiguous, unsupported, or unsafe requests instead of forcing a tool call
- **Execution logging** — every parsed action, validation result, and execution outcome is logged for debugging and auditability
- **Extensible by design** — new tools can be added by implementing a single interface and registering with the router, no changes to the parsing or execution layers required

---

## 🧠 Architecture

```
┌─────────────┐
│ User Input  │  (natural language)
└──────┬──────┘
       ▼
┌─────────────────────┐
│  LLM Planning Layer  │  Gemini 2.5 Flash — intent understanding
│  (prompt + schema)   │  + structured JSON generation
└──────┬───────────────┘
       ▼
┌─────────────────────┐
│  JSON Action Parser  │  Validates output against action schema
│  + Schema Validator   │  Rejects malformed/unsafe actions
└──────┬───────────────┘
       ▼
┌─────────────────────┐
│     Tool Router      │  Maps action.type → registered tool handler
└──────┬───────────────┘
       ▼
┌─────────────────────┐
│  Execution Layer     │  Sandboxed execution + result capture
│  (per-tool handlers) │
└──────┬───────────────┘
       ▼
┌─────────────────────┐
│   Logger / Observer  │  Records action, outcome, errors
└──────────────────────┘
```

**Design principles:**
- **Separation of concerns** — planning (LLM), validation (schema), execution (tools), and observability (logging) are fully decoupled layers
- **Fail-safe by default** — unrecognized or invalid actions never silently execute; they fall back to a safe response
- **Stateless core, pluggable tools** — the router has no knowledge of tool internals, only a registered interface contract

---

## ⚙️ Supported Tools

| Tool | Description |
|---|---|
| `run_python` | Executes Python code in a controlled subprocess and captures stdout/stderr |
| `open_app` | Opens native macOS applications via system calls |
| `search_web` | Performs web search / browser automation for information retrieval |
| `general_response` | Safe fallback for conversational, ambiguous, or unsupported requests |

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **LLM:** Google Gemini 2.5 Flash (via API)
- **Core concepts applied:** structured output / function-calling patterns, JSON schema validation, subprocess sandboxing, modular plugin architecture, agentic loop design

---

## 📦 Setup

```bash
git clone https://github.com/yourusername/AIOS.git
cd AIOS

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the project root with your API key:

```
GEMINI_API_KEY=your_key_here
```

Run the agent:

```bash
python main.py
```

---

## 💡 Example Usage

```
> Open VS Code and search the web for "Python asyncio tutorial"

[Planner]  → {"action": "open_app", "params": {"name": "Visual Studio Code"}}
[Executor] → ✅ Opened Visual Studio Code
[Planner]  → {"action": "search_web", "params": {"query": "Python asyncio tutorial"}}
[Executor] → ✅ Opened 5 search results in default browser
```

---

## 🔒 Safety & Guardrails

- All LLM-generated actions are validated against a strict schema before execution — no raw model output is ever executed directly
- Python execution runs in an isolated subprocess with output capture, not `eval()`
- Unsupported or ambiguous requests route to `general_response` instead of attempting a best-guess execution
- All actions and outcomes are logged for auditability

---

## 🗺️ Roadmap

- [ ] **Memory layer** — persistent context across sessions (vector store for long-term agent memory)
- [ ] **Multi-step planning** — decompose complex requests into an ordered sequence of tool calls instead of single-action turns
- [ ] **Permission system** — per-tool user confirmation before executing sensitive actions (file writes, app control)
- [ ] **Plugin marketplace** — drop-in third-party tool modules with a standardized manifest
- [ ] **Cross-platform support** — extend `open_app` and system tools beyond macOS to Windows/Linux
- [ ] **Local LLM support** — swap in local models (Llama, Mistral) via a pluggable model interface
- [ ] **Web dashboard** — real-time view of agent reasoning, action history, and logs
- [ ] **Unit + integration test suite** — full coverage of parser, router, and tool layers

---

## 🧪 Testing

```bash
pytest tests/
```

*(Test suite in progress — see Roadmap)*

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](https://github.com/yourusername/AIOS/issues) or open a PR.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**[Your Name]**
[LinkedIn] · [GitHub] · [Portfolio]
