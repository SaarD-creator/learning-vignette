import streamlit as st

st.title("Learning vignette")

st.write("Welcome to the learning vignette of group 48. Please start by answering the next question:")

col1, col2 = st.columns([3,1])

with col1:
    antwoord = st.text_input("Which percentage of employees in the health sector quit within their first year?")

with col2:
    st.write("%")

if antwoord:
    try:
        waarde = float(antwoord.replace(",", "."))

        if 30 <= waarde <= 31:
            st.success("Correct! Well done. The actual percentage is around 30%.")
        elif 20 <= waarde <= 40:
            st.info("You're close! Your estimate is in the right range, but not quite correct.")
        else:
            st.error("Your answer is quite far from the actual percentage. Try thinking about it again.")

    except:
        st.warning("Please enter a valid number.")
