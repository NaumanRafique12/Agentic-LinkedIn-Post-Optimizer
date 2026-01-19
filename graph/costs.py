
ESTIMATED_TOKEN_COSTS = {
    "intent_classifier": 500,
    "generator": 1000,
    "evaluator": 1200,
    "optimizer": 2500,
    "summarizer": 700,
    }

def charge_cost(state, agent_name: str):
    cost = ESTIMATED_TOKEN_COSTS[agent_name]

    state["run_metrics"]["estimated_tokens_used"] += cost
    state["run_metrics"]["token_budget_remaining"] -= cost
    state["run_metrics"]["llm_calls"][agent_name] += 1

    if state["run_metrics"]["token_budget_remaining"] < 0:
        state["run_metrics"]["stop_reason"] = "token_budget_exceeded"
