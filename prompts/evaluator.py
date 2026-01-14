from pydantic import BaseModel, Field
from typing import Literal, Dict, List
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import LinkedInPostState
from models.llm_config import evaluator_llm


class LinkedInPostReview(BaseModel):
    review_decision: Literal["accept", "revise"]

    hook_strength: int = Field(..., ge=0, le=10)
    factual_grounding: int = Field(..., ge=0, le=10)
    causal_clarity: int = Field(..., ge=0, le=10)
    interpretive_judgment: int = Field(..., ge=0, le=10)
    density: int = Field(..., ge=0, le=10)

    total_score: int = Field(..., ge=0, le=50)
    review_feedback: str


structured_evaluator = evaluator_llm.with_structured_output(
    LinkedInPostReview)


def evaluate_linkedin_post(state: LinkedInPostState) -> LinkedInPostState:
    intent = state["intent"]

    messages = [
        SystemMessage(
            content=(
                "You are a strict evaluator of LinkedIn posts written by senior AI engineers.\n\n"
                "GENERAL RULES:\n"
                "- Do NOT score formatting or bullet usage.\n"
                "- Evaluate clarity, credibility, and density of claims.\n\n"
                "PROOF_OF_WORK RULES:\n"
                "- All user-provided metrics MUST appear verbatim.\n"
                "- No inferred mechanisms allowed.\n"
                "- Bounded interpretation is REQUIRED for high scores.\n\n"
                "TECH THOUGHT LEADERSHIP RULES:\n"
                "- Exactly five conceptual sections expected.\n"
                "- No metrics allowed.\n"
            )
        ),
        HumanMessage(
    content=f"""
Review the LinkedIn post below.

Post:
\"\"\"
{state["draft_post"]}
\"\"\"

Score the post on the following dimensions (0–10 each):

1. Hook strength
2. Factual grounding
3. Cause → effect clarity
4. Interpretive judgment
5. Information density

Guidelines:
- Be strict and skeptical.
- Do NOT reward fluency alone.
- Penalize abstraction, redundancy, or vague claims.
- High scores should require exceptional clarity and sharpness.

Return ONLY the structured scores and feedback.
"""
)
,
    ]

    response = structured_evaluator.invoke(messages)

    scores: Dict[str, int] = {
        "hook_strength": response.hook_strength,
        "factual_grounding": response.factual_grounding,
        "causal_clarity": response.causal_clarity,
        "interpretive_judgment": response.interpretive_judgment,
        "density": response.density,
    }

    focus_factors = sorted(scores, key=scores.get)[:2]
    
    return {
        "review_decision": "accept" if response.total_score >= 42 else "revise",
        "review_feedback": response.review_feedback,
        "review_feedback_history": [response.review_feedback],
        "quality_score": response.total_score,
        "focus_factors": focus_factors,
        "history": state.get("history", [])
    }
