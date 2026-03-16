import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# ---- SESSION STATE INIT ----

if "page" not in st.session_state:
    st.session_state.page = "vraag"

if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False


# ---- PAGINA 1 ----

if st.session_state.page == "vraag":

    st.title("Learning vignette")

    st.write(
        "Welcome to the learning vignette of group 48. "
        "Please start by answering the next question:"
    )

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
            st.error(
                "Your answer is quite far from the actual percentage. "
                "Try thinking about it again."
            )

        if correct_of_dichtbij:

            if st.button("Go to the next page"):

                st.session_state.page = "spel"
                st.session_state.feedback_given = False

                # ---- GAME INIT ----

                st.session_state.icons = [
                    "🔔","💊","📝","📂","🛏️",
                    "🩺","🧴","🧪","🩹","💉",
                    "🧷","🧻","🩻","🧫","🧹",
                    "📋","🧸"
                ]

                random.shuffle(st.session_state.icons)

                st.session_state.tasks = [
                    {"name":"Click the bell","icon":"🔔"},
                    {"name":"Click the medicine","icon":"💊"},
                    {"name":"Click the document","icon":"📋"},
                    {"name":"Click the bed","icon":"🛏️"}
                ]

                st.session_state.active_tasks = []
                st.session_state.completed_tasks = []
                st.session_state.failed_tasks = []

                st.session_state.last_task_time = time.time()



# ---- PAGINA 2 ----

elif st.session_state.page == "spel":

    st.title("Hospital Shift Simulator")

    st.write(
        "Tasks will appear while you work. "
        "Try to keep up with the workload."
    )

    # auto refresh elke seconde
    st_autorefresh(interval=1000, key="game_refresh")

    # ---- ICON GRID ----

    icons = st.session_state.icons[:10]

    cols = st.columns(5)

    for i, icon in enumerate(icons):

        with cols[i % 5]:

            if st.button(icon, key=f"icon_{i}"):

                for task in st.session_state.active_tasks:

                    if task["icon"] == icon:

                        st.session_state.completed_tasks.append(task)
                        st.session_state.active_tasks.remove(task)
                        break


    # ---- NIEUWE TASK ELKE 7 SECONDEN ----

    if time.time() - st.session_state.last_task_time > 7:

        new_task = random.choice(st.session_state.tasks)

        st.session_state.active_tasks.append({
            "name": new_task["name"],
            "icon": new_task["icon"],
            "time": time.time()
        })

        st.session_state.last_task_time = time.time()


    st.divider()

    # ---- ACTIEVE TAKEN ----

    st.subheader("Active tasks")

    tasks_to_remove = []

    for task in st.session_state.active_tasks:

        if time.time() - task["time"] > 7:

            st.session_state.failed_tasks.append(task)
            tasks_to_remove.append(task)

        else:

            st.write(f"⏳ {task['name']}")

    for task in tasks_to_remove:
        st.session_state.active_tasks.remove(task)


    # ---- COMPLETED ----

    st.subheader("Completed")

    for task in st.session_state.completed_tasks:
        st.write(f"✅ {task['name']}")


    # ---- FAILED ----

    st.subheader("Missed")

    for task in st.session_state.failed_tasks:
        st.write(f"❌ {task['name']}")
