import streamlit as st
import time

# pagina bijhouden
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
                st.rerun()

# ---- PAGINA 2 ----
# pagina "spel"
st.title("The Multitasking Trap")

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
    st.session_state.task_phase = 1  # fase 1 = makkelijk
    st.session_state.tasks_done = []

# tijd sinds start
elapsed = time.time() - st.session_state.start_time

# fase 2 na 10 seconden
if elapsed > 10:
    st.session_state.task_phase = 2

st.write("Simuleer het multitasken van healthcare workers!")

# ---- FASE 1: simpele taken ----
if st.session_state.task_phase == 1:
    st.subheader("Simple tasks:")
    
    col1, col2, col3 = st.columns(3)

    if col1.button("🔔 Patient call"):
        st.session_state.tasks_done.append("Patient call done")
        st.success("Patient call completed!")
    if col2.button("💊 Click medicine icon"):
        st.session_state.tasks_done.append("Medicine clicked")
        st.success("Medicine clicked!")
    if col3.button("📝 Type 'admin'"):
        admin_input = st.text_input("Type 'admin' here:")
        if admin_input.lower() == "admin":
            st.session_state.tasks_done.append("Admin task done")
            st.success("Admin task done!")

# ---- FASE 2: chaos ----
elif st.session_state.task_phase == 2:
    st.subheader("Chaos! Too many tasks at once! 😵")
    st.write("Healthcare workers often juggle multiple responsibilities simultaneously.")
    
    col1, col2, col3, col4 = st.columns(4)

    if col1.button("🔔 Patient call"):
        st.warning("Impossible to keep up!")
    if col2.button("💊 Click medicine icon"):
        st.warning("Impossible to keep up!")
    if col3.button("📝 Type 'admin'"):
        st.warning("Impossible to keep up!")
    if col4.button("📂 Drag patient dossier"):
        st.warning("Impossible to keep up!")

st.write("Tasks done:", st.session_state.tasks_done)
