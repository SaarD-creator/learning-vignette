import streamlit as st

st.title("Learning vignette")

st.write("Welcome to the learning vignette of group 48. Please start by answering the next question:")

vraag = st.text_input("Which percentage of employees in the health sector quit within their first year?")

if vraag:
    st.write(f"Leuk je te ontmoeten, !")
