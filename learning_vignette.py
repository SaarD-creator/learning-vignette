import streamlit as st
import random
import time

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
        st.session_state.feedback_given = True
        correct_of_dichtbij = False

        if 30 <= waarde <= 31:
            st.success("Correct! Well done. The actual percentage is 30.02%.")
            correct_of_dichtbij = True
        elif 20 <= waarde <= 40:
            st.info("You're close! The correct answer is 30.02%.")
            correct_of_dichtbij = True
        else:
            st.error("Your answer is quite far from the actual percentage. Try thinking about it again.")

        if correct_of_dichtbij:
            if st.button("Go to the next page"):
                st.session_state.page = "spel"
                st.session_state.feedback_given = False
                # --- initialize game ---
                st.session_state.task_index = 0
                st.session_state.task_start_time = time.time()
                st.session_state.task_results = []
                st.session_state.clicked_icon = None
                st.session_state.icons = [
                    "🔔","💊","📝","📂","🛏️","🩺","🧴","🧪","🩹","💉",
                    "🧷","🧻","🩻","🩺","🧫","🧹","🧪","📋","🩺","🧸"
                ]
                random.shuffle(st.session_state.icons)
                st.session_state.tasks = [
                    {"name":"Click the bell","icon":"🔔"},
                    {"name":"Click the medicine","icon":"💊"},
                    {"name":"Type 'admin'","icon":"📝"},
                    {"name":"Drag the patient to bed","icon":"🛏️"}
                ]
                st.rerun()

# ---- PAGINA 2 ----
elif st.session_state.page == "spel":
    import time, random

    st.title("The Multitasking Trap")

    # initialize game state
    if "task_index" not in st.session_state:
        st.session_state.task_index = 0
        st.session_state.task_start_time = time.time()
        st.session_state.task_results = []
        st.session_state.clicked_icon = None
        st.session_state.icons = [
            "🔔","💊","📝","📂","🛏️","🩺","🧴","🧪","🩹","💉",
            "🧷","🧻","🩻","🩺","🧫","🧹","🧪","📋","🩺","🧸"
        ]
        random.shuffle(st.session_state.icons)
        st.session_state.tasks = [
            {"name":"Click the bell","icon":"🔔"},
            {"name":"Click the medicine","icon":"💊"},
            {"name":"Type 'admin'","icon":"📝"},
            {"name":"Drag the patient to bed","icon":"🛏️"}
        ]

    elapsed = time.time() - st.session_state.task_start_time
    current_index = st.session_state.task_index

    # check of alle taken klaar zijn
    if current_index >= len(st.session_state.tasks):
        st.balloons()
        st.success("All tasks done!")

    else:
        # check tijdsoverschrijding
        if elapsed > 4:
            if st.session_state.clicked_icon != st.session_state.tasks[current_index]["icon"]:
                st.session_state.task_results.append({
                    "task": st.session_state.tasks[current_index]["name"],
                    "result": "failed"
                })
            st.session_state.task_index += 1
            st.session_state.task_start_time = time.time()
            st.session_state.clicked_icon = None
            st.experimental_rerun()

        # huidige taak tonen
        current_task = st.session_state.tasks[current_index]
        st.subheader(f"Task: {current_task['name']} (click the correct icon!)")

        # toon iconen met unieke keys
        cols = st.columns(5)
        for idx, icon in enumerate(st.session_state.icons):
            col = random.choice(cols)
            key_name = f"{icon}_{idx}_{current_index}"  # uniek
            # buiten de loop geen rerun meer
            clicked = col.button(icon, key=key_name)
            if clicked:
                st.session_state.clicked_icon = icon
                if icon == current_task["icon"]:
                    st.session_state.task_results.append({
                        "task": current_task["name"],
                        "result": "completed"
                    })
                    # update voor volgende taak zonder rerun in loop
                    st.session_state.task_index += 1
                    st.session_state.task_start_time = time.time()
                    st.session_state.clicked_icon = None
                    # break loop zodat we 1 klik per run verwerken
                    break
                else:
                    st.warning("Wrong icon!")

        st.write("Task results so far:", st.session_state.task_results)
