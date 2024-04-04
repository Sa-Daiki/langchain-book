import os

import streamlit as st
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent, load_tools
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)

load_dotenv()

def create_agent_executor(callback):
  chat = ChatOpenAI(
    model_name=os.environ["OPENAI_API_MODEL"],
    temperature=os.environ["OPENAI_API_TEMPERATURE"],
    streaming=True
  )
  
  prompt_template = ChatPromptTemplate.from_template(
    "{input}"
  )
  tools = load_tools(['ddg-search', 'wikipedia'])
  ## prompt_templateをhubから取得している例しかないため渡し方がわからない
  ## localでPromptTemplateを適切に作成する方法が不明
  agent = create_react_agent(chat, tools, prompt=prompt_template)
  return AgentExecutor(agent=agent, tools=tools, callbacks=[callback])


st.title("langchain-streamlit-app")

if "messages" not in st.session_state:
  st.session_state.messages = []
  
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

prompt = st.chat_input("Wht is up?")

if prompt:
  st.session_state.messages.append({"role": "user", "content": prompt})
  
  with st.chat_message("user"):
    st.markdown(prompt)
    
  with st.chat_message("assistant"):
    # chat = ChatOpenAI(
    #   model_name=os.environ["OPENAI_API_MODEL"],
    #   temperature=os.environ["OPENAI_API_TEMPERATURE"],
    # )
    # messages = [HumanMessage(content=prompt)]
    # response = chat(messages)
    callback = StreamlitCallbackHandler(st.container())
    agent_executor = create_agent_executor(callback=callback)
    response = agent_executor.invoke({input: prompt})
    st.markdown(response.content)
    
  st.session_state.messages.append({"role": "assistant", "content": response})
  
