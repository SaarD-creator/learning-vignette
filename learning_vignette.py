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
    st.button(
        "🎯 Try it out!",
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
        display: flex; flex-direction: column; align-items: center;
        padding: 18px 16px 30px; font-family: 'Crimson Text', serif;
        min-height: 100vh; overflow: hidden;
      }
      h1 { font-family:'Playfair Display',serif; font-weight:900; font-size:2rem; color:#6B3A2A; text-align:center; margin-bottom:4px; }
      .subtitle { font-family:'Crimson Text',serif; font-style:italic; font-size:1rem; color:#A0624A; text-align:center; margin-bottom:18px; }

      #game-row { display:flex; flex-direction:row; align-items:flex-start; gap:24px; justify-content:center; }

      #sudoku {
        display:grid; grid-template-columns:repeat(9,50px); grid-template-rows:repeat(9,50px);
        border:3px solid #8B3A20; background:#C4866A; gap:1px;
        box-shadow:0 8px 32px rgba(100,40,20,0.18); border-radius:6px; overflow:hidden; flex-shrink:0;
      }
      .cell {
        width:50px; height:50px; background:#FDF6EC;
        display:flex; align-items:center; justify-content:center;
        font-size:1.35rem; font-family:'Playfair Display',serif; font-weight:700; color:#4A2510; transition:background 0.3s;
      }
      .cell[data-col="3"],.cell[data-col="6"] { border-left:2.5px solid #8B3A20; }
      .cell[data-row="3"],.cell[data-row="6"] { border-top:2.5px solid #8B3A20; }
      .cell.empty input {
        width:100%; height:100%; border:none; background:transparent; text-align:center;
        font-size:1.35rem; font-family:'Playfair Display',serif; font-weight:700; color:#C4663A; outline:none;
      }
      .cell.correct { background:#C8F0D0; animation:flashGreen 0.5s ease; }
      .cell.wrong   { background:#FFD0CC; }
      .cell.hint-active { background:#FFF8DC !important; animation:hintPulse 0.8s ease-in-out infinite alternate !important; }
      .cell.hint-active input { color:#8B6000; }
      @keyframes flashGreen { 0%{background:#7BE89A} 100%{background:#C8F0D0} }
      @keyframes hintPulse {
        from { box-shadow:inset 0 0 0 3px #D4A010, 0 0 10px rgba(212,160,16,0.5); }
        to   { box-shadow:inset 0 0 0 3px #D4A010, 0 0 22px rgba(212,160,16,0.9); }
      }

      #help-panel {
        display:none; flex-direction:column; align-items:center;
        background:linear-gradient(160deg,#FDF0E4,#FAE4CC); border:2px solid #E0A070;
        border-radius:18px; padding:1.4rem 1.2rem; width:172px;
        box-shadow:0 6px 24px rgba(180,80,40,0.13); animation:slideIn 0.5s ease;
      }
      #help-panel.visible { display:flex; }
      @keyframes slideIn { from{opacity:0;transform:translateX(20px)} to{opacity:1;transform:translateX(0)} }
      .help-title { font-family:'Playfair Display',serif; font-weight:900; font-size:1.1rem; color:#6B3A2A; margin-bottom:0.5rem; text-align:center; }
      .help-sub   { font-family:'Crimson Text',serif; font-style:italic; font-size:0.88rem; color:#A06040; text-align:center; margin-bottom:1rem; line-height:1.4; }
      #hint-btn {
        padding:0.55rem 1.1rem; width:100%;
        font-family:'Playfair Display',serif; font-weight:700; font-size:0.95rem;
        background:linear-gradient(135deg,#C4663A,#E07B50); color:white; border:none;
        border-radius:30px; cursor:pointer; box-shadow:0 3px 12px rgba(196,102,58,0.35);
        transition:transform 0.15s; margin-bottom:1rem;
      }
      #hint-btn:hover { transform:scale(1.05); }
      #hint-display {
        font-family:'Crimson Text',serif; font-size:1rem; color:#6B3A2A; text-align:center;
        line-height:1.5; min-height:52px; margin-bottom:1.1rem; font-style:italic;
      }
      #hint-display strong { font-style:normal; font-size:1.6rem; color:#8B5E00; display:block; }
      #timer { font-family:'Playfair Display',serif; font-weight:900; font-size:2.4rem; color:#6B3A2A; line-height:1; }
      #timer.warn   { color:#C47A2A; }
      #timer.urgent { color:#C43A2A; animation:timerPulse 0.4s ease-in-out infinite alternate; }
      @keyframes timerPulse { from{transform:scale(1)} to{transform:scale(1.08)} }
      #timer-label { font-family:'Crimson Text',serif; font-style:italic; font-size:0.8rem; color:#A06040; margin-top:4px; text-align:center; }
      #timer-done  { font-family:'Crimson Text',serif; font-style:italic; font-size:0.9rem; color:#6B3A2A; text-align:center; margin-top:6px; display:none; }

      .task-icon {
        position:fixed; font-size:2.8rem; cursor:pointer; z-index:500;
        animation:pulse 0.8s ease-in-out infinite alternate;
        filter:drop-shadow(0 0 8px rgba(196,102,58,0.7));
        user-select:none; background:rgba(255,255,255,0.88); border-radius:50%; padding:4px; line-height:1;
      }
      .task-icon:hover  { transform:scale(1.15); }
      .task-icon.warn   { filter:drop-shadow(0 0 10px rgba(220,140,0,0.9));  animation:pulse-warn 0.5s ease-in-out infinite alternate; }
      .task-icon.urgent { filter:drop-shadow(0 0 13px rgba(200,30,30,0.95)); animation:pulse-urgent 0.22s ease-in-out infinite alternate; }
      .task-icon.clicked { transform:scale(0); opacity:0; transition:transform 0.22s,opacity 0.22s; }
      .sad-icon { position:fixed; font-size:2.8rem; z-index:500; animation:fadeout 2s forwards; user-select:none; line-height:1; }
      @keyframes pulse        { from{transform:scale(1)}    to{transform:scale(1.1)}  }
      @keyframes pulse-warn   { from{transform:scale(1)}    to{transform:scale(1.15)} }
      @keyframes pulse-urgent { from{transform:scale(0.95)} to{transform:scale(1.2)}  }
      @keyframes fadeout      { 0%{opacity:1} 60%{opacity:1} 100%{opacity:0;transform:scale(0.6)} }

      .care-cloud {
        position:fixed; cursor:pointer; z-index:501; user-select:none;
        animation:float 2s ease-in-out infinite alternate;
        filter:drop-shadow(0 4px 16px rgba(196,102,58,0.35));
      }
      .care-cloud .cloud-label {
        position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
        font-family:'Playfair Display',serif; font-weight:900; font-size:1.5rem; color:#6B3A2A; letter-spacing:0.08em;
      }
      @keyframes float { from{transform:translateY(0)} to{transform:translateY(-8px)} }

      #pause-overlay {
        display:none; position:fixed; inset:0; z-index:9999;
        background:rgba(253,243,231,0.97); flex-direction:column; align-items:center; justify-content:center;
        padding:2rem; text-align:center;
      }
      #pause-overlay.visible { display:flex; }
      .overlay-section { display:none; flex-direction:column; align-items:center; }
      .overlay-section.active { display:flex; }
      .overlay-title { font-family:'Playfair Display',serif; font-weight:900; font-size:1.9rem; color:#6B3A2A; margin-bottom:1.2rem; opacity:0; animation:fadeIn 0.6s 0.2s forwards; }
      .message { font-family:'Crimson Text',serif; font-size:1.15rem; color:#8B4A30; line-height:1.65; max-width:540px; margin-bottom:0.8rem; opacity:0; }
      .message.italic { font-style:italic; font-size:1.22rem; color:#C4663A; }
      .message.show { animation:fadeIn 0.7s forwards; }
      .resume-btn {
        margin-top:1.4rem; padding:0.7rem 2.2rem;
        font-family:'Playfair Display',serif; font-weight:700; font-size:1rem;
        background:linear-gradient(135deg,#C4663A,#E07B50); color:white; border:none;
        border-radius:40px; cursor:pointer; box-shadow:0 4px 16px rgba(196,102,58,0.35); opacity:0;
        transition:transform 0.15s;
      }
      .resume-btn:hover { transform:scale(1.04); }
      .resume-btn.show { animation:fadeIn 0.7s forwards; }
      @keyframes fadeIn { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
    </style>

    <h1>Solve this Sudoku</h1>
    <p class="subtitle">Make sure to click on every task that appears as well!</p>
    <div id="game-row">
      <div id="sudoku"></div>
      <div id="help-panel">
        <div class="help-title">💡 Coaching</div>
        <div class="help-sub">A good coach shows you where to look — not what to write.</div>
        <button id="hint-btn">Help</button>
        <div id="hint-display"></div>
        <div id="timer">1:00</div>
        <div id="timer-label">remaining</div>
        <div id="timer-done">Take your time. 🌿</div>
      </div>
    </div>

    <div id="pause-overlay">
      <div class="overlay-section" id="section-R">
        <div class="overlay-title">R — Resilience Training</div>
        <div class="message italic" id="r1">Take a deep breath. 🌿</div>
        <div class="message"        id="r2">Every puzzle has a solution — just like every challenge in healthcare.</div>
        <div class="message italic" id="r3">You are capable of more than you think. 💛</div>
        <div class="message"        id="r4">Stress narrows your focus. A moment of stillness opens it back up.</div>
        <div class="message italic" id="r5">Resilience isn't about going faster — it's about going smarter.</div>
        <div class="message"        id="r6">Just like in nursing: structured pauses and self-compassion make you stronger, not weaker.</div>
        <div class="message italic" id="r7">You don't need to solve everything at once. 🌱</div>
        <button class="resume-btn" id="resume-R">▶ Continue</button>
      </div>
      <div class="overlay-section" id="section-A">
        <div class="overlay-title">A — Adaptation Support</div>
        <div class="message"        id="a1">Without a program like CARE, new employees often face everything at once — icons, sudoku, full pressure, from day one.</div>
        <div class="message italic" id="a2">Sound familiar? That's exactly what you just experienced. 🎯</div>
        <div class="message"        id="a3">The CARE start program changes that. Your employer makes a deliberate choice: new employees start at a calmer pace.</div>
        <div class="message italic" id="a4">Step by step, they take on more tasks and responsibilities. But it begins gently — just like it did here. 🌱</div>
        <div class="message"        id="a5">That's why the task icons have now disappeared. Through CARE, your employer has chosen to reduce the pressure — for now.</div>
        <button class="resume-btn" id="resume-A">▶ Continue</button>
      </div>
      <div class="overlay-section" id="section-C">
        <div class="overlay-title">C — Coaching</div>
        <div class="message"        id="c1">In the CARE start program, you are never alone.</div>
        <div class="message italic" id="c2">A coach doesn't solve things for you — they help you find the answer yourself. 💡</div>
        <div class="message"        id="c3">In healthcare, a good mentor makes the difference between feeling lost and feeling capable.</div>
        <div class="message italic" id="c4">From now on, you have a coaching panel next to your sudoku.</div>
        <div class="message"        id="c5">Click <em>Help</em> whenever you're stuck — it will point you in the right direction.</div>
        <button class="resume-btn" id="resume-C">▶ Continue</button>
      </div>
    </div>

    <script>
      const puzzle = [
        [5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]
      ];
      const solution = [
        [5,3,4,6,7,8,9,1,2],[6,7,2,1,9,5,3,4,8],[1,9,8,3,4,2,5,6,7],
        [8,5,9,7,6,1,4,2,3],[4,2,6,8,5,3,7,9,1],[7,1,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],[2,8,7,4,1,9,6,3,5],[3,4,5,2,8,6,1,7,9]
      ];

      const grid = document.getElementById('sudoku');
      let currentHintCell = null;

      for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
          const cell = document.createElement('div');
          cell.className = 'cell'; cell.dataset.row = r; cell.dataset.col = c;
          const val = puzzle[r][c];
          if (val !== 0) {
            cell.textContent = val;
          } else {
            cell.classList.add('empty');
            const inp = document.createElement('input');
            inp.type = 'text'; inp.maxLength = 1;
            inp.addEventListener('keydown', e => { if (!'123456789Backspace'.includes(e.key)) e.preventDefault(); });
            inp.addEventListener('input', () => {
              const v = inp.value.replace(/[^1-9]/g,'');
              inp.value = v ? v[v.length-1] : '';
              if (!inp.value) { cell.classList.remove('correct','wrong'); return; }
              const ok = parseInt(inp.value) === solution[r][c];
              cell.classList.toggle('correct', ok);
              cell.classList.toggle('wrong',  !ok);
              if (ok && cell === currentHintCell) {
                cell.classList.remove('hint-active');
                currentHintCell = null;
                document.getElementById('hint-display').innerHTML = 'Well done! 🎉';
              }
            });
            cell.appendChild(inp);
          }
          grid.appendChild(cell);
        }
      }

      // ---- HINT ----
      document.getElementById('hint-btn').addEventListener('click', () => {
        if (currentHintCell) { currentHintCell.classList.remove('hint-active'); currentHintCell = null; }
        const candidates = [];
        for (let r = 0; r < 9; r++)
          for (let c = 0; c < 9; c++)
            if (puzzle[r][c] === 0) {
              const cell = grid.querySelector(`[data-row="${r}"][data-col="${c}"]`);
              if (!cell.classList.contains('correct')) candidates.push({r,c,cell});
            }
        if (!candidates.length) { document.getElementById('hint-display').innerHTML = 'All cells filled correctly! 🎉'; return; }
        const {r, c, cell} = candidates[Math.floor(Math.random() * candidates.length)];
        cell.classList.add('hint-active');
        currentHintCell = cell;
        document.getElementById('hint-display').innerHTML =
          'Fill in<strong>' + solution[r][c] + '</strong>in the glowing cell ✨';
      });

      // ---- TIMER ----
      let timerInterval = null;
      function startTimer(seconds) {
        const timerEl = document.getElementById('timer');
        const doneEl  = document.getElementById('timer-done');
        let remaining = seconds;
        function tick() {
          const m = Math.floor(remaining/60), s = remaining%60;
          timerEl.textContent = m+':'+String(s).padStart(2,'0');
          timerEl.className = remaining<=10 ? 'urgent' : remaining<=30 ? 'warn' : '';
          if (remaining-- <= 0) {
            clearInterval(timerInterval);
            timerEl.style.display='none';
            document.getElementById('timer-label').style.display='none';
            doneEl.style.display='block';
          }
        }
        tick(); timerInterval = setInterval(tick, 1000);
      }

      // ---- ICONS + CARE CLOUDS ----
      const ICONS=['🔔','💊','🛏️','🩺','💉','🧪','📋','🧹','🧴','🩹'];
      const EXPIRE_MS=5000, SAD_MS=2000;
      let paused=false, careCount=0, iconsDisabled=false, spawningStopped=false;
      let nextSpawnId=null, resumeTime=null;
      const gameStart=Date.now();
      const activeIcons=new Map();

      function scheduleNext(delay) {
        if (spawningStopped) return;
        nextSpawnId = setTimeout(doSpawn, delay!==undefined ? delay : (4+Math.random()*3)*1000);
      }

      function doSpawn() {
        if (paused || spawningStopped) return;
        const now=Date.now(), sinceStart=now-gameStart, sinceResume=resumeTime?now-resumeTime:Infinity;
        const shouldCare =
          (careCount===0 && sinceStart>=20000) ||
          (careCount===1 && sinceResume>=15000) ||
          (careCount===2 && sinceResume>=15000);
        if (shouldCare) {
          spawnCareCloud();
          // no scheduleNext here — resumes after continue is clicked
        } else if (!iconsDisabled) {
          spawnIcon(); scheduleNext();
        } else {
          scheduleNext(2000); // keep polling for next CARE cloud
        }
      }

      function randomPos() {
        const m=65;
        return { x:m+Math.random()*(window.innerWidth-m*2), y:m+Math.random()*(window.innerHeight-m*2) };
      }

      function spawnIcon() {
        if (iconsDisabled||spawningStopped) return;
        const el=document.createElement('div');
        el.className='task-icon'; el.textContent=ICONS[Math.floor(Math.random()*ICONS.length)];
        const {x,y}=randomPos(); el.style.left=x+'px'; el.style.top=y+'px';
        document.body.appendChild(el);
        const t1=setTimeout(()=>el.classList.add('warn'),3000);
        const t2=setTimeout(()=>el.classList.add('urgent'),4200);
        const tExp=setTimeout(()=>expireIcon(el),EXPIRE_MS);
        activeIcons.set(el,{t1,t2,tExp,startedAt:Date.now(),duration:EXPIRE_MS});
        el.addEventListener('click',()=>{
          if(paused)return;
          const e=activeIcons.get(el);
          if(e){clearTimeout(e.t1);clearTimeout(e.t2);clearTimeout(e.tExp);}
          activeIcons.delete(el); el.classList.add('clicked'); setTimeout(()=>el.remove(),300);
        });
      }

      function expireIcon(el) {
        activeIcons.delete(el);
        const sad=document.createElement('div'); sad.className='sad-icon'; sad.textContent='😢';
        sad.style.left=el.style.left; sad.style.top=el.style.top;
        document.body.appendChild(sad); el.remove(); setTimeout(()=>sad.remove(),SAD_MS);
      }

      function spawnCareCloud() {
        const {x,y}=randomPos();
        const w=document.createElement('div'); w.className='care-cloud';
        w.style.left=x+'px'; w.style.top=y+'px';
        w.innerHTML='<svg width="120" height="80" viewBox="0 0 120 80" xmlns="http://www.w3.org/2000/svg"><path d="M100,55 Q115,55 115,42 Q115,30 103,30 Q101,18 90,18 Q84,10 74,12 Q66,4 54,8 Q42,4 36,14 Q24,14 22,26 Q12,28 12,40 Q12,55 28,55 Z" fill="#FDE8D0" stroke="#E07B50" stroke-width="2.5"/></svg><div class="cloud-label">CARE</div>';
        document.body.appendChild(w);
        w.addEventListener('click',()=>{w.remove();pauseGame();});
      }

      function pauseGame() {
        paused=true; clearTimeout(nextSpawnId);
        activeIcons.forEach((entry,el)=>{
          clearTimeout(entry.t1);clearTimeout(entry.t2);clearTimeout(entry.tExp);
          entry.remaining=entry.duration-(Date.now()-entry.startedAt);
          el.style.animationPlayState='paused';
        });
        careCount++;
        const sMap={1:'section-R',2:'section-A',3:'section-C'};
        const pMap={1:'r',2:'a',3:'c'}, nMap={1:7,2:5,3:5}, bMap={1:'resume-R',2:'resume-A',3:'resume-C'};
        document.querySelectorAll('.overlay-section').forEach(s=>s.classList.remove('active'));
        document.getElementById(sMap[careCount]).classList.add('active');
        document.querySelectorAll('.message,.resume-btn').forEach(el=>{el.classList.remove('show');el.style.opacity='0';});
        document.getElementById('pause-overlay').classList.add('visible');
        const pfx=pMap[careCount], n=nMap[careCount];
        for(let i=1;i<=n;i++){const el=document.getElementById(pfx+i);if(el)setTimeout(()=>el.classList.add('show'),i*900);}
        setTimeout(()=>document.getElementById(bMap[careCount]).classList.add('show'),(n+1)*900);
      }

      function unfreezeIcons() {
        activeIcons.forEach((entry,el)=>{
          el.style.animationPlayState='';
          const rem=Math.max(entry.remaining||1000,500);
          entry.tExp=setTimeout(()=>expireIcon(el),rem);
        });
      }

      document.getElementById('resume-R').addEventListener('click',()=>{
        document.getElementById('pause-overlay').classList.remove('visible');
        paused=false; resumeTime=Date.now(); unfreezeIcons(); scheduleNext(2000);
      });

      document.getElementById('resume-A').addEventListener('click',()=>{
        document.getElementById('pause-overlay').classList.remove('visible');
        paused=false; iconsDisabled=true; resumeTime=Date.now();
        activeIcons.forEach((entry,el)=>{clearTimeout(entry.t1);clearTimeout(entry.t2);clearTimeout(entry.tExp);el.remove();});
        activeIcons.clear(); clearTimeout(nextSpawnId);
        scheduleNext(2000); // keep polling — C cloud will come after 15s
      });

      document.getElementById('resume-C').addEventListener('click',()=>{
        document.getElementById('pause-overlay').classList.remove('visible');
        paused=false; spawningStopped=true; clearTimeout(nextSpawnId);
        document.getElementById('help-panel').classList.add('visible');
        startTimer(60);
      });

      setTimeout(doSpawn, 3000);
    </script>
    """, height=660, scrolling=False)
