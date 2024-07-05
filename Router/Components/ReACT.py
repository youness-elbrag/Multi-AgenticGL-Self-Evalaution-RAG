from typing import Any, List, Optional
from langchain.agents.agent import AgentExecutor
# from langchain.agents.agent_toolkits.pandas.prompt import PREFIX, SUFFIX
from langchain.agents import ZeroShotAgent
from langchain.callbacks.base import BaseCallbackManager
from langchain.chains.llm import LLMChain
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from langchain_openai import ChatOpenAI




PREFIX = """
            You are working with a pandas dataframe in Python. The name of the dataframe is `df`.
            You should use the tools below to answer the question posed of you:
            
         """


    
SUFFIX = """
        This is the result of `print(df.head())`:
        {df}
        Begin!
        {chat_history}
        Question: {input}
        {agent_scratchpad}
        """

def ReACT_DataFrame_Agent(
    llm: ChatOpenAI,
    df: Any,
    callback_manager: Optional[BaseCallbackManager] = None,
    prefix: str = PREFIX,
    suffix: str = SUFFIX,
    memory = None ,
    input_variables: Optional[List[str]] = None,
    verbose: bool = False,
    return_intermediate_steps: bool = False,
    max_iterations: Optional[int] = 15,
    max_execution_time: Optional[float] = None,
    early_stopping_method: str = "force",
    **kwargs: Any,
) -> AgentExecutor:
    """Construct a pandas agent from an LLM and dataframe."""
    import pandas as pd

    if not isinstance(df, pd.DataFrame):
        raise ValueError(f"Expected pandas object, got {type(df)}")
    if input_variables is None:
        input_variables = ["df", "input", "agent_scratchpad"]
    tools = [PythonAstREPLTool(locals={"df": df})]
    

    prompt = ZeroShotAgent.create_prompt(
        tools, 
        prefix=PREFIX,
        suffix=SUFFIX, 
        input_variables=["df", "input", "chat_history", "agent_scratchpad"]
    )
    
    print(prompt)
    
    partial_prompt = prompt.partial(df=str(df.head()))
    
    llm_chain = LLMChain(
        llm=llm,
        prompt=partial_prompt,
        callback_manager=callback_manager,
    )
    
    tool_names = [tool.name for tool in tools]
    
    agent = ZeroShotAgent(
        llm_chain=llm_chain,
        allowed_tools=tool_names,
        callback_manager=callback_manager,
        **kwargs,
    )
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=verbose,
        return_intermediate_steps=return_intermediate_steps,
        max_iterations=max_iterations,
        max_execution_time=max_execution_time,
        early_stopping_method=early_stopping_method,
        callback_manager=callback_manager,
        memory = memory
    )
