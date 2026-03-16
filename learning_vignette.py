import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

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

# ---- PAGINA 2 ----
st_autorefresh(interval=1000, key="game_refresh")

elif st.session_state.page == "spel":

    st.title("Hospital Shift Simulator")
    st.write("Tasks will appear while you work. Try to keep up!")

    # refresh elke seconde
    st_autorefresh(interval=1000, key="game_refresh")

    # 10 iconen tonen
    icons = st.session_state.icons[:10]

    cols = st.columns(5)
    for i, icon in enumerate(icons):
        with cols[i % 5]:
            if st.button(icon, key=f"icon_{i}"):
                # check of een taak dit icoon nodig had
                for task in st.session_state.active_tasks:
                    if task["icon"] == icon:
                        st.session_state.completed_tasks.append(task)
                        st.session_state.active_tasks.remove(task)
                        break

    # elke 7 seconden nieuwe taak
    if time.time() - st.session_state.last_task_time > 7:
        new_task = random.choice(st.session_state.tasks)
        st.session_state.active_tasks.append({
            "name": new_task["name"],
            "icon": new_task["icon"],
            "time": time.time()
        })
        st.session_state.last_task_time = time.time()

    st.divider()
    st.subheader("Active tasks")

    # taken tonen
    for task in st.session_state.active_tasks:
        if time.time() - task["time"] > 7:
            st.session_state.failed_tasks.append(task)
            st.session_state.active_tasks.remove(task)
            st.write(f"❌ {task['name']}")
        else:
            st.write(f"⏳ {task['name']}")

    st.subheader("Completed")
    for task in st.session_state.completed_tasks:
        st.write(f"✅ {task['name']}")
