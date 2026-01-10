from langgraph.graph import StateGraph, START, END
from graph.state import LinkedInPostState
from prompts.generator import generate_linkedin_post
from prompts.evaluator import evaluate_linkedin_post
from prompts.optimizer import optimize_linkedin_post

def should_continue(state: LinkedInPostState):
    if state["review_decision"] == "accept":
        return END
    if state["iteration_count"] >= state["max_iterations"]:
        return END
    if state["quality_score"] >= 42:
        return END
    return "optimize_linkedin_post"

graph = StateGraph(LinkedInPostState)

graph.add_node("generate_linkedin_post", generate_linkedin_post)
graph.add_node("evaluate_linkedin_post", evaluate_linkedin_post)
graph.add_node("optimize_linkedin_post", optimize_linkedin_post)

graph.add_edge(START, "generate_linkedin_post")
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
