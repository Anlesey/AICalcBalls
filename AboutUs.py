import streamlit as st

# if st.button('太长不听，先试为敬！', use_container_width = True):
#     st.switch_page("pages/赛程表.py")

with open('Readme.md', encoding='utf-8') as f:
    st.markdown(f.read())
