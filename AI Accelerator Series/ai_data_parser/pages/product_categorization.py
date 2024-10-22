import streamlit as st
from streamlit_condition_tree import condition_tree
from services.product_categorization.functions import e2e_audience_tree_builder, convert_to_target_structure, create_config
from services.product_categorization.pydantic_parser import User_Tree
import warnings
warnings.filterwarnings('ignore')
# st.set_page_config(layout="wide")
st.title('Product Categorization Tool')
st.markdown(
    """
    <p> In the rapidly evolving landscape of digital streaming, understanding and categorizing content effectively is crucial for enhancing user experience and optimizing
    content delivery. Our AI-powered data parser serves as a robust solution for product categorization across diverse streaming platforms.
    
    This use case revolves around two distinct types of data: content type categorization and programming categorization. The first dataset includes attributes such as
    <code>CONTENT_BRAND_NAME</code>, <code>GENRE</code>, and <code>SHOW_TITLE</code>, which help classify shows based on their content type (e.g., talk shows, music programs, news segments). The second dataset extends this categorization to encompass specific programming details, such as <code>SPORT</code>, <code>LEAGUE</code>, and <code>SHOW_TITLE</code>, focusing on sports content and its associated leagues.
    
    By leveraging advanced machine learning techniques, our parser will:
    <ol>
    <li><b>Automate Categorization:</b> Streamline the process of sorting and tagging shows by recognizing patterns and relationships within the data, ensuring consistent categorization</li>
    across platforms.
    <li><b>Enhance Discoverability:</b> Improve the user experience by enabling more accurate search and recommendation features, allowing users to find content that fits their interests quickly. </li>
    <li><b>Data-Driven Insights:</b> Generate insights on viewing trends and preferences based on categorized data, enabling businesses to make informed decisions about content
    acquisition and marketing strategies.</li>
    <li><b>Cross-Platform Compatibility:</b> Support various streaming platforms, ensuring that content is categorized uniformly, regardless of where it is accessed.</li>
    </ol>
    This innovative approach to product categorization not only improves operational efficiency but also enriches the overall viewer experience, positioning businesses to thrive in a competitive digital content market.

    For more information, please visit the confluence page <a href='https://blend360.atlassian.net/wiki/spaces/DSDH/pages/1000669215/Product+Categorization' target='_blank'>here</a>.
    </p>
    """,
    unsafe_allow_html=True
)

def reset_app():
    for key in ['tree_data', 'query_struct', 'user_input', 'llm_output', 'show_llm_output']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# Initialize session state
if 'tree_data' not in st.session_state:
    st.session_state.tree_data = None
if 'query_struct' not in st.session_state:
    st.session_state.query_struct = None
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'llm_output' not in st.session_state:
    st.session_state.llm_output = None
if 'show_llm_output' not in st.session_state:
    st.session_state.show_llm_output = False

# User input
user_input = st.text_area("**Enter your query to build a condition tree:**", 
                          value=st.session_state.user_input, 
                          key="user_input")
st.markdown("")
# Create columns for buttons
col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])

# Submit button in the left column
with col1:
    submit_button = st.button("Build Audience Tree", use_container_width=True,type='primary')

# Show LLM Output button in the middle column (only show if LLM output exists)
with col3:
    if st.session_state.llm_output:
        if st.button("Show AI Model Output", use_container_width=True,type='primary'):
            st.session_state.show_llm_output = not st.session_state.show_llm_output

# Create Another Tree button in the right column (only show if tree data exists)
with col5:
    if st.session_state.tree_data:
        if st.button("Create Another Tree", use_container_width=True,type='primary'):
            reset_app()

# Process when button is clicked
if submit_button:
    with st.spinner("Building audience tree..."):
        llm_output = e2e_audience_tree_builder(pydantic_class=User_Tree, user_query=user_input)
        st.session_state.llm_output = llm_output  # Store LLM output in session state

        tree = convert_to_target_structure(llm_output)
        config = create_config()
        
        # Store the tree data in session state
        st.session_state.tree_data = {
            'config': config,
            'tree': tree
        }
                      
# Display LLM Output if the button was clicked
if st.session_state.show_llm_output and st.session_state.llm_output:
    st.subheader("LLM Output:")
    st.write(st.session_state.llm_output)

# Display the tree structure if data exists
if st.session_state.tree_data:
    st.subheader("Generated Tree Structure:")
    
    # Generate and display the condition tree
    query_struct = condition_tree(
        st.session_state.tree_data['config'],
        always_show_buttons=True,
        return_type='jsonLogic',
        tree=st.session_state.tree_data['tree'],
        key='tree'
    )
    
    # Store and display the query structure
    if query_struct:
        st.session_state.query_struct = query_struct
    else:
        st.error("No query structure generated.")