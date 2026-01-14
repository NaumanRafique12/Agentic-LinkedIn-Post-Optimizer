from pydantic import BaseModel
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import LinkedInPostState
from models.llm_config import change_summary_llm


class ChangeSummary(BaseModel):
    summary: str


structured_summary_llm = change_summary_llm.with_structured_output(ChangeSummary)


def summarize_changes(state: LinkedInPostState) -> LinkedInPostState:
    history = state.get("review_feedback_history",[])

    if len(history) < 3:
        return {"change_summary": None}

    messages = [
        SystemMessage(
            content=(
                "You summarize editorial changes across iterations.\n"
                "Do NOT rescore or re-evaluate.\n"
                "Do NOT introduce new claims.\n"
                "Only describe what improved, weakened, or stayed the same."
            )
        ),
        HumanMessage(
            content=f"""
        Initial feedback:
        {history[0]}

        Final feedback:
        {history[-1]}

        Focus dimensions:
        {state["focus_factors"]}

        Summarize the changes clearly for a user.
        """
                ),
    ]

    response = structured_summary_llm.invoke(messages)

    return {"change_summary": response.summary}
