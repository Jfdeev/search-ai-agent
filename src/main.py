from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schema import AgentResponse

load_dotenv()

tools = [TavilySearch()]
llm = ChatGoogleGenerativeAI(
    temperature=0.7,
    model="gemini-1.5-flash",
)
# Pega um prompt de reação do hub do langchain, o hub serve para compartilhar projetos entre a comunidade
react_prompt = hub.pull("hwchase17/react")
output_parser = PydanticOutputParser(pydantic_object=AgentResponse)
react_prompt_with_validation = PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    input_variables=["input", "agent_scratchpad", "tool_names"]
).partial(format_instructions = output_parser.get_format_instructions())


# Mecanismo de raciocinio seguindo as normas do Agente de Reação
agent = create_react_agent(
    llm=llm, 
    tools=tools, 
    #prompt=react_prompt
    prompt=react_prompt_with_validation,
    )
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
extract_output = RunnableLambda(lambda x: x["output"])
parse_output = RunnableLambda(lambda x: output_parser.parse(x))
chain = agent_executor | extract_output | parse_output


def main():
    result = chain.invoke(
        input={
            "input": 'Task: Search LinkedIn for 3 job postings for "AI Engineer" roles that mention LangChain and show the job descriptions.',
        }
    )
    print(result)


if __name__ == "__main__":
    main()
