import os
import urllib

import streamlit as st
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from config import ConfigLLM

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
USERNAME = os.getenv("USERNAME", "")
PASSWORD = os.getenv("PASSWORD", "")
uri = uri = (
    "mongodb+srv://"
    + urllib.parse.quote_plus(USERNAME)
    + ":"
    + urllib.parse.quote_plus(PASSWORD)
    + "@cluster0.k3qwm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
client = MongoClient(uri)
collection = client["llm_task"]["purchase_order"]

prompt_template_for_creating_query = (
    """
    You are an expert in crafting NoSQL queries for MongoDB with 10 years of experience, particularly in MongoDB. 
    I will provide you with the table_schema and schema_description in a specified format. 
    Your task is to read the user_question, which will adhere to certain guidelines or formats, and create a NOSQL MongoDb pipeline accordingly.

    Table schema:"""
    + ConfigLLM.TABLE_SCHEMA
    + """
    Schema Description: """
    + ConfigLLM.SCHEMA_DESCRIPTION
    + """
    
    Here are some example:
    Input: what is Total number of orders created during 2010 to 2013
    Output: {json_ex_string_1}

    Input: what is sum of all values in total price field
    Output: {json_ex_string_2}

    Input: what is Identification of the quarter with the highest spending
    Output: {json_ex_string_3}
    
    Input: Total spending grouped by Acquisition Type
    Output: {json_ex_string_4}

    Note: You have to just return the python pipeline query nothing else. Don't return any additional text with the python pipeline query.
    Input: {user_question}
    """
)
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.7,
    max_tokens=4000,
)


st.title("talk to MongoDB")
st.write("ask anything and get answer")
input = st.text_area("enter your question here")


query_creation_prompt = PromptTemplate(
    template=prompt_template_for_creating_query,
    input_variables=[
        "user_question",
        "json_ex_string_1",
        "json_ex_string_2",
        "json_ex_string_3",
    ],
)

llmchain = LLMChain(llm=llm, prompt=query_creation_prompt, verbose=True)

if input is not None:
    button = st.button("Submit")
    if button:
        response = llmchain.invoke(
            {
                "user_question": input,
                "json_ex_string_1": ConfigLLM.FEW_SHOT_EXAMPLE_1,
                "json_ex_string_2": ConfigLLM.FEW_SHOT_EXAMPLE_2,
                "json_ex_string_3": ConfigLLM.FEW_SHOT_EXAMPLE_3,
                "json_ex_string_4": ConfigLLM.FEW_SHOT_EXAMPLE_4,
            }
        )
        pipeline = eval(response["text"])
        results = collection.aggregate(pipeline)
        for result in results:
            st.write(result)
