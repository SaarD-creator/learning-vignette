import streamlit as st
import streamlit.components.v1 as components
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

# ---- DEV SHORTCUTS: sidebar expander to jump to any page ----
with st.sidebar:
    with st.expander("🛠️ Dev shortcuts"):
        if st.button("→ CARE start program", key="dev_care"):
            st.session_state.page = "care"
            st.rerun()
        if st.button("→ Info page", key="dev_info"):
            st.session_state.page = "info"
            st.session_state.start_time_info = None
            st.rerun()
        if st.button("→ Sudoku", key="dev_sudoku"):
            st.session_state.page = "sudoku"
            st.rerun()
        if st.button("→ Game", key="dev_spel"):
            go_to_spel()
            st.rerun()


# ---- CALLBACK: Go to game page ----

def go_to_spel():
    st.session_state.page = "spel"
    st.session_state.feedback_given = False
    st.session_state.game_over = False
    st.session_state.game_over_time = None
    st.session_state.start_time_info = None
    st.session_state.error_tasks = 0
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


# ======================================================
# PAGINA 1
# ======================================================

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
            min_value=0, max_value=100, step=1, format="%d"
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
            st.button("Go to the next page", on_click=go_to_spel)


# ======================================================
# PAGINA 2
# ======================================================

elif st.session_state.page == "spel":

    st.title("Hospital Shift Simulator")
    st.write("Tasks appear while you work. Try to keep up.")

    st_autorefresh(interval=1000, key="refresh")

    if st.session_state.task_count < 3:
        interval = 5
    elif st.session_state.task_count < 6:
        interval = 3
    else:
        interval = 1

    if not st.session_state.game_over and st.session_state.task_count < 36:
        if time.time() - st.session_state.last_task_time > interval:
            new_task = random.choice(st.session_state.icons)
            st.session_state.active_tasks.append(new_task)
            st.session_state.task_count += 1
            st.session_state.last_task_time = time.time()

    base_stress = len(st.session_state.active_tasks) / 10
    stress_level = base_stress + (st.session_state.error_tasks * 0.1)
    if stress_level >= 1:
        stress_level = 1
        st.session_state.game_over = True

    # ---- STRESS BAR IN SIDEBAR ----
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
            clicked = st.button(item["icon"], key=f"icon_{i}", use_container_width=True)
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
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background-color: rgba(0,0,0,0.7);
                display: flex; justify-content: center; align-items: center; z-index: 9999;
            }
            .message-box {
                background-color: white; padding: 40px; border-radius: 20px;
                text-align: center; max-width: 600px;
                box-shadow: 0 0 30px rgba(0,0,0,0.3);
            }
            .message-box h1 { color: red; font-size: 40px; }
            .message-box p { font-size: 20px; }
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

        if time.time() - st.session_state.game_over_time > 5:
            st.session_state.page = "info"
            st.session_state.game_over_time = None
            st.rerun()


# ======================================================
# PAGINA 3
# ======================================================

elif st.session_state.page == "info":

    st.title("What's really going on?")

    st_autorefresh(interval=1000, key="info_refresh")

    if st.session_state.start_time_info is None:
        st.session_state.start_time_info = time.time()

    elapsed = int(time.time() - st.session_state.start_time_info)
    step = elapsed // 3

    teksten = [
        "30.2% of healthcare workers leave their job within the first year — nearly one in three.",
        "This happens while the sector is already facing serious staff shortages.",
        "We recruit, we train… yet we fail to retain.",
        "The core of the problem? Transition shock — the gap between expectations and reality.",
        "From day one, new employees face high workloads, intense emotions, and heavy responsibilities.",
        "Without confidence and guidance, what should feel like growth feels like survival.",
        "People leave. Pressure on those who remain increases. A vicious cycle.",
        "The problem is not inflow — it's retention in that first year.",
        "And that is exactly where our solution intervenes."
    ]

    for i in range(min(step + 1, len(teksten))):
        st.write(teksten[i])

    if step + 1 >= len(teksten):
        st.markdown("<br>", unsafe_allow_html=True)
        st.button(
            "✨ Discover the CARE start program",
            on_click=lambda: st.session_state.update({"page": "care"}),
            use_container_width=True
        )


# ======================================================
# PAGINA 4: CARE START PROGRAM
# ======================================================

