from typing import TypedDict, Literal, List, Dict, Any


class LinkedInPostState(TypedDict):
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

    draft_post: str

    review_decision: Literal["accept", "revise"]
    review_feedback: str
    quality_score: int

    iteration_count: int
    max_iterations: int

    history: List[Dict[str, Any]]
