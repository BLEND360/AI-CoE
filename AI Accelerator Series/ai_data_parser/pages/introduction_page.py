import streamlit as st
import pandas as pd

st.html("<h1>AI Data Parser Tools</h1>")

st.html("<h4>Overview</h4>"
"<p>The AI Data Parser Tool introduces the flexibility of capturing meaningful entities from a dynamic \
user input using Artificial Intelligence. It accelerates data retrieval and reduces manual effort, \
leading to cost savings and improved operational efficiency. Within this tool, we use LangChain’s <b>Pydantic \
Parser</b> to facilitate accurate extraction and structuring of key entities from user queries, which is crucial\
 for improving the precision of search engines, chatbots, and virtual assistants, leading to better user \
 experiences and more relevant responses. Within the AI Data Parser tool, we have implemented three accelerators\
  for various use cases such as Audience Filteration, Product Categorization and Resume Parser. The details for\
  these specific use cases are discussed in the sections below.</p>"
"<h4>Audience Filteration</h4>"
"<ol><h6>Business Use Case:</h6>\
<p>Based on a specific schema, certain audience segments can be filtered seemlessly using AI. Considering \
only the input user query description, the tool can easily extract and integrate valuable information from \
user queries, enhancing the depth of data analysis and insights. This capability allows businesses to \
precisely target and tailor their marketing strategies to distinct audience segments, leading to more \
effective and personalized campaigns. By accurately filtering and analyzing audience data, companies can \
improve engagement rates, optimize resource allocation, and achieve higher ROI on marketing \
efforts.</p>\
<h6>Data:</h6>\
<p> A <b>Customer Segmentation Dataset</b> from Kaggle is used to demonstrate this particular use case. This \
dataset is used for demonstration purposes. The underlying mechanism for the accelerator can be easily customized \
to fit any other appropriate dataset.</p>")
customer_segmentation=pd.read_csv('data/customer_segmentation.csv')
st.dataframe(customer_segmentation, hide_index=True)

st.html("<h6>Input:</h6>\
<p>The input is a user query in natural language to filter the dataset based on a desired set of conditions. </p>\
<h6>Output:</h6>\
<p>The output is the filtered dataset based on the input user query, EDA Plots and Insights, a SQL query\
 used to generate the output and the number of extracted entities on which the data was filtered for\
reference.</p></ol>"

"<h4>Product Categorization</h4>"
"<ol><h6>Business Use Case:</h6>\
<p>Utilizing retail data from platforms like Amazon or Flipkart, the AI Data Parser Tool can efficiently \
categorize products based on predefined schemas and user input descriptions. By parsing and analyzing \
product attributes and descriptions, the tool can accurately assign items to appropriate categories, \
facilitating seamless integration into inventory systems. This capability enhances the organization and \
accessibility of products, leading to improved user experience by making it easier for customers to find \
what they’re looking for. Accurate product categorization also boosts search accuracy, increases visibility \
in product recommendations, and supports targeted marketing efforts. </p>\
<h6>Data:</h6>\
<p>The data used for this tool is divided into two main categories: 1) Sports 2) Entertainment. \
Here is a data snippet for reference.</p>")
entertainment=pd.read_csv('data/entertainment_combos.csv')
sports=pd.read_csv('data/sports_combos.csv')
st.html("<ul><h7>Entertainment data</h7></ul>")
st.dataframe(entertainment, hide_index=True)
st.html("<ul><h7>Sports data</h7></ul>")
st.dataframe(sports, hide_index=True)

st.html("<ol><h6>Input:</h6>\
<p>The input is a User Query aiming to categorise a combination of multiple attributes from the given \
two categories.</p>\
<h6>Output:</h6>\
<p>The output is a tree of desired attributes categorized according to the user queries.</p></ol>"
"<h4>Resume Parser</h4>"
"<p>TBD</p>")

st.markdown("<p>For more in-depth information, please visit the confluence page <a href='https://blend360.atlassian.net/wiki/spaces/DSDH/pages/929792015/AI+Data+Parser+Tool' target='_blank'> here </a> </p>", unsafe_allow_html=True)