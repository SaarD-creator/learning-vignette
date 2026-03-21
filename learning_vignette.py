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

                # ---- ICON DEFINITIONS ----

                st.session_state.icons = [
                    {"icon":"🔔","name":"Call bell"},
                    {"icon":"💊","name":"Medication"},
                    {"icon":"🛏️","name":"Patient bed"},
                    {"icon":"🩺","name":"Stethoscope"},
                    {"icon":"💉","name":"Injection"},
                    {"icon":"🧪","name":"Lab test"},
                    {"icon":"📋","name":"Patient chart"},
                    {"icon":"🧹","name":"Clean room"},
                    {"icon":"🧴","name":"Disinfect"},
                    {"icon":"🩹","name":"Bandage"}
                ]

                random.shuffle(st.session_state.icons)

                st.session_state.active_tasks = []
                st.session_state.completed_tasks = []

                st.session_state.task_count = 0
                st.session_state.last_task_time = time.time()



# ---- PAGINA 2 ----

elif st.session_state.page == "spel":

    st.title("Hospital Shift Simulator")
    st.write("Tasks appear while you work. Try to keep up.")

    st_autorefresh(interval=1000, key="refresh")

    # ---- GAME OVER STATE ----
    if "game_over" not in st.session_state:
        st.session_state.game_over = False

    # ---- INTERVAL BEPALEN ----
    if st.session_state.task_count < 3:
        interval = 5
    elif st.session_state.task_count < 6:
        interval = 3
    else:
        interval = 1

    # ---- NIEUWE TAKEN TOEVOEGEN ----
    if not st.session_state.game_over and st.session_state.task_count < 36:

        if time.time() - st.session_state.last_task_time > interval:

            new_task = random.choice(st.session_state.icons)

            st.session_state.active_tasks.append(new_task)

            st.session_state.task_count += 1
            st.session_state.last_task_time = time.time()

    # ---- STRESS BEREKENEN ----
    base_stress = len(st.session_state.active_tasks) / 10

    if "error_tasks" not in st.session_state:
        st.session_state.error_tasks = 0

    stress_level = base_stress + (st.session_state.error_tasks * 0.1)

    if stress_level >= 1:
        stress_level = 1
        st.session_state.game_over = True

    st.subheader("Stress level")
    st.progress(stress_level)

    # ---- TAKEN BOVENAAN ----
    st.subheader("Current tasks")
    for task in st.session_state.active_tasks:
        st.warning(f"Click the {task['name']} {task['icon']}")

    st.divider()

    # ---- ICON GRID ----
    cols = st.columns(5)

    for i, item in enumerate(st.session_state.icons):

        with cols[i % 5]:

            clicked = st.button(
                item["icon"],
                key=f"icon_{i}",
                use_container_width=True
            )

            if clicked:

                if st.session_state.game_over:
                    continue

                matched_task = None
                for task in st.session_state.active_tasks:
                    if task["icon"] == item["icon"]:
                        matched_task = task
                        break

                if matched_task:
                    st.session_state.completed_tasks.append(matched_task)
                    st.session_state.active_tasks.remove(matched_task)
                else:
                    st.session_state.error_tasks += 1
                    st.warning("⚠️ Wrong icon clicked! Stress increased.")

    # ---- GAME OVER OVERLAY ----
    if st.session_state.game_over:

        st.markdown(
            """
            <style>
            .overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.7);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 9999;
            }
            .message-box {
                background-color: white;
                padding: 40px;
                border-radius: 20px;
                text-align: center;
                max-width: 600px;
                box-shadow: 0 0 30px rgba(0,0,0,0.3);
            }
            .message-box h1 {
                color: red;
                font-size: 40px;
            }
            .message-box p {
                font-size: 20px;
            }
            </style>

            <div class="overlay">
                <div class="message-box">
                    <h1>⚠️ CRITICAL STRESS LEVEL</h1>
                    <p>The workload has become overwhelming.</p>
                    <p>This reflects the real pressure healthcare workers experience.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
