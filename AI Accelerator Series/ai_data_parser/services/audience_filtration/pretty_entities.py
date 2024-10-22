import json
import streamlit as st

def flatten_entities(pydantic_output):
    # Extract all the values from each customer group and append as a list.
    pydantic_dict = [vars(group) for group in pydantic_output.customer_groups]
    
    # Initialize an empty dictionary to hold the flattened data
    flattened_dict = {}
    
    # Iterate over each dictionary in the list
    for entry in pydantic_dict:
        # For each key in the dictionary
        for key, value in entry.items():
            # If the key is not already in the result dictionary, add it with an empty list
            if key not in flattened_dict:
                flattened_dict[key] = []
            # Append the current value to the list of the corresponding key
            flattened_dict[key].append(value)

    return flattened_dict

def pretty_entity_string(pydantic_output):
    # Flatten the pydantic output to list of dictionaries
    flattened_dict = flatten_entities(pydantic_output = pydantic_output)
    
    # Initialize an empty list to store the result
    result = []
    
    first_line = "##### These are all the entities identified and extracted from your query"
    result.append(first_line)
    
    # Iterate through the flattened dictionary
    for key, values in flattened_dict.items():
        # Filter out any empty values from the list
        non_empty_values = [value for value in values if value]
        unique_values = list(set(non_empty_values))
    
        # If there are any non-empty values, concatenate the key with its values
        if unique_values:
            # Join multiple values with a comma
            values_str = ', '.join(unique_values)
            # Append the formatted string to the result
            new_line = f"**{key.replace('_', ' ').title()}**: {values_str}\n  "
            result.append(new_line)

    return result