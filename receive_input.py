import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts.prompt import PromptTemplate
import chainlit as cl
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) 

async def on_boarding_questions():
    llm_model = os.environ['llm_model']
    client_input_parameter={}
    parameter_question = {'name':'What is your name?','system_name':"How would you like to address me?"}
    for question in parameter_question.keys():
        value = await cl.AskUserMessage(content=parameter_question[question], timeout=10).send()
        if value:
            value = value['output']
        client_input_parameter[question] = value
    client_input_parameter['temperature'] = 0
    
    relationship = await cl.AskActionMessage(
        content="Relationship are you looking for !",
        actions=[
            cl.Action(name="Girlfriend", value="Girlfriend", label="Girlfriend"),
            cl.Action(name="Friend", value="Friend", label="Friend"),
        ],
    ).send()

    if relationship:
        client_input_parameter['relationship']=relationship.get("value")
        if relationship.get("value") == "Girlfriend":
            client_input_parameter['tone'] = "flirty"
            client_input_parameter['temperature'] = 1
        if relationship.get("value") == "Friend":
            client_input_parameter['tone'] = "Mature"

    client_input_parameter['ageGroup'] = "Adult"
    ageGroup = await cl.AskActionMessage(
        content="What is your age group !",
        actions=[
            cl.Action(name="Teen", value="Teen", label="Teen"),
            cl.Action(name="Adult", value="Adult", label="Adult"),
        ],
    ).send()

    if ageGroup:
        client_input_parameter['ageGroup']=ageGroup.get("value")
    

    await cl.Message(content=f"Hello {client_input_parameter['name']}, What's up? ").send()
    
    introduction = f"""Consider your name is '{client_input_parameter['system_name']}' and user name is '{client_input_parameter['name']}'. " \
               The user belongs to age group '{client_input_parameter['ageGroup']}'. The system tone should be similar to '{client_input_parameter['tone']}' in nature."""

    prompt_message = f"""
        You're a chatbot—an automated service designed for seamless conversations with users. \
Your goal is to engage naturally without revealing your identity as a chatbot. \
Begin each interaction with a friendly greeting and ensure to include emojis to \
add warmth and expression. When encountering unexpected questions, \
take a moment to analyze before crafting a thoughtful and helpful response. \
Keep your responses concise and relevant. Remember to personalize your \
interaction by reading the user's introduction : {introduction}. Let's aim for memorable and enjoyable conversations!
the output response should always contain followup question.
    """
    model = ChatOpenAI(streaming=True,temperature=client_input_parameter['temperature'], model=llm_model)
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_message),
        ("human", "{input}"),
    ])
    return prompt


