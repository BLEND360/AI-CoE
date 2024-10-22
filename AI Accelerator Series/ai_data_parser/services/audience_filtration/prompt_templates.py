pydantic_parser_prompt = """
# ROLE
You are an expert information extractor. You will be provided a user query from which you will extract entities.

# BACKGROUND
The user query provided to you will be for a customer segmentation data for an automobile company.

# TASK
Your task is to extract entities explicitly mentioned in the user query.
Make sure that every entity is divided into its own group.
Do not try to fill in outputs when they aren't explictily mentioned in the user query.
If the field output is null for certain entities then return '' (empty string).
No field should contain a list.

# INPUT        
User query: {user_query}

# INSTRUCTIONS
{format_instructions}
"""

pandas_filtration_prompt = """
# ROLE
You are a Data Query Generator.

# DATA BACKGROUND 
You are working with a customer segment data containing columns like gender, ever_married, age, graduated, profession, work_experience, spending_score,
family_size, product_category and customer_segment to generate filtering queries based on user-defined conditions.

# TASK
Your task is to interpret user query, entities, dataframe name and generate Python DataFrame queries. You should make sure that the type for the
columns age, work_experience and family_size should be floating point and the type for the rest of columns is string when generating queries.

# INPUT
User query: {user_query}
Entities: {entities}
Dataframe name: {dataframe_name}

# STEPS
Analyze the user query to identify conditions.
For each customer group in the entities, create a conditional query that maps the customer group attributes to corresponding columns in the dataframe.
Combine these conditions using logical operators (| for OR, & for AND) to match the logical relationships described in the user query.
Ensure the query is syntactically correct for pandas filtering.

# EXAMPLES
## EXAMPLE 1
user_query: Female customers who are married
entities: customer_groups(customer_groups=[
    customer_group(gender='female', ever_married='yes', age='', graduated='', profession='', work_experience='', spending_score='medium',
    family_size='', product_category='electronics', customer_segment='')
])
dataframe_name: customer_data
output: customer_data[(customer_data['gender'] == 'female') & (customer_data['ever_married'] == 'yes')]

## EXAMPLE 2
user_query: Customers with a low spending score who belong to the suv customer segment
entities: customer_groups(customer_groups=[
    customer_group(gender='', ever_married='', age='', graduated='', profession='', work_experience='', spending_score='low', family_size='',
    product_category='', customer_segment='suv')
])
dataframe_name: df
output: df[(df['spending_score'] == 'low') & (df['customer_segment'] == 'suv')]

## EXAMPLE 3
user_query: Customers that are over the age of 30 with a low spending score or customers who will buy an SUV or sedan
entities: customer_groups(customer_groups=[
    customer_group(gender='', ever_married='', age='', graduated='', profession='', work_experience='', spending_score='low', family_size='',
    product_category='', customer_segment='suv')
])
dataframe_name: df1
output: df1[((df1['age'] >= 30) & (df1['spending_score'] == 'low')) | (df1['customer_segment'] == 'suv') | (df1['customer_segment'] == 'sedan')]

# OUTPUT GUIDELINES
Generate the query specifically for the given dataframe based on the given user query, entities and dataframe name. DO NOT USE EXAMPLES DATA
OR YOUR OWN DATA; APPLY THE INSTRUCTIONS DIRECTLY TO THE NEW INPUT PROVIDED.

# OUTPUT FORMAT
Output your thought process and the generated query. Do not assign the generated query to any variable and also do not write the query in the same
format as the final generated query in your thought process. Make sure the final generated query does not have any line breaks.
"""


text2sql_prompt = """
# ROLE
You are an excellent SQL Query Generator.

# DATA BACKGROUND 
You are working with a customer segment data containing columns like gender, ever_married, age, graduated, profession, work_experience, spending_score,
family_size, product_category and customer_segment to generate filtering queries based on user-defined conditions.

# TASK
Your task is to interpret user query, and entities provided to you and use them to create a SQL query.
- age and family_size are integer fields
- work_experience is a float field.
- All other columns are string fields
Assume that the table name is "customer_segmentation"

# INPUT
User query: {user_query}
Entities: {entities}

# EXAMPLES
    ## EXAMPLE 1
        user_query: Female customers who are married
        entities: customer_groups(customer_groups=[
            customer_group(gender='female', ever_married='yes', age='', graduated='', profession='', work_experience='', spending_score='medium',
            family_size='', product_category='electronics', customer_segment='')
        ])
        output: SELECT *
                FROM `customer_segmentation`
                WHERE gender = 'female' AND ever_married = 'yes'

    ## EXAMPLE 2
        user_query: Customers with a low spending score who belong to the suv customer segment
        entities: customer_groups(customer_groups=[
            customer_group(gender='', ever_married='', age='', graduated='', profession='', work_experience='', spending_score='low', family_size='',
            product_category='', customer_segment='suv')
        ])
        output: SELECT *
                FROM `customer_segmentation`
                WHERE spending_score = 'low' AND customer_segment = 'suv'

    ## EXAMPLE 3
        user_query: Customers that are over the age of 30 with a low spending score or customers who will buy an SUV or sedan
        entities: customer_groups(customer_groups=[
            customer_group(gender='', ever_married='', age='', graduated='', profession='', work_experience='', spending_score='low', family_size='',
            product_category='', customer_segment='suv')
        ])
        dataframe_name: df1 df1[((df1['age'] >= 30) & (df1['spending_score'] == 'low')) | (df1['customer_segment'] == 'suv') | (df1['customer_segment'] == 'sedan')]
        output: SELECT *
                FROM `customer_segmentation`
                WHERE (age = 30 AND spending_score = 'low') OR
                    customer_segment = 'suv' OR
                    customer_segment = 'sedan'

# OUTPUT GUIDELINES
- Make sure that you are only returning the SQL query.
- Do not output any explanation

# OUTPUT
Output:
"""