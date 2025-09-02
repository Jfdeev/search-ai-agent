from typing import List

from pydantic import BaseModel, Field


# Base Model serve para modelar o nosso schema
class Source(BaseModel):
    """Schema for a source used by the agent"""

    url: str = Field(description="The URL of the source")


class AgentResponse(BaseModel):
    """Schema for the agent's response with answer to the query"""

    answer: str = Field(description="The agent answer to the query")
    sources: List[Source] = Field(
        default_factory=list,
        description="The list of sources used to generate the answer",
    )
