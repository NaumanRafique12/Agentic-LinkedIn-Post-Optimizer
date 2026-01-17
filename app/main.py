from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import PlainTextResponse
from typing import Dict, Any, Literal, Optional
from graph.workflow import linkedin_post_workflow


app = FastAPI(
    title="Agentic LinkedIn Post Optimizer",
    description=(
        "Automates intent-aware, style-controlled, "
        "proof-of-work-safe LinkedIn post optimization using LangGraph"
    ),
    version="1.1.0",
)


# ---------- API SCHEMAS ----------

class PostRequest(BaseModel):
    topic: str = Field(..., description="User-provided content or claim")
    max_iterations: int = Field(3, ge=1, le=8)

    communication_style: Literal[
        "ENGINEERING_DIRECT",
        "VIRAL_ENGINEER",
        "STORY_DRIVEN",
    ] = Field(
        "VIRAL_ENGINEER",
        description="Controls how the post is framed, not what facts are allowed",
    )


class PostResponse(BaseModel):
    final_post: str
    iterations_used: int
    final_score: int

    # NEW: surfaced for transparency
    change_summary: Optional[str]


# ---------- STATE INITIALIZATION ----------

def build_initial_state(request: PostRequest) -> Dict[str, Any]:
    """
    Explicitly initialize all fields used by the agent graph.
    Control variables live here; agents only modify them.
    """
    return {
        # -----------------
        # User input
        # -----------------
        "topic": request.topic,
        "communication_style": request.communication_style,

        # -----------------
        # Control flow
        # -----------------
        "iteration_count": 0,
        "max_iterations": request.max_iterations,

        # -----------------
        # Agent-populated fields
        # -----------------
        "intent": None,
        "references": [],
        "draft_post": "",
        "review_feedback": "",
        "quality_score": 0,

        # -----------------
        # Focus control (NEW)
        # -----------------
        # Selected once by evaluator at iteration 0
        "frozen_focus_factors": [],

        # Actively optimized factors (subset of frozen)
        "active_focus_factors": [],

        # Graduation threshold (system-level config)
        "focus_graduation_threshold": 8,
         
        # best iteration
        "best_iteration": None,

        # -----------------
        # Diagnostics
        # -----------------
        "history": [],
        "review_feedback_history": [],
        "iteration_focus_history": [],
        "change_summary": None,
    }



# ---------- ENDPOINTS ----------

@app.post("/optimize", response_model=PostResponse)
def optimize_linkedin_post(request: PostRequest):
    """
    Runs the full agentic loop:
    Intent → References → Generate → Evaluate → Optimize → Summarize
    """

    initial_state = build_initial_state(request)

    final_state = linkedin_post_workflow.invoke(
        initial_state,
        config={
            "tags": ["agentic-linkedin-post-optimizer"],
            "metadata": {
                "intent": initial_state["intent"],
                "communication_style": initial_state["communication_style"],
                "max_iterations": initial_state["max_iterations"],
            },
        },
    )

    # Picking up the best state post and scores
    best = final_state.get("best_iteration")

    final_post = (
        best["draft_post"]
        if best is not None
        else final_state["draft_post"]
    )

    final_score = (
        best["quality_score"]
        if best is not None
        else final_state.get("quality_score", 0)
    )
    return {
        "final_post": final_post,
        "iterations_used": final_state["iteration_count"],
        "final_score": final_score,
        "review_decision": "accept" if final_score >= 39 else "revise",
        "change_summary": final_state.get("change_summary"),
    }


@app.post("/optimize/text", response_class=PlainTextResponse)
def optimize_linkedin_post_text(request: PostRequest):
    """
    Returns only the final LinkedIn post text,
    formatted exactly as it should be published.
    """

    initial_state = build_initial_state(request)
    final_state = linkedin_post_workflow.invoke(initial_state)
    # Picking up the best state post and scores
    best = final_state.get("best_iteration")

    final_post = (
        best["draft_post"]
        if best is not None
        else final_state["draft_post"]
    )

    return final_post
