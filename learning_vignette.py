import streamlit as st

# pagina bijhouden
if "page" not in st.session_state:
    st.session_state.page = "vraag"

# ---- PAGINA 1 ----
if st.session_state.page == "vraag":

    st.title("Learning vignette")
    st.write("Welcome to the learning vignette of group 48. Please start by answering the next question:")

    col1, col2 = st.columns([3,1])
    with col1:
        waarde = st.number_input(
            "Which percentage of employees in the health sector quit within their first year?",
            min_value=0,
            max_value=100,
            step=1,         # stap van 1%
            format="%d"     # hele getallen
        )
    with col2:
        st.write("%")

    # Submit knop om feedback pas te geven na bevestiging
    if st.button("Submit answer"):
        if 30 <= waarde <= 31:
            st.success("Correct! Well done. The actual percentage is 30.02%.")
            st.session_state.page = "spel"  # direct naar volgende pagina
            st.rerun()

        elif 20 <= waarde <= 40:
            st.info("You're close! The correct answer is 30.02%.")
            st.session_state.page = "spel"  # ook doorgaan bij dichtbij
            st.rerun()

        else:
            st.error("Your answer is quite far from the actual percentage. Try thinking about it again.")

# ---- PAGINA 2 ----
elif st.session_state.page == "spel":
    st.title("spel")
