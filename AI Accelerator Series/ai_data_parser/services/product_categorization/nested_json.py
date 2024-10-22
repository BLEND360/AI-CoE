from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import openai
import os
import ast
import json
from .prompt_templates import nested_json_prompt

# Setting up OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

example1={
    "AND": {
        "sports": {
            "product": "",
            "programming": "",
            "sport": "Soccer",
            "league": "",
            "show_title": "",
            "engagement_level": "",
            "time_frame": ""
            },
        "OR": {
            "entertainment": {
                "product": "",
                "content_brand_name": "",
                "genre": "COM",
                "show_title": "",
                "season": "",
                "engagement_level": "",
                "time_frame": ""
            }
        }
    }
}
example2={
    "AND": {
        "entertainment": {
                "product": "Bravo App",
                "content_brand_name": "Bravo",
                "genre": "",
                "show_title": "30 ROCK",
                "season": "",
                "engagement_level": "1",
                "time_frame": "90"
            },
        "AND": {
            "entertainment": {
                "product": "NBC App",
                "content_brand_name": "NBC",
                "genre": "",
                "show_title": "THE OFFICE",
                "season": "",
                "engagement_level": "1",
                "time_frame": "90"
            }
        }
    }
}
example3={
    "AND": {
        "entertainment": {
            "product": "Bravo App",
            "content_brand_name": "NBC",
            "genre": "",
            "show_title": "30 ROCK",
            "season": "",
            "engagement_level": "1",
            "time_frame": "90"
        },
        "OR":{
            "entertainment": {
                "product": "NBC App",
                "content_brand_name": "",
                "genre": "",
                "show_title": "THE OFFICE",
                "season": "",
                "engagement_level": "1",
                "time_frame": "90"
            },
            "NOT AND": {
                "sports": {
                    "product": "",
                    "programming": "",
                    "sport": "Soccer",
                    "league": "",
                    "show_title": "",
                    "engagement_level": "1",
                    "time_frame": "90"
                }
            }
        }
    }
}

def get_nested_json(pydantic_entities, user_query):

    user_tree_str = json.dumps(
        {
            "sports_groups": [vars(group) for group in pydantic_entities.sports_groups],
            "entertainment_groups": [vars(group) for group in pydantic_entities.entertainment_groups]
        },
        indent=4)
    
    llm = ChatOpenAI(
        model="gpt-4-turbo",#"gpt-3.5-turbo-16k-0613",
        openai_api_key=openai.api_key,
        temperature=0,
        streaming=True
    )
    
    prompt = PromptTemplate(
        template=nested_json_prompt,
        input_variables=["user_query", "user_tree"],
    )

    chain = prompt | llm

    result = chain.invoke({"user_query": user_query, "user_tree": user_tree_str,"example1":example1,"example2":example2,"example3":example3})

    llm_output = result.content
    
    try:
        clean_output = ast.literal_eval(llm_output
                                        .replace('`', '')
                                        .replace('json', '')
                                        .replace('sports_groups', 'sports')
                                        .replace('entertainment_groups', 'entertainment')
                                       )
        # print('Audience tree successfully built!')
    except Exception as e:
        clean_output = {}
        print('Audience tree failed! ', llm_output)
    
    return clean_output    