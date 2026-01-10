from langchain_openai import ChatOpenAI

generator_llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.7,
)

evaluator_llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.1,
)

optimizer_llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.4,
)

