from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from typing import List
import openai
import os
import json
import pandas as pd
import re
from services.audience_filtration.prompt_templates import text2sql_prompt

# Setting up OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_sql_query(user_query, pydantic_output):
    llm = ChatOpenAI(
            model="gpt-4-turbo",#"gpt-3.5-turbo-16k-0613",
            openai_api_key=openai.api_key,
            temperature=0,
            streaming=True
        )
    
    prompt = PromptTemplate(
        template=text2sql_prompt,
        input_variables=["user_query", "entities"],
    )
    
    chain = prompt | llm
    
    llm_output = chain.invoke({"user_query": user_query, "entities": pydantic_output})
    
    output = llm_output.content

    return output