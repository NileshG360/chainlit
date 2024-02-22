import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.chains import LLMChain
from receive_input import on_boarding_questions
from router_helper import router_chain_prompt
import chainlit as cl
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) 
openai.api_key = os.environ['OPENAI_API_KEY']




@cl.on_chat_start
async def on_chat_start():
    prompt = await on_boarding_questions()
    chain = await router_chain_prompt(prompt)
    cl.user_session.set("chain", chain)



@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("chain")  
    res = chain.run(message.content)
    await cl.Message(content=res).send()

