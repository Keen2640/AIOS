# AIOS — AI Agent Operating System 🤖

An LLM-powered AI agent system that converts natural language into structured actions and executes real tools on a local machine.

---

## 🚀 Features

- Converts natural language → structured JSON actions
- Executes real tools (Python, apps, web search)
- Modular tool execution system
- Extensible agent architecture
- Built with Gemini API

---

## 🧠 Architecture

User Input
   ↓
LLM (Gemini 2.5 Flash)
   ↓
JSON Action Parser
   ↓
Tool Router
   ↓
Execution Layer

---

## ⚙️ Supported Tools

- run_python → execute Python code
- open_app → open Mac applications
- search_web → browser automation
- general_response → safe fallback

---

## 🛠️ Setup

```bash
git clone https://github.com/yourusername/AIOS.git
cd AIOS

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt