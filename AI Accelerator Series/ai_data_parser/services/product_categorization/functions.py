from .pydantic_parser import get_pydantic_parsed_entities, User_Tree
from .nested_json import get_nested_json
from .data_groups import sport_product, sport_programming, sport_sport, sport_league, sport_show_title, ent_product, ent_content_brand_name, ent_genre,  ent_show_title

# E2E tree builder
def e2e_audience_tree_builder(pydantic_class, user_query):
    unique_entities = get_pydantic_parsed_entities(pydantic_class = User_Tree, user_query = user_query)
    
    # print('Unique entities:', unique_entities)
    
    audience_tree = get_nested_json(pydantic_entities = unique_entities, user_query = user_query)
    
    return audience_tree

def convert_to_target_structure(input_data):
    def process_group_or_rules(data, parent_key=None):
        if isinstance(data, dict):
            group_conjunction = list(data.keys())[0]
            group_data = data[group_conjunction]
            children = []
            for key, value in group_data.items():
                if key in ["AND", "OR", "NOT AND", "NOT OR"]:
                    children.append(process_group_or_rules({key: value}, None))
                elif isinstance(value, dict):
                    for field_key, field_value in value.items():
                        if field_value != "":
                            children.append(create_rule(field_key, field_value, key))
                else:
                    if value != "":
                        children.append(create_rule(key, value, parent_key))
            return {
                "type": "group",
                "properties": {
                    "conjunction": group_conjunction.replace('NOT','').strip(),
                    "not": True if 'not' in group_conjunction.lower() else False
                },
                "children": children
            }
    
    def create_rule(field_key, field_value, parent_key=None):
        field_path = f"{parent_key}.{field_key}" if parent_key else field_key
        
        if field_key == 'engagement_level':
            operator = 'greater_or_equal'
            value = [int(field_value)] if isinstance(field_value, str) and field_value.isdigit() else [field_value]
            value_type = ["number"]
        elif field_key == 'time_frame':
            operator = 'less_or_equal'
            value = [int(field_value)] if isinstance(field_value, str) and field_value.isdigit() else [field_value]
            value_type = ["number"]
        elif field_key == 'show_title':
            operator = 'multiselect_contains'
            value = [field_value] if isinstance(field_value, str) else field_value
            value_type = ["multiselect"]
        else:
            operator = "select_equals"
            value = [field_value]
            value_type = ["select"]
        
        return {
            "type": "rule",
            "properties": {
                "fieldSrc": "field",
                "field": field_path,
                "operator": operator,
                "value": value,
                "valueSrc": ["value"],
                "valueType": value_type
            }
        }
    
    return process_group_or_rules(input_data)

def create_config():
    return {
        'fields': {
            'category': {
                'type': 'select',
                'label': 'Category',
                'valueSources': ['value'],
                'fieldSettings': {
                    'listValues': [
                        {'value': 'sports', 'title': 'Sports'},
                        {'value': 'entertainment', 'title': 'Entertainment'}
                    ]
                }
            },
            'sports': {
                'type': '!struct',
                'label': 'Sports',
                'subfields': {
                    'product': {
                        'type': 'select',
                        'label': 'Product',
                        'valueSources': ['value'],
                        'fieldSettings': {
                            'listValues': [{'value': p, 'title': p} for p in sport_product]
                        }
                    },
                    'programming': {
                        'type': 'select',
                        'label': 'Programming',
                        'valueSources': ['value'],
                        'fieldSettings': {
                            'listValues': [{'value': p, 'title': p} for p in sport_programming]
                        }
                    },
                    'sport': {
                        'type': 'select',
                        'label': 'Sport',
                        'valueSources': ['value'],
                        'fieldSettings': {
                            'listValues': [{'value': s, 'title': s} for s in sport_sport]
                        }
                    },
                    'league': {
                        'type': 'select',
                        'label': 'League',
                        'valueSources': ['value'],
                        'fieldSettings': {
                            'listValues': [{'value': l, 'title': l} for l in sport_league]
                        }
                    },
                    'show_title': {
                        'type': 'multiselect',
                        'label': 'Show Title',
                        'valueSources': ['value'],
                        'fieldSettings': {
                            'listValues': [{'value': t, 'title': t} for t in sport_show_title],
                            'allowCustomValues': True
                        },
                        'operators': ['multiselect_contains', 'multiselect_not_contains', 'equal', 'not_equal', 'select_any_in', 'select_not_any_in', 'is_null', 'is_not_null']
                    },
                    'engagement_level': {
                        'type': 'number',
                        'label': 'Engagement Level',
                        'valueSources': ['value'],
                        'fieldSettings': {
                            'min': 1,
                            'max': 100
                        },
                        'preferWidgets': ['slider', 'number']
                    },
                    'time_frame': {
                        'type': 'number',
                        'label': 'Time Frame',
                        'valueSources': ['value'],
                        'fieldSettings': {
                            'min': 1
                        },
                        'preferWidgets': ['number']
                    }
                }
            },
            'entertainment': {
                'type': '!struct',
                'label': 'Entertainment',
                'subfields': {
                    'product': {
                        'type': 'select',
                        'label': 'Product',
                        'valueSources': ['value'],
                        'fieldSettings': {
                            'listValues': [{'value': p, 'title': p} for p in ent_product]
                        }
                    },
                    'content_brand': {
                        'type': 'select',
                        'label': 'Content Brand',
                        'valueSources': ['value'],
                        'fieldSettings': {
                            'listValues': [{'value': b, 'title': b} for b in ent_content_brand_name]
                        }
                    },
                    'genre': {
                        'type': 'select',
                        'label': 'Genre',
                        'valueSources': ['value'],
                        'fieldSettings': {
                            'listValues': [{'value': g, 'title': g} for g in ent_genre]
                        }
                    },
                    'show_title': {
                        'type': 'multiselect',
                        'label': 'Show Title',
                        'valueSources': ['value'],
                        'fieldSettings': {
                            'listValues': [{'value': t, 'title': t} for t in ent_show_title],
                            'allowCustomValues': True

                        },
                        'operators': ['multiselect_contains', 'multiselect_not_contains', 'equal', 'not_equal', 'select_any_in', 'select_not_any_in', 'is_null', 'is_not_null']
                    },
                    'engagement_level': {
                        'type': 'number',
                        'label': 'Engagement Level',
                        'valueSources': ['value'],
                        'fieldSettings': {
                            'min': 1,
                            'max': 100
                        },
                        'preferWidgets': ['slider', 'number']
                    },
                    'time_frame': {
                        'type': 'number',
                        'label': 'Time Frame',
                        'valueSources': ['value'],
                        'fieldSettings': {
                            'min': 1
                        },
                        'preferWidgets': ['number']
                    }
                }
            }
        }
    }
