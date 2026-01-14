from typing import TypedDict, Literal, List, Dict, Any, Optional, Annotated
from operator import add

class LinkedInPostState(TypedDict):
    # User input
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

    # Draft content
    draft_post: str

    # Evaluation
    review_decision: Literal["accept", "revise"]
    review_feedback: str
    quality_score: int

    # NEW: explicit evaluator signals (used later for diffing)
    scores: Dict[str, int]

    # Control flow
    iteration_count: int
    max_iterations: int

    # History
    history: List[Dict[str, Any]]

    # Top factors to improve
    focus_factors: List[str]
     
    # Stores the review feedback over iterations
    review_feedback_history: Annotated[List[str],add]

    # NEW: user-facing explanation of what changed
    change_summary: Optional[str]
