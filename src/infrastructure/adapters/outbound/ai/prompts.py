from langchain_core.prompts import (
  HumanMessagePromptTemplate,
  SystemMessagePromptTemplate,
)

SYSTEM_PROMPT = SystemMessagePromptTemplate.from_template(
  """You are a {level}-level {subject} professor. Your job is to create study plans for {level}-level students."""
)

GENERATE_STUDY_PLAN_PROMPT = HumanMessagePromptTemplate.from_template("""
Generate a study plan for {grade} year {level} students that include a list of topics with the materials the students can use to study them, such as books, scientific papers, or tutorials from recognized professionals in the field and an exam for each topic that includes a quiz and practice exercises.
You have access to an internet search tool as your primary means of gathering information.
## `internet_search`
Use this to run an internet search for a given query. You can specify the max number of results to return, the topic, and whether raw content should be included.
""")