elif st.session_state.page == "care":

    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #FDF3E7 0%, #FAE8D0 40%, #F5DEC8 100%);
        }
        [data-testid="stHeader"] { background: transparent !important; }
        .main .block-container { padding-top: 2rem !important; }
        </style>

        <div style="font-family:'Crimson Text',serif; font-size:1.3rem; color:#6B3A2A;
                    text-align:center; letter-spacing:0.06em; margin-bottom:0.1rem;">
            Our solution
        </div>
        <h1 style="font-family:'Playfair Display',serif; font-weight:900;
                   font-size:clamp(1.8rem,4.5vw,4rem); text-align:center; color:#6B3A2A;
                   letter-spacing:0.08em; margin:0 0 0.2rem 0; white-space:nowrap;
                   text-shadow: 2px 3px 0px rgba(180,80,40,0.15);">
            CARE start program
        </h1>
        <div style="font-family:'Crimson Text',serif; font-style:italic; font-size:1.05rem;
                    color:#A0624A; text-align:center; margin-bottom:1rem;">
            Click each letter to reveal what it stands for
        </div>
    """, unsafe_allow_html=True)

    # ---- Interactive flip cards via components.html (JS fully works here) ----
    components.html("""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <style>
      * { box-sizing: border-box; margin: 0; padding: 0; }
      body { background: transparent; font-family: sans-serif; }

      .grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 18px;
        max-width: 820px;
        margin: 0 auto 1.5rem auto;
        padding: 8px;
      }

      .card {
        perspective: 900px;
        cursor: pointer;
        height: 260px;
        user-select: none;
      }

      .card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1);
        border-radius: 22px;
      }

      .card.flipped .card-inner {
        transform: rotateY(180deg);
      }

      .face {
        position: absolute;
        inset: 0;
        border-radius: 22px;
        backface-visibility: hidden;
        -webkit-backface-visibility: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 1.2rem;
      }

      .front { box-shadow: 0 10px 36px rgba(100,40,20,0.16); }
      .c .front { background: linear-gradient(150deg, #C4663A, #E07B50); }
      .a .front { background: linear-gradient(150deg, #D4933A, #EFB55A); }
      .r .front { background: linear-gradient(150deg, #7A9E7E, #9DC49F); }
      .e .front { background: linear-gradient(150deg, #C4737A, #E09298); }

      .big-letter {
        font-family: 'Playfair Display', serif;
        font-weight: 900;
        font-size: 7rem;
        color: rgba(255,255,255,0.95);
        line-height: 1;
        text-shadow: 0 5px 20px rgba(0,0,0,0.2);
        transition: transform 0.2s;
      }
      .card:hover:not(.flipped) .big-letter { transform: scale(1.07); }

      .tap-hint {
        font-family: 'Crimson Text', serif;
        font-style: italic;
        font-size: 0.82rem;
        color: rgba(255,255,255,0.7);
        margin-top: 8px;
      }

      .back {
        transform: rotateY(180deg);
        box-shadow: 0 10px 36px rgba(100,40,20,0.13);
      }
      .c .back { background: #FDE8DC; border: 2.5px solid #E07B50; }
      .a .back { background: #FEE9C4; border: 2.5px solid #EFB55A; }
      .r .back { background: #D9EDD9; border: 2.5px solid #9DC49F; }
      .e .back { background: #FDE0E2; border: 2.5px solid #E09298; }

      .back-letter {
        font-family: 'Playfair Display', serif;
        font-weight: 900;
        font-size: 3rem;
        line-height: 1;
      }
      .c .back-letter { color: #C4663A; }
      .a .back-letter { color: #C47A2A; }
      .r .back-letter { color: #4A7A4E; }
      .e .back-letter { color: #B05860; }

      .word {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 1.15rem;
        text-align: center;
        margin-top: 14px;
        line-height: 1.3;
      }
      .c .word { color: #8B3A20; }
      .a .word { color: #8B5A10; }
      .r .word { color: #2A5A2E; }
      .e .word { color: #8B3840; }

      .footer {
        font-family: 'Crimson Text', serif;
        font-style: italic;
        text-align: center;
        color: #A0624A;
        font-size: 1rem;
        padding-bottom: 10px;
      }
    </style>

    <div class="grid">

      <div class="card c" onclick="this.classList.toggle('flipped')">
        <div class="card-inner">
          <div class="face front">
            <div class="big-letter">C</div>
            <div class="tap-hint">click to reveal</div>
          </div>
          <div class="face back">
            <div class="back-letter">C</div>
            <div class="word">Coaching</div>
          </div>
        </div>
      </div>

      <div class="card a" onclick="this.classList.toggle('flipped')">
        <div class="card-inner">
          <div class="face front">
            <div class="big-letter">A</div>
            <div class="tap-hint">click to reveal</div>
          </div>
          <div class="face back">
            <div class="back-letter">A</div>
            <div class="word">Adaptation support</div>
          </div>
        </div>
      </div>

      <div class="card r" onclick="this.classList.toggle('flipped')">
        <div class="card-inner">
          <div class="face front">
            <div class="big-letter">R</div>
            <div class="tap-hint">click to reveal</div>
          </div>
          <div class="face back">
            <div class="back-letter">R</div>
            <div class="word">Resilience training</div>
          </div>
        </div>
      </div>

      <div class="card e" onclick="this.classList.toggle('flipped')">
        <div class="card-inner">
          <div class="face front">
            <div class="big-letter">E</div>
            <div class="tap-hint">click to reveal</div>
          </div>
          <div class="face back">
            <div class="back-letter">E</div>
            <div class="word">Early feedback</div>
          </div>
        </div>
      </div>

    </div>

    <div class="footer">✦ Together, these four pillars make healthcare workers stay. ✦</div>
    """, height=340)
    # ---- Try it out button ----
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
        <style>
        div[data-testid="stButton"] > button {
            font-family: 'Playfair Display', serif !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            background: linear-gradient(135deg, #C4663A, #E07B50) !important;
            color: white !important;
            border: none !important;
            border-radius: 40px !important;
            padding: 0.75rem 2.5rem !important;
            box-shadow: 0 4px 16px rgba(196,102,58,0.35) !important;
            letter-spacing: 0.06em !important;
            transition: transform 0.15s, box-shadow 0.15s !important;
        }
        div[data-testid="stButton"] > button:hover {
            box-shadow: 0 6px 20px rgba(196,102,58,0.5) !important;
            transform: scale(1.03) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    st.button(
        "Try it out",
        on_click=lambda: st.session_state.update({"page": "sudoku"}),
        use_container_width=True
    )



# ======================================================
# PAGINA 5: SUDOKU
# ======================================================

elif st.session_state.page == "sudoku":

    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
        <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #FDF3E7 0%, #FAE8D0 40%, #F5DEC8 100%);
        }
        [data-testid="stHeader"] { background: transparent !important; }
        .main .block-container { padding-top: 1.5rem !important; }
        </style>
    """, unsafe_allow_html=True)

    components.html("""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <style>
      * { box-sizing: border-box; margin: 0; padding: 0; }
      body {
        background: linear-gradient(135deg, #FDF3E7 0%, #FAE8D0 40%, #F5DEC8 100%);
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 10px 16px 16px;
        font-family: 'Crimson Text', serif;
        min-height: 100vh;
        overflow: hidden;
      }

      h1 {
        font-family: 'Playfair Display', serif;
        font-weight: 900;
        font-size: 1.7rem;
        color: #6B3A2A;
        text-align: center;
        margin-bottom: 2px;
        text-shadow: 1px 2px 0 rgba(180,80,40,0.12);
      }
      .subtitle {
        font-family: 'Crimson Text', serif;
        font-style: italic;
        font-size: 0.95rem;
        color: #A0624A;
        text-align: center;
        margin-bottom: 8px;
      }

      /* ---- Sudoku grid ---- */
      #sudoku {
        display: grid;
        grid-template-columns: repeat(9, 50px);
        grid-template-rows: repeat(9, 50px);
        border: 3px solid #8B3A20;
        background: #C4866A;
        gap: 1px;
        box-shadow: 0 8px 32px rgba(100,40,20,0.18);
        border-radius: 6px;
        overflow: hidden;
      }

      .cell {
        width: 50px; height: 50px;
        background: #FDF6EC;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.35rem;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        color: #4A2510;
        position: relative;
        transition: background 0.3s;
      }
      /* thick box borders */
      .cell[data-col="3"], .cell[data-col="6"] { border-left: 2.5px solid #8B3A20; }
      .cell[data-row="3"], .cell[data-row="6"] { border-top: 2.5px solid #8B3A20; }

      .cell.empty { cursor: text; }
      .cell.empty input {
        width: 100%; height: 100%;
        border: none; background: transparent;
        text-align: center;
        font-size: 1.35rem;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        color: #C4663A;
        outline: none;
        cursor: text;
      }
      /* feedback states */
      .cell.correct { background: #C8F0D0; animation: flashGreen 0.5s ease; }
      .cell.wrong   { background: #FFD0CC !important; }
      @keyframes flashGreen {
        0%   { background: #7BE89A; }
        100% { background: #C8F0D0; }
      }

      /* ---- Coaching highlights ---- */
      .cell.coach-stripe {
        background: #FBBF7A !important;
        transition: background 0.5s;
      }
      .cell.coach-num {
        background: #E07B50 !important;
        color: white !important;
        font-weight: 900 !important;
        font-size: 1.6rem !important;
        transition: background 0.5s;
      }
      .cell.coach-box { /* border drawn via overlay div, no background */ }

      #coach-hint {
        font-family: 'Crimson Text', serif;
        font-style: italic;
        font-size: 1rem;
        color: #6B3A2A;
        background: #FDE8D0;
        border-left: 3px solid #C4663A;
        border-radius: 6px;
        padding: 8px 14px;
        margin: 8px auto 0;
        max-width: 460px;
        text-align: center;
        animation: fadeIn 0.5s ease forwards;
      }
      /* ---- Floating task icons ---- */
      .task-icon {
        position: fixed;
        font-size: 2.8rem;
        cursor: pointer;
        z-index: 500;
        animation: pulse 0.8s ease-in-out infinite alternate;
        filter: drop-shadow(0 0 8px rgba(196,102,58,0.7));
        user-select: none;
        background: rgba(255,255,255,0.88);
        border-radius: 50%;
        padding: 4px;
        line-height: 1;
        transition: transform 0.15s;
      }
      .task-icon:hover { transform: scale(1.15); }
      .task-icon.warn    { filter: drop-shadow(0 0 10px rgba(220,140,0,0.9)); animation: pulse-warn 0.5s ease-in-out infinite alternate; }
      .task-icon.urgent  { filter: drop-shadow(0 0 13px rgba(200,30,30,0.95)); animation: pulse-urgent 0.22s ease-in-out infinite alternate; }
      .task-icon.clicked { transform: scale(0); opacity: 0; transition: transform 0.22s, opacity 0.22s; }

      .sad-icon {
        position: fixed; font-size: 2.8rem; z-index: 500;
        animation: fadeout 2s forwards; user-select: none; line-height: 1;
      }

      @keyframes pulse        { from{transform:scale(1)}   to{transform:scale(1.1)} }
      @keyframes pulse-warn   { from{transform:scale(1)}   to{transform:scale(1.15)} }
      @keyframes pulse-urgent { from{transform:scale(0.95)} to{transform:scale(1.2)} }
      @keyframes fadeout      { 0%{opacity:1;transform:scale(1)} 60%{opacity:1;transform:scale(1.1)} 100%{opacity:0;transform:scale(0.6)} }

      /* ---- Countdown timer ---- */
      #timer-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 8px;
      }
      #timer-display {
        font-family: 'Playfair Display', serif;
        font-weight: 900;
        font-size: 2.2rem;
        color: #6B3A2A;
        letter-spacing: 0.05em;
        text-shadow: 1px 2px 0 rgba(180,80,40,0.12);
        line-height: 1;
        transition: color 0.4s;
      }
      #timer-display.warning { color: #C4663A; }
      #timer-display.urgent  { color: #B02020; animation: pulse-urgent 0.4s ease-in-out infinite alternate; }
      #timer-label {
        font-family: 'Crimson Text', serif;
        font-style: italic;
        font-size: 0.9rem;
        color: #A0624A;
        margin-top: 2px;
      }

      /* ---- CARE cloud ---- */
      .care-cloud {
        position: fixed;
        cursor: pointer;
        z-index: 501;
        user-select: none;
        animation: float 2s ease-in-out infinite alternate;
        filter: drop-shadow(0 4px 16px rgba(196,102,58,0.35));
      }
      .care-cloud svg { display: block; }
      .care-cloud .cloud-label {
        position: absolute; inset: 0;
        display: flex; align-items: center; justify-content: center;
        font-family: 'Playfair Display', serif;
        font-weight: 900;
        font-size: 1.5rem;
        color: #6B3A2A;
        letter-spacing: 0.08em;
      }
      @keyframes float { from{transform:translateY(0)} to{transform:translateY(-8px)} }

      /* ---- Pause overlay ---- */
      #pause-overlay {
        display: none;
        position: fixed; inset: 0; z-index: 9999;
        background: rgba(253,243,231,0.96);
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        text-align: center;
      }
      #pause-overlay.visible { display: flex; }

      .pause-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        animation: pulse 1.2s ease-in-out infinite alternate;
      }

      .resilience-title {
        font-family: 'Playfair Display', serif;
        font-weight: 900;
        font-size: 1.9rem;
        color: #6B3A2A;
        margin-bottom: 1.2rem;
        opacity: 0;
        animation: fadeIn 0.6s 0.2s forwards;
      }

      .message {
        font-family: 'Crimson Text', serif;
        font-size: 1.15rem;
        color: #8B4A30;
        line-height: 1.65;
        max-width: 520px;
        margin-bottom: 0.8rem;
        opacity: 0;
      }
      .message.italic { font-style: italic; font-size: 1.25rem; color: #C4663A; }
      .message.show { animation: fadeIn 0.7s forwards; }

      #resume-btn {
        margin-top: 1.4rem;
        padding: 0.7rem 2.2rem;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 1rem;
        background: linear-gradient(135deg, #C4663A, #E07B50);
        color: white;
        border: none;
        border-radius: 40px;
        cursor: pointer;
        box-shadow: 0 4px 16px rgba(196,102,58,0.35);
        opacity: 0;
        transition: transform 0.15s, box-shadow 0.15s;
      }
      #resume-btn:hover { transform: scale(1.04); box-shadow: 0 6px 20px rgba(196,102,58,0.45); }
      #resume-btn.show { animation: fadeIn 0.7s forwards; }

      @keyframes fadeIn { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
    </style>

    <h1>Solve this Sudoku</h1>
    <p class="subtitle">Make sure to click on every task that appears as well!</p>

    <div id="timer-wrap">
      <div id="timer-display">2:00</div>
      <div id="timer-label">Time remaining</div>
    </div>

    <div id="sudoku"></div>
    <div id="coach-hint" style="display:none;"></div>

    <!-- Pause overlay -->
    <div id="pause-overlay">
      <div class="resilience-title" id="overlay-title"></div>
      <div id="overlay-messages"></div>
      <button id="resume-btn">▶ Continue</button>
    </div>

    <script>
      // =============================================
      // COUNTDOWN TIMER
      // =============================================
      let timerSeconds = 120;
      let timerPaused  = false;

      function updateTimerDisplay() {
        const m = Math.floor(timerSeconds / 60);
        const s = timerSeconds % 60;
        const display = document.getElementById('timer-display');
        display.textContent = m + ':' + s.toString().padStart(2, '0');
        display.classList.remove('warning', 'urgent');
        if (timerSeconds <= 15)       display.classList.add('urgent');
        else if (timerSeconds <= 30)  display.classList.add('warning');
      }

      setInterval(() => {
        if (timerPaused || timerSeconds <= 0) return;
        timerSeconds--;
        updateTimerDisplay();
      }, 1000);

      // =============================================
      // SUDOKU
      // =============================================
      const puzzle = [
        [5,3,0, 0,7,0, 0,0,0],
        [6,0,0, 1,9,5, 0,0,0],
        [0,9,8, 0,0,0, 0,6,0],

        [8,0,0, 0,6,0, 0,0,3],
        [4,0,0, 8,0,3, 0,0,1],
        [7,0,0, 0,2,0, 0,0,6],

        [0,6,0, 0,0,0, 2,8,0],
        [0,0,0, 4,1,9, 0,0,5],
        [0,0,0, 0,8,0, 0,7,9]
      ];
      const solution = [
        [5,3,4, 6,7,8, 9,1,2],
        [6,7,2, 1,9,5, 3,4,8],
        [1,9,8, 3,4,2, 5,6,7],

        [8,5,9, 7,6,1, 4,2,3],
        [4,2,6, 8,5,3, 7,9,1],
        [7,1,3, 9,2,4, 8,5,6],

        [9,6,1, 5,3,7, 2,8,4],
        [2,8,7, 4,1,9, 6,3,5],
        [3,4,5, 2,8,6, 1,7,9]
      ];

      const grid = document.getElementById('sudoku');
      for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
          const cell = document.createElement('div');
          cell.className = 'cell';
          cell.dataset.row = r;
          cell.dataset.col = c;
          const val = puzzle[r][c];
          if (val !== 0) {
            cell.textContent = val;
          } else {
            cell.classList.add('empty');
            const inp = document.createElement('input');
            inp.type = 'text'; inp.maxLength = 1;
            inp.addEventListener('keydown', e => {
              if (!'123456789Backspace'.includes(e.key)) e.preventDefault();
            });
            inp.addEventListener('input', () => {
              const v = inp.value.replace(/[^1-9]/g,'');
              inp.value = v ? v[v.length-1] : '';
              if (!inp.value) { cell.classList.remove('correct','wrong'); }
              else {
                const correct = parseInt(inp.value) === solution[r][c];
                cell.classList.toggle('correct', correct);
                cell.classList.toggle('wrong',   !correct);
                if (correct) {
                  // After flash, convert to a fixed-looking cell
                  setTimeout(() => {
                    cell.classList.remove('correct', 'empty');
                    cell.classList.add('fixed');
                    const span = document.createElement('span');
                    span.textContent = inp.value;
                    cell.replaceChild(span, inp);
                  }, 600);
                }
              }
              // Recalculate coaching hint after every input
              if (coachingActive) {
                clearTimeout(coachHintTimeout);
                showNextHint();
              }
            });
            cell.appendChild(inp);
          }
          grid.appendChild(cell);
        }
      }

      // =============================================
      // FLOATING ICONS + CARE CLOUD
      // =============================================
      const ICONS = ["🔔","💊","🛏️","🩺","💉","🧪","📋","🧹","🧴","🩹"];
      const EXPIRE_MS = 5000;
      const SAD_MS    = 2000;

      // 3 CARE clouds: R first, then A (icons stop after), then C
      const careData = [
        {
          title: 'R — Resilience Training',
          msgs: [
            { id:'m1', text:'Take a deep breath. 🌿', italic:true },
            { id:'m2', text:'Every puzzle has a solution — just like every challenge in healthcare.' },
            { id:'m3', text:'You are capable of more than you think. 💛', italic:true },
            { id:'m4', text:'Stress narrows your focus. A moment of stillness opens it back up.' },
            { id:'m5', text:'Resilience is not about going faster — it is about going smarter.', italic:true },
            { id:'m6', text:'Just like in nursing: structured pauses and self-compassion make you stronger, not weaker.' },
            { id:'m7', text:'You do not need to solve everything at once. 🌱', italic:true }
          ]
        },
        {
          title: 'A — Adaptation Support',
          msgs: [
            { id:'m1', text:'Adapting to a new role takes time — and that is perfectly normal.', italic:true },
            { id:'m2', text:'You are not expected to know everything from day one.' },
            { id:'m3', text:'Support is not a sign of weakness. It is how we grow together. 💛', italic:true },
            { id:'m4', text:'Lean on your team. Ask questions. Adapt at your own pace.' },
            { id:'m5', text:'Every small step forward counts. 🌱', italic:true }
          ]
        },
        {
          title: 'C — Coaching',
          msgs: [
            { id:'m1', text:'A good coach can change everything. 🤝', italic:true },
            { id:'m2', text:'Coaching is not about fixing what is broken — it is about unlocking what is possible.' },
            { id:'m3', text:'Share what you need. Your supervisor is there to support you. 💛', italic:true },
            { id:'m4', text:'You grow faster when you learn alongside someone who guides you.' },
            { id:'m5', text:'Asking for help is not a step back. It is a step forward. 🌱', italic:true }
          ]
        }
      ];

      let careIndex   = 0;
      let iconsActive = true;
      let paused      = false;
      let nextSpawnId = null;
      let nextCareId  = null;

      // Track active icons for pause/resume
      const activeIcons = new Map();

      function scheduleNext() {
        const delay = (4 + Math.random() * 3) * 1000;
        nextSpawnId = setTimeout(doSpawn, delay);
      }

      function doSpawn() {
        if (paused || !iconsActive) return;
        spawnIcon();
        scheduleNext();
      }

      function randomPos() {
        const margin = 65;
        const W = document.documentElement.clientWidth  || window.innerWidth;
        const H = document.documentElement.clientHeight || window.innerHeight;
        return {
          x: margin + Math.random() * (W - margin * 2),
          y: margin + Math.random() * (H - margin * 2)
        };
      }

      function spawnIcon() {
        const icon = ICONS[Math.floor(Math.random() * ICONS.length)];
        const el = document.createElement('div');
        el.className = 'task-icon';
        el.textContent = icon;
        const {x, y} = randomPos();
        el.style.left = x + 'px'; el.style.top = y + 'px';
        document.body.appendChild(el);

        const t1   = setTimeout(() => el.classList.add('warn'),   3000);
        const t2   = setTimeout(() => el.classList.add('urgent'), 4200);
        const tExp = setTimeout(() => expireIcon(el),             EXPIRE_MS);
        activeIcons.set(el, {t1, t2, tExp, startedAt: Date.now(), duration: EXPIRE_MS});

        el.addEventListener('click', () => {
          if (paused) return;
          const entry = activeIcons.get(el);
          if (entry) { clearTimeout(entry.t1); clearTimeout(entry.t2); clearTimeout(entry.tExp); }
          activeIcons.delete(el);
          el.classList.add('clicked');
          setTimeout(() => el.remove(), 300);
        });
      }

      function expireIcon(el) {
        activeIcons.delete(el);
        const sad = document.createElement('div');
        sad.className = 'sad-icon';
        sad.textContent = '😢';
        sad.style.left = el.style.left; sad.style.top = el.style.top;
        document.body.appendChild(sad);
        el.remove();
        setTimeout(() => sad.remove(), SAD_MS);
      }

      function clearAllIcons() {
        activeIcons.forEach((entry, el) => {
          clearTimeout(entry.t1); clearTimeout(entry.t2); clearTimeout(entry.tExp);
          el.classList.add('clicked');
          setTimeout(() => el.remove(), 300);
        });
        activeIcons.clear();
      }

      function spawnCareCloud() {
        if (careIndex >= careData.length) return;
        const sudokuEl = document.getElementById('sudoku');
        const rect = sudokuEl.getBoundingClientRect();
        const cloudW = 120, cloudH = 80;
        const x = rect.left + Math.random() * (rect.width  - cloudW);
        const y = rect.top  + Math.random() * (rect.height - cloudH);
        const wrapper = document.createElement('div');
        wrapper.className = 'care-cloud';
        wrapper.style.left = x + 'px'; wrapper.style.top = y + 'px';
        wrapper.innerHTML = '<svg width="120" height="80" viewBox="0 0 120 80" xmlns="http://www.w3.org/2000/svg"><path d="M100,55 Q115,55 115,42 Q115,30 103,30 Q101,18 90,18 Q84,10 74,12 Q66,4 54,8 Q42,4 36,14 Q24,14 22,26 Q12,28 12,40 Q12,55 28,55 Z" fill="#FDE8D0" stroke="#E07B50" stroke-width="2.5"/></svg><div class="cloud-label">CARE</div>';
        document.body.appendChild(wrapper);

        wrapper.addEventListener('click', () => {
          wrapper.remove();
          pauseGame();
        });
      }

      // =============================================
      // PAUSE / RESUME
      // =============================================
      function pauseGame() {
        paused = true;
        timerPaused = true;
        clearTimeout(nextSpawnId);
        clearTimeout(nextCareId);

        // Freeze all active icons
        activeIcons.forEach((entry, el) => {
          clearTimeout(entry.t1); clearTimeout(entry.t2); clearTimeout(entry.tExp);
          entry.remaining = entry.duration - (Date.now() - entry.startedAt);
          el.style.animationPlayState = 'paused';
        });

        // Fill overlay with content for current care index
        const data = careData[careIndex];
        document.getElementById('overlay-title').textContent = data.title;
        const msgContainer = document.getElementById('overlay-messages');
        msgContainer.innerHTML = '';
        const btn = document.getElementById('resume-btn');
        btn.classList.remove('show');

        const delays = [0.3, 1.0, 1.8, 2.6, 3.4, 4.2, 5.0];
        data.msgs.forEach((m, i) => {
          const div = document.createElement('div');
          div.className = 'message' + (m.italic ? ' italic' : '');
          div.textContent = m.text;
          msgContainer.appendChild(div);
          setTimeout(() => div.classList.add('show'), delays[i] * 1000);
        });
        setTimeout(() => btn.classList.add('show'), delays[data.msgs.length] * 1000);

        document.getElementById('pause-overlay').classList.add('visible');
      }

      document.getElementById('resume-btn').addEventListener('click', resumeGame);

      function resumeGame() {
        paused = false;
        timerPaused = false;
        document.getElementById('pause-overlay').classList.remove('visible');

        if (careIndex === 1) {
          // After cloud A: clear all icons and stop spawning
          clearAllIcons();
          iconsActive = false;
          careIndex++;
          // Schedule cloud C after 15s
          nextCareId = setTimeout(spawnCareCloud, 15000);
        } else if (careIndex === 2) {
          // After cloud C: start coaching mode
          careIndex++;
          startCoaching();
        } else {
          // After cloud R: resume icons, schedule next cloud
          activeIcons.forEach((entry, el) => {
            el.style.animationPlayState = '';
            const remaining = Math.max(entry.remaining || 1000, 500);
            entry.tExp = setTimeout(() => expireIcon(el), remaining);
          });
          careIndex++;
          if (careIndex < careData.length) {
            nextCareId = setTimeout(spawnCareCloud, 15000);
          }
          scheduleNext();
        }
      }

      // =============================================
      // COACHING: highlight by number
      // =============================================
      let coachingActive = false;
      let coachHintTimeout = null;

      function startCoaching() {
        coachingActive = true;
        showNextHint();
      }

      function getCurrentBoard() {
        const board = puzzle.map(row => [...row]);
        // Read user inputs
        document.querySelectorAll('.cell.empty input').forEach(inp => {
          const cell = inp.parentElement;
          const r = parseInt(cell.dataset.row);
          const c = parseInt(cell.dataset.col);
          const v = parseInt(inp.value);
          if (v >= 1 && v <= 9) board[r][c] = v;
        });
        // Read correctly solved cells (converted to fixed spans)
        document.querySelectorAll('.cell.fixed span').forEach(span => {
          const cell = span.parentElement;
          const r = parseInt(cell.dataset.row);
          const c = parseInt(cell.dataset.col);
          const v = parseInt(span.textContent);
          if (v >= 1 && v <= 9) board[r][c] = v;
        });
        return board;
      }

      function getPossibles(board, r, c) {
        if (board[r][c] !== 0) return [];
        const used = new Set();
        for (let i = 0; i < 9; i++) {
          used.add(board[r][i]);
          used.add(board[i][c]);
        }
        const br = Math.floor(r/3)*3, bc = Math.floor(c/3)*3;
        for (let dr = 0; dr < 3; dr++)
          for (let dc = 0; dc < 3; dc++)
            used.add(board[br+dr][bc+dc]);
        return [1,2,3,4,5,6,7,8,9].filter(v => !used.has(v));
      }

      function clearCoachHighlights() {
        document.querySelectorAll('.cell.coach-stripe, .cell.coach-num')
          .forEach(el => el.classList.remove('coach-stripe', 'coach-num'));
        const outline = document.getElementById('coach-box-outline');
        if (outline) outline.remove();
        const hint = document.getElementById('coach-hint');
        hint.style.display = 'none';
        hint.textContent = '';
      }

      // Only hint when row/col elimination leaves exactly 1 candidate in the box
      function findBoxOnlyHints(board) {
        const hints = [];
        for (let boxR = 0; boxR < 9; boxR += 3) {
          for (let boxC = 0; boxC < 9; boxC += 3) {
            for (let num = 1; num <= 9; num++) {
              // Skip if num already placed in this box
              let inBox = false;
              for (let dr = 0; dr < 3; dr++)
                for (let dc = 0; dc < 3; dc++)
                  if (board[boxR+dr][boxC+dc] === num) inBox = true;
              if (inBox) continue;

              // Find empty cells in this box where num is still possible
              const candidates = [];
              for (let dr = 0; dr < 3; dr++) {
                for (let dc = 0; dc < 3; dc++) {
                  const r = boxR+dr, c = boxC+dc;
                  if (board[r][c] === 0 && getPossibles(board, r, c).includes(num))
                    candidates.push({r, c});
                }
              }
              // Valid hint: exactly one cell left in the box for this number
              if (candidates.length === 1)
                hints.push({r: candidates[0].r, c: candidates[0].c, num});
            }
          }
        }
        return hints;
      }

      function drawBoxOutline(boxR, boxC) {
        const first = document.querySelector('.cell[data-row="'+boxR+'"][data-col="'+boxC+'"]');
        const last  = document.querySelector('.cell[data-row="'+(boxR+2)+'"][data-col="'+(boxC+2)+'"]');
        if (!first || !last) return;
        const fr = first.getBoundingClientRect();
        const lr = last.getBoundingClientRect();
        const div = document.createElement('div');
        div.id = 'coach-box-outline';
        div.style.cssText = 'position:fixed;pointer-events:none;z-index:10;box-sizing:border-box;' +
          'border:3px solid #1a1a1a;' +
          'left:'+fr.left+'px;top:'+fr.top+'px;' +
          'width:'+(lr.right-fr.left)+'px;height:'+(lr.bottom-fr.top)+'px;';
        document.body.appendChild(div);
      }

      function showNextHint() {
        if (!coachingActive) return;
        clearCoachHighlights();
        const board = getCurrentBoard();

        const hints = findBoxOnlyHints(board);
        if (hints.length === 0) { return; } // no clear hints yet

        // Pick the hint for the number that appears most on the board (most visible)
        let best = hints[0], bestCount = 0;
        hints.forEach(h => {
          let count = 0;
          for (let r = 0; r < 9; r++)
            for (let c = 0; c < 9; c++)
              if (board[r][c] === h.num) count++;
          if (count > bestCount) { bestCount = count; best = h; }
        });

        const { r: bestR, c: bestC, num: targetNum } = best;
        const boxR = Math.floor(bestR/3)*3;
        const boxC = Math.floor(bestC/3)*3;

        // Rows and cols containing targetNum
        const usedRows = new Set(), usedCols = new Set();
        for (let r = 0; r < 9; r++)
          for (let c = 0; c < 9; c++)
            if (board[r][c] === targetNum) { usedRows.add(r); usedCols.add(c); }

        document.querySelectorAll('.cell').forEach(cell => {
          const r = parseInt(cell.dataset.row);
          const c = parseInt(cell.dataset.col);
          if (r === bestR && c === bestC) return;
          if (cell.classList.contains('wrong')) return;
          if (board[r][c] === targetNum)                    cell.classList.add('coach-num');
          else if (usedRows.has(r) || usedCols.has(c))     cell.classList.add('coach-stripe');
        });

        drawBoxOutline(boxR, boxC);

        // Show hint text
        const hint = document.getElementById('coach-hint');
        hint.textContent = 'The highlighted rows and columns already contain the number ' + targetNum + '. It is missing from the framed box — find the one spot where it fits!';
        hint.style.display = 'block';

        // Fallback refresh every 10s
        coachHintTimeout = setTimeout(showNextHint, 10000);
      }

      // First icon spawn after 3s, first CARE cloud (R) after 20s
      setTimeout(doSpawn, 3000);
      nextCareId = setTimeout(spawnCareCloud, 20000);
    </script>
    """, height=720, scrolling=False)
