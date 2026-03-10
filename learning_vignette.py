import streamlit as st

# session state om bij te houden op welke pagina we zitten
if "page" not in st.session_state:
    st.session_state.page = "vraag"

# ---- PAGINA 1: VRAAG ----
if st.session_state.page == "vraag":

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
                st.success("Correct! Well done. The actual percentage is 30.02%.")

                if st.button("Go to the next page"):
                    st.session_state.page = "spel"
                    st.rerun()

            elif 20 <= waarde <= 40:
                st.info("You're close! Your estimate is in the right range, but not quite correct.")

                if st.button("Continue to the next page"):
                    st.session_state.page = "spel"
                    st.rerun()

            else:
                st.error("Your answer is quite far from the actual percentage. Try thinking about it again.")

        except:
            st.warning("Please enter a valid number.")


# ---- PAGINA 2 ----
elif st.session_state.page == "spel":
    st.title("spel")
