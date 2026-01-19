from typing import TypedDict, Literal, List, Dict, Any, Optional, Annotated
from operator import add


class LinkedInPostState(TypedDict):
    # -----------------
    # User input
    # -----------------
    topic: str

    intent: Literal[
        "TECH_THOUGHT_LEADERSHIP",
        "PROOF_OF_WORK",
    ]

    communication_style: Literal[
        "ENGINEERING_DIRECT",
        "VIRAL_ENGINEER",
        "STORY_DRIVEN",
    ]

    # -----------------
    # Draft content
    # -----------------
    draft_post: str

    # -----------------
    # Evaluation outputs
    # -----------------
    review_feedback: str
    quality_score: int

    # Per-dimension evaluator scores
    scores: Dict[str, int]

    # -----------------
    # Focus control (NEW)
    # -----------------
    # Weakest dimensions selected once at iteration 0
    frozen_focus_factors: List[str]

    # Actively optimized dimensions (subset of frozen + optional replacements)
    active_focus_factors: List[str]

    # Score at which a dimension is considered "good enough"
    focus_graduation_threshold: int

    # -----------------
    # Control flow
    # -----------------
    iteration_count: int
    max_iterations: int

    # -----------------
    # History & diagnostics
    # -----------------
    history: List[Dict[str, Any]]

    # Accumulates evaluator feedback across iterations
    review_feedback_history: Annotated[List[str], add]

    # Tracks focus-factor scores per iteration (trajectory analysis)
    iteration_focus_history: Annotated[List[Dict[str, Any]], add]

    # Best iteration safety
    best_iteration: Optional[Dict[str, Any]]

    # User-facing explanation of what changed (computed at end)
    change_summary: Optional[str]
    
    # Cost Metrics per run
    run_metrics: Dict[str, Any]
