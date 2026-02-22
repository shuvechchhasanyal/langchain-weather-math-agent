# 🌤️ 🧮 LangChain Weather & Math Agent

A robust, local AI assistant powered by LangChain and Groq (Llama 3.3). This agent implements a ReAct (Reason + Act) loop to intelligently handle user queries about weather and mathematics using live tools.

---

## ✨ Features

- **Modern Orchestration:** Uses `langchain.create_agent` for stable tool-calling.

- **Zero-Auth Weather Tool:** Integrates the Open-Meteo API to fetch coordinates and weather data without requiring an API key.

- **On-the-Fly Calculator:** A dynamic math tool that evaluates Python-based expressions using a calculator tool.

- **Diagnostic Streaming:** Built-in real-time monitoring that shows the agent's internal state, tool calls, and logic flow as it happens.

- **Infinite Loop Protection:** Optimized system prompting to prevent the model from redundant tool execution.

---

## 🛠️ Prerequisites

- Python 3.12+
- A Groq API Key (Get one at https://console.groq.com)

---

## 🚀 Installation & Setup

### Clone the Repository

```bash
git clone <your-repo-link>
cd Weather-news-tools
```

### Setup virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Install requirements

```bash
pip install -r requirements.txt
```
### Configure environment variables
Create a .env file in the root directory:

```bash
GROQ_API_KEY= "your_groq_api_key_here"
```

## 💻 Usage

Launch the agent via your terminal:
```bash
python pipeline.py
```

## 🧪 Example Queries

Weather:
"What is the weather in New York?"

Math:
"What is the square root of 144 plus 50?"

Hybrid:
"What's the temperature in Bengaluru, and if I multiply that number by 2, what do I get?"

## 🏗️ Architecture

The agent follows a cyclic graph pattern. When a user sends a message, the LLM determines if a tool is needed. If so, it halts text generation, triggers the tool, and uses the tool's output to formulate a final response.

## 📜 Dependencies

langchain — Core agent framework

langchain-groq — High-speed inference for Llama 3.3

requests — For interacting with the Open-Meteo API

python-dotenv — For secure environment variable management