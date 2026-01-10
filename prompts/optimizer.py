from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import LinkedInPostState
from models.llm_config import optimizer_llm


def optimize_linkedin_post(state: LinkedInPostState) -> LinkedInPostState:
    messages = [
        SystemMessage(
            content=(
                "You refine LinkedIn posts written by senior AI engineers. "
                "You increase clarity and density while preserving real-world credibility."
            )
        ),
        HumanMessage(
            content=f"""
Revise the post using the feedback below.

Feedback:
{state["review_feedback"]}

Current Draft:
\"\"\"
{state["draft_post"]}
\"\"\"

REQUIRED FINAL OUTPUT FORMAT (must follow exactly):

[One strong opening line]

1) ...
2) ...
3) ...
4) ...
5) ...

#hashtags

STRICT ENFORCEMENT RULES:
- Exactly ONE opening line.
- Exactly FIVE numbered points (1–5).
- Each numbered point must be 2–3 lines long.
- Increase information density without adding fluff.
- Ensure each point reflects cause → effect → engineering decision.
- Rewrite vague statements into concrete system behavior.
- Do NOT split or merge points.
- Do NOT turn points into essays.
- Remove blog-style, academic, or neutral explainer phrasing.
- Remove any questions or engagement bait.
- Add 3–5 relevant hashtags ONLY at the end.
- Plain text only. No markdown.

The final output must be publish-ready for LinkedIn.
"""
        ),
    ]

    response = optimizer_llm.invoke(messages).content

    return {
        "draft_post": response,
        "iteration_count": state["iteration_count"] + 1,
    }
