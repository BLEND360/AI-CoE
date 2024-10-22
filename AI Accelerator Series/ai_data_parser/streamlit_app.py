import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator.utilities import (
                                               Hasher,
                                               LoginError,
                                               )

st.set_page_config(layout="wide")

with open('auth.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# hashed_passwords = stauth.Hasher(['DataParserDemo101']).generate()
# print(hashed_passwords)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)
try:
    authenticator.login('main')
except LoginError as e:
    st.error(e)

if st.session_state["authentication_status"]:
        authenticator.logout('Logout','sidebar')
        # Main streamlit app
        intro_page = st.Page("pages/introduction_page.py", title="Introduction")
        audience_filt_page = st.Page("pages/audience_filtration.py", title="Audience Filtration")
        product_categ_page = st.Page("pages/product_categorization.py", title="Product Categorization")
        resume_parser_page = st.Page("pages/resume_parser.py", title="Resume Parser")

        pg = st.navigation([intro_page, audience_filt_page, product_categ_page, resume_parser_page])
        pg.run()
        #st.write(f'Welcome *{st.session_state["name"]}*')
elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

