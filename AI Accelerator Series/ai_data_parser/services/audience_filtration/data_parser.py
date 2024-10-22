import json
import pandas as pd
from services.audience_filtration.pydantic_parser import get_pydantic_parsed_entities
from services.audience_filtration.pandas_filtration import get_filtered_data
from services.audience_filtration.text2sql import get_sql_query
import concurrent.futures

# customer_data = pd.read_csv('data/customer_segmentation.csv')

def audience_filtration(user_query, customer_data):
    extracted_entities = get_pydantic_parsed_entities(user_query = user_query)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the functions to the executor
        future1 = executor.submit(get_filtered_data, user_query, extracted_entities, customer_data)
        future2 = executor.submit(get_sql_query, user_query, extracted_entities)
        
        # Retrieve the results (waits until both are done)
        filtered_data = future1.result()
        sql_query = future2.result()

    return extracted_entities, filtered_data, sql_query