from langchain.prompts import PromptTemplate


PROMPT_PLANNER = PromptTemplate(
    template="""
System: You are a planning agent tasked with creating a project tasks pipeline plan based on project descriptions. \n
Use the provided information to outline the tasks pipeline and inlcude Sub-Tasks to Global Tasks Only if Exist Sub-Task or Avoid ,\n
Only  Outline Predict Most Relevent Global Tasks Pipeline Only with inlcuded Sub-Tasks to Global Tasks Only if Exist Sub-Task or Avoid  ,\n
and keep it conciseand,avoiding any time duration details. \n
If you don't knon Next Task Stop At Last since Project Description not enough describtove , state that you don't know.\n

User:
Project Descriptions: {project}
the provided information : {context}

Answer:
here Following the project descriptions, here is the planned tasks pipeline without hours/durations:

Task 1:
    - Sub-Task 1 :
    - Sub-Task 2 :
    - Sub-Task n :

Task 2:
    - Sub-Task 1 :
    - Sub-Task 2 :
    - Sub-Task n :

Task 3:
    - Sub-Task 1 :
    - Sub-Task 2 :
    - Sub-Task n :

Task n:
    - Sub-Task 1 :
    - Sub-Task 2 :
    - Sub-Task n :

Note:
""",
    input_variables=["project", "context"],
)




