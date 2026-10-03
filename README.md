# Under the Hood: LLM Agent Token Trace

This repository contains a minimal reproducible example designed to audit token accumulation, stateless execution loops, and framework overhead inside an LLM agent during tool invocation. 

It accompanies the technical article: **"The Hidden Token Multiplier: What Actually Happens Under the Hood of an LLM Agent?"**

## 📌 Overview

When building applications with LLM agents, it is easy to assume a linear workflow: `User ➔ Agent ➔ Tool ➔ Answer`. However, because Large Language Models are fundamentally stateless, the orchestration layer must manage multiple invocation turns—compounding the context window with every historical exchange.

This project demonstrates a single parallel tool-calling step using LangChain and `gpt-4o-mini`, tracking exactly how input and output tokens accumulate across multiple invocations.

## 🏗️ Architecture Flow

The agent handles requests via a two-phase execution cycle:
1. **LLM Call #1 (The Decision):** Receives the system instructions, user query, and tool schemas. It outputs a structured tool-calling payload instead of a final response.
2. **External Execution:** The application layer executes local functions (`get_stock_price` and `get_weather`) asynchronously.
3. **LLM Call #2 (The Synthesis):** The framework builds a new context window stacking the original prompt history, the model's intent, and the raw tool results, invoking the LLM a second time to produce the final answer.

## 📊 Token Accounting Summary

Based on a dual-intent test query (*"Stock price of APPL and temp of Newyork"*):

| Metric | LLM Call #1 | LLM Call #2 | Cumulative Total |
| :--- | :--- | :--- | :--- |
| **Input Tokens** | 134 | 258 | **392** |
| **Output Tokens** | 47 | 34 | **81** |
| **Total Tokens** | 181 | 292 | **473** |

## 📂 Project Structure

*   `main.py` — The core entry point that orchestrates the execution flow.
*   `trace_callback.py` — Custom LangChain callback handlers tracking granular token metadata.
*   `SimpleAIAgent_Tools_Tracing.py` — The encapsulated agent configuration and mock tool setups.
*   `pyproject.toml` & `uv.lock` — Workspace definition and deterministic dependency locks managed via `uv`.

## 🚀 Getting Started

This project uses **`uv`** for fast, deterministic Python package management. 

### 1. Installation

Clone this repository and sync the virtual environment with a single command:
```bash
git clone https://gitlab.com
cd llm-token-trace
uv sync
```

### 2. Environment Configuration

Copy the example environment file and add your OpenAI API key:
```bash
cp .env.example .env
```
Open your newly created `.env` file and populate your credentials:
```text
OPENAI_API_KEY=your-actual-api-key-here
```

### 3. Running the Trace Audit

Execute the agent workspace through the automated virtual environment runner:
```bash
uv run python main.py
```

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
