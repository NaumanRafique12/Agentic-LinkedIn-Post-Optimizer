
from graph.state import LinkedInPostState


# ---- Proof-of-Work reference snippets (style + density only) ----

PROOF_OF_WORK_REFERENCES = [
    """
A system appeared performant but failed subtly after upstream changes.
The root issue was optimizing for speed without correctness over time.
Versioned caches and TTL-based invalidation made behavior predictable.
Lesson: production reliability is enforced through system semantics, not models.
""",
    """
Repeated queries caused unnecessary recomputation across the RAG pipeline.
Layered semantic caches eliminated redundant execution paths.
Miss-only execution ensured expensive components ran only when required.
Result: order-of-magnitude latency reduction without changing models.
""",
    """
Vector retrieval became the bottleneck once embedding latency was optimized.
A single large index limited parallelism and increased ANN traversal cost.
Sharding the vector store enabled faster search and horizontal scaling.
Outcome: retrieval latency dropped significantly through shard-aware routing.
"""
]


# ---- Tech Thought Leadership reference snippets (patterns only) ----

TECH_THOUGHT_LEADERSHIP_REFERENCES = [
    """
Many AI systems fail not due to weak prompts but due to fragile infrastructure.
Routing errors, stale data, or unreliable search cause confident hallucinations.
Agents amplify system weaknesses rather than fixing them.
Insight: robustness comes from boring, deterministic system design.
""",
    """
Engineers often over-invest in models while under-investing in observability.
Latency, failures, and correctness degrade silently without proper metrics.
Production AI success depends on monitoring, fallbacks, and debuggability.
Conclusion: system design matters more than algorithmic novelty.
""",
    """
Learning AI engineering is less about theory depth and more about end-to-end ownership.
Key challenges arise in orchestration, latency management, and failure handling.
The ability to swap components without downtime defines system maturity.
Lesson: shipping reliable systems beats mastering isolated techniques.
"""
]


def reference_retriever(state: LinkedInPostState) -> LinkedInPostState:
    """
    Attaches intent-specific reference intelligence to the state.
    References are used for style, density, and reasoning patterns only.
    """

    if state["intent"] == "PROOF_OF_WORK":
        state["references"] = PROOF_OF_WORK_REFERENCES

    elif state["intent"] == "TECH_THOUGHT_LEADERSHIP":
        state["references"] = TECH_THOUGHT_LEADERSHIP_REFERENCES

    else:
        state["references"] = []

    return state
