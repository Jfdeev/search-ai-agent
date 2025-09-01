
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch

load_dotenv()

tools = [TavilySearch]

def main():
    print("Hello from search-ai-agent!")


if __name__ == "__main__":
    main()
