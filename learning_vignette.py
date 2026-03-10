import streamlit as st

st.title("Mijn eerste Streamlit App")

st.write("Hallo! Deze app draait via GitHub en Streamlit Cloud.")

naam = st.text_input("Wat is je naam?")

if naam:
    st.write(f"Leuk je te ontmoeten, {naam}!")
