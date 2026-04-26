import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# ---- SESSION STATE INIT ----

if "page" not in st.session_state:
    st.session_state.page = "vraag"

if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = False

if "icons" not in st.session_state:
    st.session_state.icons = []

if "active_tasks" not in st.session_state:
    st.session_state.active_tasks = []

if "completed_tasks" not in st.session_state:
    st.session_state.completed_tasks = []

if "task_count" not in st.session_state:
    st.session_state.task_count = 0

if "last_task_time" not in st.session_state:
    st.session_state.last_task_time = time.time()

if "error_tasks" not in st.session_state:
    st.session_state.error_tasks = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "game_over_time" not in st.session_state:
    st.session_state.game_over_time = None

if "start_time_info" not in st.session_state:
    st.session_state.start_time_info = None


# ---- CALLBACK: Go to next page ----

def go_to_spel():
    st.session_state.page = "spel"
    st.session_state.feedback_given = False

    # RESET STATE
    st.session_state.game_over = False
    st.session_state.game_over_time = None
    st.session_state.start_time_info = None
    st.session_state.error_tasks = 0

    # ICONS
    icons = [
        {"icon": "🔔", "name": "Call bell"},
        {"icon": "💊", "name": "Medication"},
        {"icon": "🛏️", "name": "Patient bed"},
        {"icon": "🩺", "name": "Stethoscope"},
        {"icon": "💉", "name": "Injection"},
        {"icon": "🧪", "name": "Lab test"},
        {"icon": "📋", "name": "Patient chart"},
        {"icon": "🧹", "name": "Clean room"},
        {"icon": "🧴", "name": "Disinfect"},
        {"icon": "🩹", "name": "Bandage"}
    ]
    random.shuffle(icons)
    st.session_state.icons = icons

    st.session_state.active_tasks = []
    st.session_state.completed_tasks = []
    st.session_state.task_count = 0
    st.session_state.last_task_time = time.time()


# ---- PAGINA 1 ----

if st.session_state.page == "vraag":

    st.title("Learning vignette")

    st.write(
        "Welcome to the learning vignette of group 48. "
        "Please start by answering the next question:"
    )

    col1, col2 = st.columns([3, 1])

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
            # FIX: use on_click callback so the page switches in a single click
            st.button("Go to the next page", on_click=go_to_spel)


# ---- PAGINA 2 ----

