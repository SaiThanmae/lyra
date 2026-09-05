"""
Lyra Orchestrator Agent (ADK).

Receives a user request, decides which sub-agent(s) to invoke,
and assembles the final response.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool

from .ingest_agent import ingest_agent
from .analysis_agent import analysis_agent
from .embedding_agent import embedding_agent
from .lineage_agent import lineage_agent
from .discovery_agent import discovery_agent

SYSTEM_INSTRUCTION = """
You are Lyra's Orchestrator — the primary intelligence of a platform for
culturally sustainable poetry preservation and analysis.

You have access to five specialist sub-agents:
- ingest_agent:     store a new poem into the corpus
- analysis_agent:   analyse a poem's meter, form, tone, themes, and cultural context
- embedding_agent:  generate and store a semantic embedding for a poem
- lineage_agent:    detect stylistic ancestors and influence networks
- discovery_agent:  find semantically similar poems and produce recommendations

Determine the user's intent and delegate to the correct agent(s).
Always respond in clear, scholarly language that respects the literary nature
of the content. Never reduce a poem to numbers alone — pair every metric with
a human-readable interpretation.
"""


def build_orchestrator() -> LlmAgent:
    return LlmAgent(
        name="lyra_orchestrator",
        model="gemini-1.5-pro",
        instruction=SYSTEM_INSTRUCTION,
        tools=[
            agent_tool.AgentTool(agent=ingest_agent),
            agent_tool.AgentTool(agent=analysis_agent),
            agent_tool.AgentTool(agent=embedding_agent),
            agent_tool.AgentTool(agent=lineage_agent),
            agent_tool.AgentTool(agent=discovery_agent),
        ],
    )


orchestrator = build_orchestrator()
