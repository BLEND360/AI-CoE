from pydantic import BaseModel, Field # version 2.4.2
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from typing import List
import openai
import os
import json
import pandas as pd
import re
from services.audience_filtration.prompt_templates import pydantic_parser_prompt

# Setting up OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Reading in data
customer_data = pd.read_csv('data/customer_segmentation.csv')

# Creating variables for each column with unique values
for column in customer_data.columns:
    if column != 'ID':
        unique_values = customer_data[column].unique()
        globals()[f"unique_{column}"] = list(unique_values)

# Seting up field descriptions
def gender_desc(unique_list: List = []):
    if unique_list:
        desc_draft = "Refers to the customer's gender. Here's a list of possible genders: {unique_list}."

        desc = desc_draft.format(unique_list = unique_list)
    else:
        desc = "Refers to the customer's gender."
    
    clean_desc = re.sub(' +', ' ', desc).strip()
    
    return clean_desc


def ever_married_desc(unique_list: List = []):
    if unique_list:
        desc_draft = "Refers to the customer's marital status. Here's a list of possible marital statuses: {unique_list}."

        desc = desc_draft.format(unique_list = unique_list)
    else:
        desc = "Refers to the customer's marital status."
    
    clean_desc = re.sub(' +', ' ', desc).strip()
    
    return clean_desc


def age_desc():
    clean_desc = "Refers to the customer's age in years. Age is an integer"
    
    return clean_desc


def graduated_desc(unique_list: List = []):
    if unique_list:
        desc_draft = "Refers to whether the customer has graduated or not. Here's a list of possible graduation status: {unique_list}."

        desc = desc_draft.format(unique_list = unique_list)
    else:
        desc = "Refers to whether the customer has graduated or not."
    
    clean_desc = re.sub(' +', ' ', desc).strip()
    
    return clean_desc


def profession_desc(unique_list: List = []):
    if unique_list:
        desc_draft = "Refers to the customer's profession. Here's a list of possible professions: {unique_list}."

        desc = desc_draft.format(unique_list = unique_list)
    else:
        desc = "Refers to the customer's profession."
    
    clean_desc = re.sub(' +', ' ', desc).strip()
    
    return clean_desc


def work_experience_desc():
    clean_desc = "Refers to the customer's work experience in years. Work experience is a float such as '1.5', '10.0', '9.8', etc. Work experience should only return numerical float values. No other characters."
    
    return clean_desc


def spending_score_desc(unique_list: List = []):
    if unique_list:
        desc_draft = "Refers to the customer's spending score. Here's a list of possible spending scores: {unique_list}."

        desc = desc_draft.format(unique_list = unique_list)
    else:
        desc = "Refers to the customer's spending score."
    
    clean_desc = re.sub(' +', ' ', desc).strip()
    
    return clean_desc


def family_size_desc():
    clean_desc = "Refer's to the customer's family size which is the number of family members for the customer including the customer. Family size is an integer"
    
    return clean_desc


def product_category_desc(unique_list: List = []):
    if unique_list:
        desc_draft = "Refers to the customer's product category. It's a automobile product category that the customer is interested in buying. Here's a list of possible product categories: {unique_list}."

        desc = desc_draft.format(unique_list = unique_list)
    else:
        desc = "Refers to the customer's product category. It's a automobile product category that the customer is interested in buying."
    
    clean_desc = re.sub(' +', ' ', desc).strip()
    
    return clean_desc


def customer_segment_desc(unique_list: List = []):
    if unique_list:
        desc_draft = "Refers to the customer segment for the customer. It is the type of automobile that the customer is predicted to buy. Here's a list of possible customer segments: {unique_list}."

        desc = desc_draft.format(unique_list = unique_list)
    else:
        desc = "Refers to the customer segment for the customer. It is the type of automobile that the customer is predicted to buy."
    
    clean_desc = re.sub(' +', ' ', desc).strip()
    
    return clean_desc



class customer_group(BaseModel):
    gender: str = Field(description = gender_desc(unique_gender))
    ever_married: str = Field(description = ever_married_desc(unique_ever_married))
    age: str = Field(description = age_desc())
    graduated: str = Field(description = graduated_desc(unique_graduated))
    profession: str = Field(description = profession_desc(unique_profession))
    work_experience: str = Field(description = work_experience_desc())
    spending_score: str = Field(description = spending_score_desc(unique_spending_score))
    family_size: str = Field(description = family_size_desc())
    product_category: str = Field(description = product_category_desc(unique_product_category))
    customer_segment: str = Field(description = customer_segment_desc(unique_customer_segment))
    
class customer_groups(BaseModel):
    customer_groups: List[customer_group] = Field(description = "Provide a list of customer group from description")


def get_pydantic_parsed_entities(user_query):
    parser = PydanticOutputParser(pydantic_object = customer_groups)

    llm = ChatOpenAI(
        model="gpt-4-turbo",#"gpt-3.5-turbo-16k-0613",
        openai_api_key=openai.api_key,
        temperature=0,
        streaming=True
    )
    
    prompt = PromptTemplate(
        template=pydantic_parser_prompt,
        input_variables=["user_query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser
    
    response = chain.invoke({"user_query": user_query})
    
    # print('Entities extracted successfully!')
    
    return response