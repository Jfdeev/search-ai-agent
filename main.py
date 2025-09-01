
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch

load_dotenv()

tools = [TavilySearch()]
llm = ChatGoogleGenerativeAI(
    temperature=0.7,
    model="gemini-1.5-flash",
)
# Pega um prompt de reação do hub do langchain, o hub serve para compartilhar projetos entre a comunidade
react_prompt = hub.pull("hwchase17/react")
# Mecanismo de raciocinio seguindo as normas do Agente de Reação
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
chain = agent_executor

def main():
    result = chain.invoke(
        input={
            "input": "search for 3 job postings for ai engineers using langchain on linkedin and list their details"
        }
    )
    print(result)


if __name__ == "__main__":
    main()
