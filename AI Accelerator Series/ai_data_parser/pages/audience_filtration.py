import streamlit as st
import pandas as pd
from services.audience_filtration.data_parser import audience_filtration
from services.audience_filtration.plots import EDAPlots
from services.audience_filtration.filtration_EDA import EDA_analysis

st.title("Audience Filtration Tool")
st.markdown(
    """
    <p> Audience Filtration is an AI-powered solution designed to help businesses filter and segment customer data based on natural language queries. By enabling users to
    describe their target audience in plain language, this tool automates the complex process of customer segmentation, making it accessible to both technical and non-technical
    users. For example, an automobile company can quickly identify customers under 28 with low spending scores who may be interested in sports cars, allowing for more precise
    marketing and outreach.
    
    The tool is especially useful for businesses with large, complex datasets containing diverse attributes like age, profession, spending behavior, and vehicle preferences. It
    simplifies the extraction of detailed customer segments, such as “female healthcare professionals aged 25-35 who prefer electric vehicles,” enabling businesses to make data
    driven decisions with ease.
    
    Audience Filtration uses two key approaches: Prompt Engineering with Pydantic Parsers and Text-to-SQL. Prompt Engineering processes natural language inputs, validates them
    using Pydantic, and returns structured data for precise filtering. Text-to-SQL translates user queries directly into SQL commands, allowing businesses to efficiently query
    relational databases without writing SQL manually. By leveraging advanced natural language processing (NLP), Audience Filtration transforms customer segmentation into an
    intelligent, streamlined process, enhancing business decision-making and customer targeting.

    For more information, please visit the confluence page <a href='https://blend360.atlassian.net/wiki/spaces/DSDH/pages/951222280/Audience+Filtration' target='_blank'>here</a>.
    </p>
    """,
    unsafe_allow_html=True
)

st.write('Original customer segmentation dataset')
df = pd.read_csv('data/customer_segmentation.csv')
st.dataframe(df, hide_index=True)
st.write(f'{df.shape[0]} rows, {df.shape[1]} columns')
st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages and filtered dfs from history on app rerun
for message in st.session_state.messages:
    st.markdown(f"🧑: **{message['content']}**")  # Display user query with user icon
    st.write("🤖:")
    st.write('SQL query:')
    st.code(message['sql_query'])
    
    output = st.expander('Detailed Output')
    output.write('Filtered Data')
    output.dataframe(message["data"], hide_index=True)
    output.write(f'{message["data"].shape[0]} rows, {message["data"].shape[1]} columns')
    
    fig = EDAPlots.charts(message["data"])
    fig.tight_layout()
    output.pyplot(fig)
    st.text(message['EDA'])
    st.divider()

# Container for user input and processing
cont = st.container()

# Accept user input
if prompt := st.chat_input("Enter your query here"):
    cont.markdown(f"🧑: **{prompt}**")  # Show user query with user icon
    
    with st.spinner("Filtering Audience ..."):
        entities, filt_df, sql_query = audience_filtration(user_query=prompt, customer_data=df)
        cont.write("🤖:")
        cont.write('SQL query:')
        cont.code(sql_query)
        
        output = cont.expander('Detailed Output')
        output.write('Filtered Data')
        output.dataframe(filt_df, hide_index=True)
        output.write(f'{filt_df.shape[0]} rows, {filt_df.shape[1]} columns')
        
        fig = EDAPlots.charts(filt_df)
        fig.tight_layout()
        output.pyplot(fig)
        
        EDA_text = EDA_analysis(filt_df)
        st.text(EDA_text)

    # Add user message and filtered df to chat history
    st.session_state.messages.append({"content": prompt, "sql_query": sql_query, "data": filt_df, "EDA": EDA_text})
    
    # Rerun the app to scroll to the latest message/output
    # st.experimental_rerun()
    # st.experimental_set_query_params()