elif st.session_state.page == "spel":

    st.title("Hospital Shift Simulator")
    st.write("Tasks appear while you work. Try to keep up.")

    st_autorefresh(interval=1000, key="refresh")

    # ---- INTERVAL ----
    if st.session_state.task_count < 3:
        interval = 5
    elif st.session_state.task_count < 6:
        interval = 3
    else:
        interval = 1

    # ---- NIEUWE TAKEN ----
    if not st.session_state.game_over and st.session_state.task_count < 36:

        if time.time() - st.session_state.last_task_time > interval:

            new_task = random.choice(st.session_state.icons)
            st.session_state.active_tasks.append(new_task)

            st.session_state.task_count += 1
            st.session_state.last_task_time = time.time()

    # ---- STRESS ----
    base_stress = len(st.session_state.active_tasks) / 10
    stress_level = base_stress + (st.session_state.error_tasks * 0.1)

    if stress_level >= 1:
        stress_level = 1
        st.session_state.game_over = True

    # ---- STRESS BAR IN SIDEBAR (always visible) ----
    with st.sidebar:
        st.subheader("🧠 Stress level")
        st.progress(stress_level)
        stress_pct = int(stress_level * 100)
        if stress_pct < 40:
            st.success(f"{stress_pct}% — Under control")
        elif stress_pct < 70:
            st.warning(f"{stress_pct}% — Getting busy!")
        else:
            st.error(f"{stress_pct}% — Critical!")

    # ---- TAKEN ----
    st.subheader("Current tasks")
    for task in st.session_state.active_tasks:
        st.warning(f"Click the {task['name']} {task['icon']}")

    st.divider()

    # ---- ICON GRID ----
    st.markdown(
        """
        <style>
        div[data-testid="stButton"] > button {
            font-size: 3.5rem !important;
            line-height: 1 !important;
            height: 5rem !important;
            min-height: 5rem !important;
            padding: 0.5rem !important;
        }
        div[data-testid="stButton"] > button p {
            font-size: 3.5rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

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

        if st.session_state.game_over_time is None:
            st.session_state.game_over_time = time.time()

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

        # NA 5 SEC NAAR INFO
        if time.time() - st.session_state.game_over_time > 5:
            st.session_state.page = "info"
            st.session_state.game_over_time = None
            st.rerun()


# ---- PAGINA 3 ----

elif st.session_state.page == "info":

    st.title("What's really going on?")

    st_autorefresh(interval=1000, key="info_refresh")

    if st.session_state.start_time_info is None:
        st.session_state.start_time_info = time.time()

    elapsed = int(time.time() - st.session_state.start_time_info)
    step = elapsed // 3

    teksten = [
        "30.2% of healthcare workers leave their job within the first year.",
        "That means: nearly one in three new employees is gone… before they are fully trained.",
        "And this is happening while the healthcare sector is already facing staff shortages.",
        "We train people, we recruit them… yet we fail to retain them.",
        "The core of the problem? Transition shock.",
        "The gap between expectations… and reality.",
        "New employees are immediately confronted with high workloads, intense emotions, and heavy responsibilities.",
        "What should feel like a growth phase often feels like survival.",
        "A lack of self-confidence plays a major role.",
        "And without proper guidance, many feel left alone.",
        "The result: people leave… and the pressure on those who remain increases.",
        "A vicious cycle is created.",
        "The problem is not inflow.",
        "The problem is retention… in that first year.",
        "If we truly want to make an impact, this is where we need to intervene.",
        "And that is exactly what our solution focuses on."
    ]

    for i in range(min(step + 1, len(teksten))):
        st.write(teksten[i])
    # Show button only after all texts have appeared
    if step + 1 >= len(teksten):
        st.markdown("<br>", unsafe_allow_html=True)
        st.button(
            "✨ Discover the CARE start program",
            on_click=lambda: st.session_state.update({"page": "care"}),
            use_container_width=True
        )


# ---- PAGINA 4: CARE ----

elif st.session_state.page == "care":

    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">

        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #FDF3E7 0%, #FAE8D0 40%, #F5DEC8 100%);
        }
        [data-testid="stHeader"] { background: transparent !important; }
        .main .block-container { padding-top: 2rem !important; }

        .care-title {
            font-family: 'Crimson Text', serif;
            font-size: clamp(1.4rem, 3vw, 2rem);
            color: #6B3A2A;
            text-align: center;
            letter-spacing: 0.04em;
            margin-bottom: 0.2rem;
        }
        .care-tagline {
            font-family: 'Crimson Text', serif;
            font-style: italic;
            font-size: 1.1rem;
            color: #A0624A;
            text-align: center;
            margin-bottom: 2.5rem;
        }
        .care-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            max-width: 860px;
            margin: 0 auto 2.5rem auto;
        }
        .care-card {
            perspective: 900px;
            cursor: pointer;
            height: 280px;
        }
        .care-card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            transform-style: preserve-3d;
            transition: transform 0.65s cubic-bezier(0.4, 0.2, 0.2, 1);
            border-radius: 20px;
        }
        .care-card.flipped .care-card-inner { transform: rotateY(180deg); }
        .care-front, .care-back {
            position: absolute;
            inset: 0;
            backface-visibility: hidden;
            -webkit-backface-visibility: hidden;
            border-radius: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 1.2rem;
        }
        .care-front { box-shadow: 0 8px 32px rgba(100,40,20,0.13), 0 2px 8px rgba(100,40,20,0.08); }
        .card-c .care-front { background: linear-gradient(160deg, #C4663A, #E07B50); }
        .card-a .care-front { background: linear-gradient(160deg, #D4933A, #EFB55A); }
        .card-r .care-front { background: linear-gradient(160deg, #7A9E7E, #9DC49F); }
        .card-e .care-front { background: linear-gradient(160deg, #C4737A, #E09298); }
        .care-letter {
            font-family: 'Playfair Display', serif;
            font-weight: 900;
            font-size: 6.5rem;
            color: rgba(255,255,255,0.95);
            line-height: 1;
            text-shadow: 0 4px 18px rgba(0,0,0,0.18);
        }
        .care-hint {
            font-family: 'Crimson Text', serif;
            font-style: italic;
            font-size: 0.85rem;
            color: rgba(255,255,255,0.75);
            margin-top: 0.5rem;
        }
        .care-back {
            transform: rotateY(180deg);
            box-shadow: 0 8px 32px rgba(100,40,20,0.13);
        }
        .card-c .care-back { background: linear-gradient(160deg, #FAF0EA, #FDE8DC); border: 2px solid #E07B50; }
        .card-a .care-back { background: linear-gradient(160deg, #FDF5E8, #FEE9C4); border: 2px solid #EFB55A; }
        .card-r .care-back { background: linear-gradient(160deg, #EFF6F0, #D9EDD9); border: 2px solid #9DC49F; }
        .card-e .care-back { background: linear-gradient(160deg, #FBF0F1, #FDE0E2); border: 2px solid #E09298; }
        .care-back-letter {
            font-family: 'Playfair Display', serif;
            font-weight: 900;
            font-size: 2.8rem;
            line-height: 1;
        }
        .card-c .care-back-letter { color: #C4663A; }
        .card-a .care-back-letter { color: #C47A2A; }
        .card-r .care-back-letter { color: #4A7A4E; }
        .card-e .care-back-letter { color: #B05860; }
        .care-word {
            font-family: 'Playfair Display', serif;
            font-size: 1.05rem;
            font-weight: 700;
            margin-top: 0.4rem;
            text-align: center;
        }
        .card-c .care-word { color: #8B3A20; }
        .card-a .care-word { color: #8B5A10; }
        .card-r .care-word { color: #2A5A2E; }
        .card-e .care-word { color: #8B3840; }
        .care-desc {
            font-family: 'Crimson Text', serif;
            font-size: 0.95rem;
            line-height: 1.45;
            text-align: center;
            margin-top: 0.7rem;
            color: #5A3A30;
        }
        .care-footer {
            font-family: 'Crimson Text', serif;
            font-style: italic;
            text-align: center;
            color: #A0624A;
            font-size: 1rem;
            margin-top: 0.5rem;
        }
        </style>

        <div class="care-title">Our solution</div>
        <h1 style="font-family:'Playfair Display',serif; font-weight:900; font-size:clamp(2.8rem,7vw,5rem);
                   text-align:center; color:#6B3A2A; letter-spacing:0.12em; margin:0 0 0.1rem 0;
                   text-shadow: 2px 3px 0px rgba(180,80,40,0.15);">
            CARE start
        </h1>
        <div class="care-tagline">Click each letter to explore the program</div>

        <div class="care-grid">
          <div class="care-card card-c" onclick="this.classList.toggle('flipped')">
            <div class="care-card-inner">
              <div class="care-front">
                <div class="care-letter">C</div>
                <div class="care-hint">tap to reveal</div>
              </div>
              <div class="care-back">
                <div class="care-back-letter">C</div>
                <div class="care-word">Coaching</div>
                <div class="care-desc">Personal guidance from an experienced mentor who helps navigate the first year.</div>
              </div>
            </div>
          </div>
          <div class="care-card card-a" onclick="this.classList.toggle('flipped')">
            <div class="care-card-inner">
              <div class="care-front">
                <div class="care-letter">A</div>
                <div class="care-hint">tap to reveal</div>
              </div>
              <div class="care-back">
                <div class="care-back-letter">A</div>
                <div class="care-word">Adaptation support</div>
                <div class="care-desc">Structured support to ease the transition from education into professional healthcare.</div>
              </div>
            </div>
          </div>
          <div class="care-card card-r" onclick="this.classList.toggle('flipped')">
            <div class="care-card-inner">
              <div class="care-front">
                <div class="care-letter">R</div>
                <div class="care-hint">tap to reveal</div>
              </div>
              <div class="care-back">
                <div class="care-back-letter">R</div>
                <div class="care-word">Resilience training</div>
                <div class="care-desc">Building the mental strength to handle pressure, setbacks and emotional intensity.</div>
              </div>
            </div>
          </div>
          <div class="care-card card-e" onclick="this.classList.toggle('flipped')">
            <div class="care-card-inner">
              <div class="care-front">
                <div class="care-letter">E</div>
                <div class="care-hint">tap to reveal</div>
              </div>
              <div class="care-back">
                <div class="care-back-letter">E</div>
                <div class="care-word">Early feedback</div>
                <div class="care-desc">Timely, constructive feedback loops that build confidence and prevent silent struggles.</div>
              </div>
            </div>
          </div>
        </div>

        <div class="care-footer">✦ Together, these four pillars make healthcare workers stay. ✦</div>
        """,
        unsafe_allow_html=True
    )
