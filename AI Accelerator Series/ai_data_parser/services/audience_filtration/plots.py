import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

class EDAPlots:
    '''A class to build out plots from the LLM generated filtered dataframe'''
    
    def charts(df):
        # Set up the plot grid
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        fig.tight_layout(pad=5.0)
        
        # Plot 1: Profession Breakdown (Pie Chart)
        profession_counts = df['profession'].value_counts()
        axs[0, 0].pie(profession_counts, labels=profession_counts.index, autopct='%1.1f%%', 
                      startangle=90, colors=plt.cm.Paired.colors)
        axs[0, 0].set_title('Profession Breakdown')
        
        # Plot 2: Product Category vs No. of Customers (Horizontal Bar)
        product_category_counts = df['product_category'].value_counts()
        axs[1, 1].barh(product_category_counts.index, product_category_counts.values, color='skyblue')
        axs[1, 1].set_xlabel('Number of Customers')
        axs[1, 1].set_ylabel('Product Category')
        axs[1, 1].set_title('Customers by Product Category')

        # Plot 3: Customer Segment Distribution (Pie Chart)
        segment_counts = df['customer_segment'].value_counts()
        axs[0, 1].pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', 
                      startangle=90, colors=plt.cm.Set2.colors)
        axs[0, 1].set_title('Customer Segment Distribution')

        # Plot 4: Age vs Family Size (Scatter Plot)
        scatter = axs[1, 0].scatter(df['age'], df['family_size'], c=df['family_size'], cmap='viridis', alpha=0.6)
        axs[1, 0].set_xlabel('Age')
        axs[1, 0].set_ylabel('Family Size')
        axs[1, 0].set_title('Age vs Family Size')
        fig.colorbar(scatter, ax=axs[1, 0], label='Family Size')

        return fig

        


