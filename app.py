import streamlit as st
from src.generate_recs import generate_recs, get_all_skills

st.title('Job Recommender - V2!')

print (get_all_skills())

options = st.multiselect(
    'Select the skill(s) you have from the list below',
    sorted(get_all_skills()),
    ['css', 'css framework'])

number = st.number_input('Enter maximum number of recommendations', min_value=5, max_value=20, value=10)

if st.button('Generate recommendations'):
    if len(options) != 0:
        st.markdown(generate_recs(options, num_recs=10), unsafe_allow_html=True)
    
    else:
        st.markdown("Select at least one skill for recommendations!", unsafe_allow_html=True)