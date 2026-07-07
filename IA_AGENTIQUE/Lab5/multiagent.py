#Définition des outils
from langchain.tools import tool

@tool
def square_root(x: float) -> float:
    """
    Calculate the square root of a number.

    Args:
        x (float): The input number.

    Returns:
        float: The square root of the input number.
    """
    return x ** 0.5


@tool
def square(x: float) -> float:
    """
    Calculate the square of a number.

    Args:
        x (float): The input number.

    Returns:
        float: The square of the input number.
    """
    return x ** 2

#Création des sous agents
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

subagent_1 = create_agent(
model='gpt-5-nano',
tools=[square_root]
)

subagent_2 = create_agent(
model='gpt-5-nano',
tools=[square]
)

#Créer l’agent principal
# Tool pour appeler le sous-agent 1
from langchain.messages import HumanMessage


@tool
def call_subagent_1(x: float) -> str:
    """
    Call subagent 1 to calculate the square root of a number.

    Args:
        x (float): The input number.

    Returns:
        str: The result returned by subagent 1.
    """
    response = subagent_1.invoke(
        {
            "messages": [
                HumanMessage(
                    content=f"Calculate the square root of {x}"
                )
            ]
        }
    )

    return response["messages"][-1].content


# Tool pour appeler le sous-agent 2
@tool
def call_subagent_2(x: float) -> str:
    """
    Call subagent 2 to calculate the square of a number.

    Args:
        x (float): The input number.

    Returns:
        str: The result returned by subagent 2.
    """
    response = subagent_2.invoke(
        {
            "messages": [
                HumanMessage(
                    content=f"Calculate the square of {x}"
                )
            ]
        }
    )

    return response["messages"][-1].content


# Création de l'agent principal
main_agent = create_agent(
    model="gpt-5-nano",
    tools=[
        call_subagent_1,
        call_subagent_2,
    ],
    system_prompt=(
        "You are a helpful assistant that can delegate tasks to "
        "specialized subagents. "
        "Use 'call_subagent_1' to calculate the square root of a number "
        "and 'call_subagent_2' to calculate the square of a number."
    ),
)
