import os
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain,RouterOutputParser
from langchain.prompts import PromptTemplate
from prompt_helper import *
from load_prompt_helper import prompt_infos
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import chainlit as cl
from langchain.schema import StrOutputParser
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) 

async def router_chain_prompt(default_Prompt):
    llm_model = os.environ['llm_model']
    llm = ChatOpenAI(temperature=0, model=llm_model)

    destination_chains = {}
    for p_info in prompt_infos:
        name = p_info["name"]
        prompt_template = p_info["prompt_template"]
        prompt = ChatPromptTemplate.from_template(template=prompt_template)
        chain = LLMChain(llm=llm, prompt=prompt)
        destination_chains[name] = chain  
        
    destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
    destinations_str = "\n".join(destinations)
    prompt_template = chatbot_prompt

    #PROMPT = PromptTemplate(input_variables=["input"], template=default_Prompt)
    #default_prompt = ChatPromptTemplate.from_template("{input}")
    default_chain = LLMChain(llm=llm, prompt=default_Prompt)
    #default_chain  = LLMChain(llm=llm, prompt=default_Prompt)

    router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
        destinations=destinations_str
    )
    router_prompt = PromptTemplate(
        template=router_template,
        input_variables=["input"],
        output_parser=RouterOutputParser(),
    )

    router_chain = LLMRouterChain.from_llm(llm, router_prompt)

    chain = MultiPromptChain(router_chain=router_chain, 
                            destination_chains=destination_chains, 
                            default_chain=default_chain, verbose=False
                            )
    return chain

