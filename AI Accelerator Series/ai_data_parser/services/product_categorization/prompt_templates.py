pydantic_parser_prompt = """
# ROLE
You are an expert information extractor. You will be provided a user query from which you will extract entities.

# TASK
Your task is to extract fields explicitly mentioned in the user query from the unique list of values provided to you.
Make sure that every field is divided into its own group.
Do not try to fill in outputs when they aren't explictily mentioned in the user query. 
If the output is null for certain fields then return '' (empty string).
No field should contain a list.

# INPUT        
User query: {user_query}

# INSTRUCTIONS
{format_instructions}
"""

nested_json_prompt = """
#ROLE
You are given a user query and a user tree object that contains identified sports and entertainment groups.
Your task is to determine the logical relationships between the identified groups based on the query and return a structured JSON output.

#INPUT
1) Your first input will be a User Query: {user_query}
2) Your second input would be a User_Tree Object: {user_tree}

#TASK
Your task is to determine the logical relationship between the identified sports and entertainment groups. Use operators such as 'and', 'or' etc.,
to reflect the relationships.The words 'additionally', 'and', 'both', 'also' SHOULD BE INTERPRETED AS LOGICAL AND OPERATOR, while the words 'either', 'or'
SHOULD BE INTERPRETED AS LOGICAL OR OPERATOR.
Provide your response in a structured JSON format showing how the different criteria are logically connected.

#THOUGHT PROCESS
1) Carefully read the input user query and the user tree object.
2) Identify the logical relationship between each entity in the user tree object from the input user query.
3) Identify the starting global operation either "AND", "OR", "NOT OR" or "NOT AND". This global operation must be followed by an entertainment or sports group. Recognise this and start creating the JSON.
4) Identify the local relationships between entities from the user query. Make sure each entity is preceded by the relevant key i.e. the logical operation.
5) Make sure you mention each logical operation for ALL the entities and do not use nested list or square brackets to denote relationships.
6) Give the relavant nested JSON output.
    
    
#EXAMPLES
Here are some examples to help you with your task.
#EXAMPLE 1: To create a JSON for the following inputs, 
    User Query: Audience that loves watching soccer or comedy shows
    User Tree: sports_groups=[Sports_Group(product='', programming='', sport='Soccer', league='', show_title='', engagement_level='', time_frame='')] entertainment_groups=[Entertainment_Group(product='', content_brand_name='', genre='COM', show_title='', season='', engagement_level='', time_frame='')]
    let's think about the it step-by-step.
        1) I read the User Query and the User Tree
        2) I see that there are two entities in the User Tree.
        3) I recognise that the global operation is AND. So I start with an "AND" operation and include all the entities inside this.
        4) I see from the user query that the two entities are logically connected with OR operation. So I make sure to preceed the second entity with the key "OR".
    Thus, my output is:
        {example1}

#EXAMPLE 2: To create a JSON for the following inputs, 
    User Query: Create an audience that watched 30 Rock at least once in the past 90 days in Bravo app and the office at least once in the past 90 days using the NBC app
    User Tree: sports_groups=sports_groups=[] entertainment_groups=[Entertainment_Group(product='Bravo App', content_brand_name='Bravo', genre='', show_title='30 Rock', season='', engagement_level='1', time_frame='90'), Entertainment_Group(product='NBC App', content_brand_name='NBC', genre='', show_title='The Office', season='', engagement_level='1', time_frame='90')]
    let's think about the it step-by-step.
        1) I read the User Query and the User Tree
        2) I see that there are two entities in the User Tree.
        3) I recognise that the global operation is AND.
        3) I see from the user query that the two entities are logically connected with AND operation. So I make sure to preceed the second entity with the key "AND".
    
    Thus, my output is:
        {example2}

#EXAMPLE 3: To create a JSON for the following inputs, 
    User Query: Create an audience that watched 30 Rock in Bravo app or the office using the NBC app at least one time in the past 90 days.On top of that, this audience must also not be interested in watching soccer at least once in the past 3 months
    User Tree: sports_groups=[Sports_Group(product='', programming='', sport='Soccer', league='', show_title='', engagement_level='1', time_frame='90')] entertainment_groups=[Entertainment_Group(product='Bravo App', content_brand_name='NBC', genre='', show_title='30 Rock', season='', engagement_level='1', time_frame='90'), Entertainment_Group(product='NBC App', content_brand_name='', genre='', show_title='The Office', season='', engagement_level='1', time_frame='90')]
        1) I read the User Query and the User Tree
        2) I see that there are three different entities in the User Tree.
        3) I recognise that the first operation is AND. So I start with an "AND" operation and include all the entities for 30 ROCK entertainment group inside this.
        3) I see from the user query that "the office" entity entertainment group is logically connected with OR operation with the first entity. So I make sure to preceed the second one with "OR".
        4) The third entity has a "NOT AND" global operator and is a condition on top of the first two entities.
    
    Thus, my output is:
        {example3}
        
    
#OUTPUT
1) DO NOT INCLUDE '[]' IN THE OUTPUT JSON STRING
2) EACH NESTED ENTITY GROUP SHOULD HAVE THE RELVANT LOGICAL OPERATION AND A SPORT/ENTERTAINMENT AS THE KEYS
3) ONLY OUTPUT THE JSON STRING. DO NOT INCLUDE ANY EXPLAINATION OR THOUGHT PROCESS IN THE OUTPUT.
"""