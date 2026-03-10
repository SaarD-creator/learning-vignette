import streamlit as st
import random

# ---- Pagina bijhouden ----
if "page" not in st.session_state:
    st.session_state.page = "vraag"

# feedback bewaren
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

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
            step=1,       
            format="%d"
        )
    with col2:
        st.write("%")

    # Submit-knop om feedback te geven
    if st.button("Submit answer") or st.session_state.feedback_given:
        st.session_state.feedback_given = True  # onthoud dat feedback gegeven is
        correct_of_dichtbij = False

        if 30 <= waarde <= 31:
            st.success("Correct! Well done. The actual percentage is 30.02%.")
            correct_of_dichtbij = True
        elif 20 <= waarde <= 40:
            st.info("You're close! The correct answer is 30.02%.")
            correct_of_dichtbij = True
        else:
            st.error("Your answer is quite far from the actual percentage. Try thinking about it again.")

        # knop om naar de volgende pagina te gaan
        if correct_of_dichtbij:
            if st.button("Go to the next page"):
                st.session_state.page = "spel"
                st.session_state.feedback_given = False  # reset voor volgende run
                # init game state
                st.session_state.task_step = 0
                st.rerun()


# ---- PAGINA 2: spel ----
elif st.session_state.page == "spel":
    st.title("The Multitasking Trap")

    # initialize game state
    if "task_step" not in st.session_state:
        st.session_state.task_step = 0

    # takenlijst
    tasks = [
        {"name": "klik het belletje", "icon": "🔔"},
        {"name": "leg de patiënt in bed", "icon": "🛏️"}
    ]

    current_task = tasks[st.session_state.task_step]

    st.subheader(f"Task: {current_task['name']}")

    # simuleren van icoontjes verspreid over het scherm
    cols = st.columns(5)
    positions = list(range(5))
    random.shuffle(positions)

    # toon icoontjes
    clicked_correct = False
    for i, col in enumerate(cols):
        # de juiste icoon bij een random positie
        if i == positions[0]:
            if col.button(current_task["icon"]):
                clicked_correct = True
        else:
            col.write("⬜")  # lege plek / distractor

    if clicked_correct:
        st.success(f"Task '{current_task['name']}' completed!")
        st.session_state.task_step += 1
        st.experimental_rerun()  # laat de volgende taak zien

    # einde
    if st.session_state.task_step >= len(tasks):
        st.balloons()
        st.write("All simple tasks completed! 🎉")
