import pandas as pd

def get_average_age(result_df):
    mean_age = result_df['age'].mean()
    output = f"- The mean age of customers is {mean_age:.2f} years.\n"
    
    return output

def get_most_spending_cat(result_df):
    spending_score_dist = result_df['spending_score'].value_counts().to_frame('count')
    spending_score_dist['percentage'] = (result_df['spending_score'].value_counts(normalize=True) * 100)
    top_spending_score_category = spending_score_dist['count'].idxmax()
    top_spending_score_percentage = spending_score_dist.loc[top_spending_score_category, 'percentage']

    return (f"- The most common spending score category is '{top_spending_score_category}' with {top_spending_score_percentage:.2f}% of customers.\n")

def get_attr_corr(result_df):
    spending_score_encoded = result_df['spending_score'].map({'low': 1, 'average': 2, 'high': 3})
    correlations = result_df[['age', 'work_experience']].copy()
    correlations['spending_score_encoded'] = spending_score_encoded
    correlation_matrix = correlations.corr()
    threshold = 0.3
    high_correlations = correlation_matrix[(correlation_matrix.abs() > threshold) & (correlation_matrix != 1.0)]
    
    output = ""
    if not high_correlations.empty:
        for row in high_correlations.index:
            for col in high_correlations.columns:
                if pd.notnull(high_correlations.loc[row, col]):
                    output += f"- {row} and {col} have a correlation of {high_correlations.loc[row, col]:.2f}\n"
                    
    return output

def get_pref_prod(result_df):
    product_by_gender = result_df.groupby('gender')['product_category'].value_counts(normalize=True).unstack().fillna(0)
    most_preferred_category = product_by_gender.idxmax(axis=1)
    most_preferred_percentage = product_by_gender.max(axis=1)

    output = ""
    for gender, category in most_preferred_category.items():
         output += f"- The most preferred product category for {gender} is '{category}' with {most_preferred_percentage[gender] * 100:.2f}% preference.\n"
        
    return output

def get_cust_spend_score(result_df):
    segment_by_spending = result_df.groupby('customer_segment')['spending_score'].value_counts(normalize=True).unstack().fillna(0)
    highest_spending_score_type = segment_by_spending.max().idxmax()
    highest_spending_score_percentage = segment_by_spending[highest_spending_score_type].max()
    best_segment = segment_by_spending[highest_spending_score_type].idxmax()
    best_segment_percentage = segment_by_spending.loc[best_segment, highest_spending_score_type]

    return (f"- '{best_segment}' customers have predominantly '{highest_spending_score_type}' spending scores ({best_segment_percentage * 100:.2f}%).\n")


def EDA_analysis(result_df):
    eda_res = "Here's some facts about the filtered data:\n"
    eda_res += get_average_age(result_df)
    eda_res += get_most_spending_cat(result_df)
    
    attr_cor_res = get_attr_corr(result_df)
    eda_res = eda_res + attr_cor_res if attr_cor_res else eda_res
    
    pref_prod_res = get_pref_prod(result_df)
    eda_res = eda_res + pref_prod_res if pref_prod_res else eda_res
    
    eda_res += get_cust_spend_score(result_df)
    
    return eda_res