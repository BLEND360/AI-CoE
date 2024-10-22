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
from .prompt_templates import pydantic_parser_prompt
from .data_groups import sport_product, sport_programming, sport_sport, sport_league, sport_show_title, ent_product, ent_content_brand_name, ent_genre, ent_show_title

# Setting up OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Setting up descriptions for sports field
def sport_product_desc(input_list):
    draft = "Refers to the brand app or brand website that users accessed.\
        Using this filter will return users who have watched, for instance, the Syfy app or bravo.com.\
        Here's a list of all the product names available: {unique_list}.\
        If a user describes their product of interest, it will be from this list above.\
        The output must be returned how it is mentioned exactly in the list.\
        "
    
    description = draft.format(unique_list = input_list)
    
    clean_desc = re.sub(' +', ' ', description).strip()
    
    return clean_desc

def sport_programming_desc(input_list):
    draft = "Refers to the sport level that users engage with.\
        Options include: {unique_list}.\
        This filter will return viewers of the selected sport level.\
        If a user describes their programming of interest, it will be from this list above.\
        The output must be returned how it is mentioned exactly in the list.\
        "
    
    description = draft.format(unique_list = input_list)
    
    clean_desc = re.sub(' +', ' ', description).strip()
    
    return clean_desc

def sport_sport_desc(input_list):
    draft = "Refers to all sports options available in PRISM.\
        This filter will return users who have watched basketball, golf, and cycling, amongst many other sports.\
        Here's a list of all sports available: {unique_list}.\
        If a user describes their sports of interest, it will be from this list above.\
        The output must be returned how it is mentioned exactly in the list.\
        "
    
    description = draft.format(unique_list = input_list)
    
    clean_desc = re.sub(' +', ' ', description).strip()
    
    return clean_desc

def sport_league_desc(input_list):
    draft = "Refers to all options for sport leagues in PRISM.\
        This filter will return users who have watched the NBA, PGA, Rugby World Cup, etc.\
        Note that the taxonomy used in both Sport and League are derived from CIP.\
        Here's a list of all the leagues available: {unique_list}.\
        If a user describes their league of interest, it will be from this list above.\
        The output must be returned how it is mentioned exactly in the list.\
        "
    
    description = draft.format(unique_list = input_list)
    
    clean_desc = re.sub(' +', ' ', description).strip()
    
    return clean_desc

def sport_show_title_desc(input_list):
    draft = "Refers to the title of all available Sports content in PRISM.\
        Note that this field is asynchronous, meaning no options are displayed by default but will be returned once users input a search for a specific result.\
        For instance, users can search for ‘Mbappe’ and will get results for all clip, vod, and linear content that has ‘Mbappe’ in its title.\
        Here's a list of all the show titles available: {unique_list}.\
        If a user describes their show title of interest, it will be from this list above.\
        The output must be returned how it is mentioned exactly in the list with the title in CAPITAL LETTERS\
        "
    
    description = draft.format(unique_list = input_list)
    
    clean_desc = re.sub(' +', ' ', description).strip()
    
    return clean_desc
    
# Setting up descriptions for entertainment field
def ent_product_desc(input_list):
    draft = "Refers to the brand app or brand website that users accessed.\
        Using this filter will return users who have watched, for instance, the Syfy app or bravo.com.\
        Here's a list of all the product names available: {unique_list}.\
        If a user describes their product name of interest, it will be from this list above.\
        The output must be returned how it is mentioned exactly in the list.\
        "
    
    description = draft.format(unique_list = input_list)
    
    clean_desc = re.sub(' +', ' ', description).strip()
    
    return clean_desc

def ent_content_brand_name_desc(input_list):
    draft = "Similar to product but is more specific to the overall brand and includes news stations.\
        Using this filter will return users who, for instance, have interacted with any Bravo content or have watched a specific local news brand (ex. KGET).\
        Here's a list of all the content brand names available: {unique_list}.\
        If a user describes their content brand name of interest, it will be from this list above.\
        The output must be returned how it is mentioned exactly in the list.\
        "
    
    description = draft.format(unique_list = input_list)
    
    clean_desc = re.sub(' +', ' ', description).strip()
    
    return clean_desc

def ent_genre_desc(input_list):
    draft = "Refers to genre of movies or shows.\
        This filter will return users who watched a certain genre, such as comedy viewers.\
        Here's a list of all the genres available: {unique_list}.\
        If a user describes their genre of interest, it will be from this list above.\
        The output must be returned how it is mentioned exactly in the list.\
        "
    
    description = draft.format(unique_list = input_list)
    
    clean_desc = re.sub(' +', ' ', description).strip()
    
    return clean_desc

def ent_show_title_desc(input_list):
    draft = "Has options for title of a show or movie.\
        This filter will return users who watched the selected show (ex. viewers of 30 ROCK).\
        Here's a list of all the show titles available: {unique_list}.\
        If a user describes their show title of interest, it will be from this list above.\
        The output must be returned how it is mentioned exactly in the list with the title in CAPITAL LETTERS\
        "
    
    description = draft.format(unique_list = input_list)
    
    clean_desc = re.sub(' +', ' ', description).strip()
    
    return clean_desc


def ent_season_desc():
    draft = "Contains options for seasons of a show. This filter will return users who have watched the selected season"
    
    return draft
def engagement_level_desc():
    draft = "Refers to an audience that has watched a specified show or movie or any type of video consumable multiple times.\
            Engagement level is how many times a user has watched a particular show.\
            Engagement level is always an integer greater than or equal to 0.\
            "
    return draft

def time_frame_desc():
    draft = "Refers to a time frame that the user query wants to focus on.\
            Such as past 90 days, 180 days, 12 days, etc.\
            Time frame is only refered in days. Only return the integer.\
            "
    return draft


#Setting up classes for pydantic parser
class Sports_Group(BaseModel):
    product: str = Field(description = sport_product_desc(sport_product))
    programming: str = Field(description = sport_programming_desc(sport_programming))
    sport: str = Field(description = sport_sport_desc(sport_sport))
    league: str = Field(description = sport_league_desc(sport_league))
    show_title: str = Field(description = sport_show_title_desc(sport_show_title))
    engagement_level: str = Field(description = engagement_level_desc())
    time_frame: str = Field(description = time_frame_desc())

class Entertainment_Group(BaseModel):
    product: str = Field(description = ent_product_desc(ent_product))
    content_brand_name: str = Field(description = ent_content_brand_name_desc(ent_content_brand_name))
    genre: str = Field(description = ent_genre_desc(ent_genre))
    show_title: str = Field(description = ent_show_title_desc(ent_show_title))
    season: str = Field(description = ent_season_desc())
    engagement_level: str = Field(description = engagement_level_desc())
    time_frame: str = Field(description = time_frame_desc())

class User_Tree(BaseModel):
    sports_groups: List[Sports_Group] = Field(description="Provide a list of sports groups from the description")
    entertainment_groups: List[Entertainment_Group] = Field(description="Provide a list of entertainment groups from the description")


def get_pydantic_parsed_entities(pydantic_class, user_query):
    parser = PydanticOutputParser(pydantic_object = pydantic_class)

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