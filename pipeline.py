import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")

# ----Loading system prompt-----------------

base_dir = os.path.dirname(os.path.abspath(__file__))
prompt_path = os.path.join(base_dir, "prompts", "system_prompt.md")

with open(prompt_path, "r", encoding="utf-8") as f:
    system_prompt = f.read()


# --- 1. Tools Definition ---

@tool
def get_weather(location: str) -> str:
    """Fetch current weather for a given city name."""
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={quote(location)}&count=1&language=en&format=json"
    
    # Added Error Handling so the tool doesn't crash silently
    try:
        geo_res = requests.get(geo_url, timeout=5).json()
    except Exception as e:
        return f"API Connection Error: Could not reach Open-Meteo. Details: {str(e)}"
    
    if "results" not in geo_res:
        return f"Could not find coordinates for '{location}'. The city might not be in the database."
    
    loc_data = geo_res["results"][0]
    lat, lon = loc_data["latitude"], loc_data["longitude"]

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m"
    
    try:
        w_res = requests.get(weather_url, timeout=5).json()
    except Exception as e:
         return f"API Connection Error: Could not fetch weather data. Details: {str(e)}"
    
    current = w_res.get("current", {})
    temp = current.get("temperature_2m")
    humidity = current.get("relative_humidity_2m")
    
    return f"In {loc_data['name']}, it is currently {temp}°C with {humidity}% humidity."

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression. Use this for any math problems."""
    try:
        # Note: eval() is used for simplicity in local testing. 
        # In a public production app, use a safer math library like `numexpr`.
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

# --- 2. Agent Initialization ---

# Lowering temperature to 0 forces the LLM to follow the tool strictness
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
tools = [get_weather, calculator]


agent = create_agent(llm, tools, system_prompt=system_prompt)

# --- 3. Execution ---

user_input = input("Ask me something (weather/maths): ")
inputs = {"messages": [("user", user_input)]}

print("\n--- Diagnostic Stream ---")
# This will print the internal thought process, the tool call, and the result!
for chunk in agent.stream(inputs, stream_mode="values"):
    chunk["messages"][-1].pretty_print()