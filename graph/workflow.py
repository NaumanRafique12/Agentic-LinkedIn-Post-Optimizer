from langgraph.graph import StateGraph, START, END

from graph.state import LinkedInPostState

from prompts.intent_classifier import intent_classifier
from prompts.reference_retriever import reference_retriever
from prompts.generator import generate_linkedin_post
from prompts.evaluator import evaluate_linkedin_post
from prompts.optimizer import optimize_linkedin_post


def should_continue(state: LinkedInPostState):
    # Hard stop if accepted with sufficient quality
    if state["review_decision"] == "accept" and state["quality_score"] >= 42:
        return END

    # Stop if max iterations reached
    if state["iteration_count"] >= state["max_iterations"]:
        return END

    # Otherwise, optimize and retry
    return "optimize_linkedin_post"


graph = StateGraph(LinkedInPostState)

# ---- Nodes ----
graph.add_node("intent_classifier", intent_classifier)
graph.add_node("reference_retriever", reference_retriever)
graph.add_node("generate_linkedin_post", generate_linkedin_post)
graph.add_node("evaluate_linkedin_post", evaluate_linkedin_post)
graph.add_node("optimize_linkedin_post", optimize_linkedin_post)

# ---- Edges ----
graph.add_edge(START, "intent_classifier")
graph.add_edge("intent_classifier", "reference_retriever")
graph.add_edge("reference_retriever", "generate_linkedin_post")
graph.add_edge("generate_linkedin_post", "evaluate_linkedin_post")

graph.add_conditional_edges(
    "evaluate_linkedin_post",
    should_continue,
    {
        "optimize_linkedin_post": "optimize_linkedin_post",
        END: END,
    },
)

graph.add_edge("optimize_linkedin_post", "evaluate_linkedin_post")

linkedin_post_workflow = graph.compile()
