#Simple AI Agent Example

import requests
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from printMessage import print_agent_trace
from trace_callback import LLMTraceCallback

load_dotenv()

@tool('get_weather', description='Get the current weather for a given city', return_direct=False)
def get_weather(city: str) -> dict:
    """Get the weather for a given City."""
    try:
        geo = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        ).json()

        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]

        weather = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        ).json()
        print(str(weather["current_weather"]))
        return str(weather["current_weather"])
    except Exception as e:
        return {'error': str(e)}


@tool('get_stock_price', description='Get the current stock price for a company ticker', return_direct=False)
def get_stock_price(ticker: str) -> str:
    """Get real-time stock price (simulated)."""
    # Simulated - in real use, call an API like Alpha Vantage
    prices = {"AAPL": "$175.43", "GOOGL": "$139.82", "MSFT": "$378.91"}
    return prices.get(ticker.upper(), "Stock not found")


agent = create_agent(
    model= 'gpt-4o-mini', # Need OPEN_API_KEY and langchain[openai]
    tools =[get_weather, get_stock_price] ,
    system_prompt= "You are Smart Assistant." \
    "1. You MUST use the available tools to answer questions." \
    "2. If relevant tool is not available. Search on internet." \
    "3. If you can't search the internet, Explictily mention that and use your internal knowledge. " 
)

def run_agent():
    user_input = input("Enter your query: ")
    user_message = HumanMessage(content=user_input)

    trace = LLMTraceCallback()

    response = agent.invoke(
        {
            'messages': [user_message]
        },
        config={"callbacks": [trace]}  # Add callback to see tool calls
    )

    print_agent_trace(response)

# Allows running this file directly if needed
if __name__ == "__main__":
    run_agent()

