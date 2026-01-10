from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import LinkedInPostState
from models.llm_config import generator_llm


def generate_linkedin_post(state: LinkedInPostState) -> LinkedInPostState:
    messages = [
        SystemMessage(
            content=(
                "You are a senior AI engineer writing in public. "
                "You share dense, practical lessons from building production systems, "
                "similar to how OpenAI or LangChain engineers post on LinkedIn."
            )
        ),
        HumanMessage(
            content=f"""
Write a LinkedIn post on the topic below.

Topic:
{state["topic"]}

REQUIRED OUTPUT FORMAT (must follow exactly):

[One strong, scroll-stopping opening line]

1) First point describing a concrete failure or limitation observed in practice, why it occurred, and why it mattered
2) Second point explaining a technical tradeoff discovered during implementation and its side effects
3) Third point describing a specific engineering action taken to address the issue and what changed as a result
4) Fourth point explaining downstream impact on reliability, latency, user trust, or system behavior
5) Fifth point summarizing the key system-level lesson learned

DENSITY & LENGTH RULES (VERY IMPORTANT):
- Each numbered point must be 2–3 lines in length.
- Each point must include cause → effect → engineering insight.
- Pack real technical detail into each point without storytelling.
- Avoid generic phrases that could apply to any AI system.
- Assume the reader is technical; do not explain basics.

STRICT RULES:
- Use first-person or experiential language ("I", "we", "in production").
- Exactly FIVE numbered points (1–5).
- Do NOT write definitions or textbook explanations.
- Do NOT write blog-style or marketing content.
- Do NOT include hashtags yet.
- Plain text only. No markdown.

This should read like a senior engineer compressing real production experience into dense insights.
"""
        ),
    ]

    response = generator_llm.invoke(messages).content

    return {
        "draft_post": response
    }
