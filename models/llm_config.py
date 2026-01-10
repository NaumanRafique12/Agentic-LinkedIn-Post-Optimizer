from langchain_openai import ChatOpenAI

# Generator: creative but grounded
generator_llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.6,
)

# Evaluator: strict, consistent judgment
evaluator_llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.0,
)

# Optimizer: precise rewriting under constraints
optimizer_llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.3,
)
