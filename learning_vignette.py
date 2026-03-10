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
        antwoord = st.text_input(
            "Which percentage of employees in the health sector quit within their first year?",
            key="antwoord"
        )
    with col2:
        st.write("%")

    # feedback en knop alleen tonen als er iets is ingevuld
    if antwoord:
        try:
            waarde = float(antwoord.replace(",", "."))
            correct_of_dichtbij = False

            if 30 <= waarde <= 31:
                st.success("Correct! Well done. The actual percentage is 30.02%.")
                correct_of_dichtbij = True
            elif 20 <= waarde <= 40:
                st.info("You're close! The correct answer is 30.2%.")
                correct_of_dichtbij = True
            else:
                st.error("Your answer is quite far from the actual percentage. Try thinking about it again.")

            # **knop verschijnt pas hier, en switch gebeurt pas als je klikt**
            if correct_of_dichtbij:
                if st.button("Go to the next page"):
                    st.session_state.page = "spel"
                    st.session_state.antwoord = ""  # reset input voor toekomstige runs
                    st.rerun()

# ---- PAGINA 2 ----
elif st.session_state.page == "spel":
    st.title("spel")
