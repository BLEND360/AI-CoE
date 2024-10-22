from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from typing import List
import openai
import os
import json
import pandas as pd
import re
from services.audience_filtration.prompt_templates import pandas_filtration_prompt

# Setting up OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')


def get_pandas_filtration_output(user_query, pydantic_output):
    llm = ChatOpenAI(
            model="gpt-4-turbo",#"gpt-3.5-turbo-16k-0613",
            openai_api_key=openai.api_key,
            temperature=0,
            streaming=True
        )
    
    prompt = PromptTemplate(
        template=pandas_filtration_prompt,
        input_variables=["user_query", "entities", "dataframe_name"],
    )
    
    chain = prompt | llm
    
    llm_output = chain.invoke({"user_query": user_query, "entities": pydantic_output, "dataframe_name": 'customer_data'})
    
    output = llm_output.content

    return output

def extract_df_filter(input_text):
    pattern = r'python\n(.*?)(?=\n|$)'
    match = re.search(pattern, input_text, re.DOTALL)

    if match:
        generated_query = match.group(1).strip()
    else:
        generated_query = "customer_data"

    return generated_query


def get_filtered_data(user_query, pydantic_output, customer_data):

    llm_output = get_pandas_filtration_output(user_query = user_query, pydantic_output = pydantic_output)

    filtered_data = eval(extract_df_filter(llm_output))
    clean_filt_data = filtered_data.reset_index(drop=True)

    return clean_filt_data

    