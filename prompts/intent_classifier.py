from typing import Literal
from graph.costs import charge_cost
from pydantic import BaseModel, Field
from models.llm_config import intent_classifier_llm
from graph.state import LinkedInPostState


class IntentOutput(BaseModel):
    prompt_intent: Literal[
        "TECH_THOUGHT_LEADERSHIP",
        "PROOF_OF_WORK"
    ] = Field(description="The intent of the LinkedIn post idea")


def intent_classifier(state: LinkedInPostState) -> LinkedInPostState:
    """
    Classifies the intent of the LinkedIn post idea
    and stores it in the agent state.
    """

    structured_llm = intent_classifier_llm.with_structured_output(IntentOutput)

    prompt = f"""
    You are classifying a LinkedIn post idea.

    Choose exactly ONE intent from the following options:

    1. TECH_THOUGHT_LEADERSHIP
      - System-level insights
      - Opinions, tradeoffs, failure modes
      - Generalized lessons beyond one build

    2. PROOF_OF_WORK
      - Something was built, tested, or implemented
      - Mentions experiments, repositories, results, or learnings
      - Concrete execution and outcomes

    Post idea:
    \"\"\"
    {state["topic"]}
    \"\"\"

    Return only the structured output.
    """
    
    charge_cost(state, "intent_classifier")
    result: IntentOutput = structured_llm.invoke(prompt)

    # Update state immutably
    state["intent"] = result.prompt_intent

    return state
