import streamlit as st
import pandas as pd
import random
import time
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AI Cognitive Dependency Experiment",
    layout="wide"
)

# =====================================================
# STYLING
# =====================================================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
    color: white;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
}

.metric-box {
    padding: 20px;
    border-radius: 15px;
    background: #1c1f26;
    margin-bottom: 10px;
}

.big-title {
    font-size: 42px;
    font-weight: 800;
}

.subtitle {
    color: #9ca3af;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "step" not in st.session_state:
    st.session_state.step = 0

if "results" not in st.session_state:
    st.session_state.results = []

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# =====================================================
# QUESTION BANK
# =====================================================

questions = [

    # LOGIC
    {
        "category": "Logic",
        "question": """
A researcher claims:

'All highly intelligent people are good at mathematics.
Some artists are highly intelligent.'

Can we conclude:
'Some artists are good at mathematics'?
""",
        "answer": "yes"
    },

    {
        "category": "Logic",
        "question": """
Five machines take 5 minutes to make 5 products.

How long would 100 machines take to make 100 products?
""",
        "answer": "5"
    },

    # CRITICAL THINKING
    {
        "category": "Critical Thinking",
        "question": """
A news article says:

'People who drink coffee live longer.'

Does this prove coffee causes longer life?
""",
        "answer": "no"
    },

    # AI REASONING
    {
        "category": "AI Verification",
        "question": """
An AI model says:

'Correlation always implies causation.'

Is the statement correct?
""",
        "answer": "no"
    },

    # MATH
    {
        "category": "Mathematics",
        "question": """
A company increases revenue by 20%
then loses 20%.

Is the final revenue equal to the original?
""",
        "answer": "no"
    },

    # SYSTEM THINKING
    {
        "category": "Systems Thinking",
        "question": """
An AI assistant answers 95% correctly,
but the remaining 5% are dangerous errors.

Should humans always verify critical outputs?
""",
        "answer": "yes"
    },

    # COGNITIVE REFLECTION
    {
        "category": "Cognitive Reflection",
        "question": """
If it takes 10 workers 10 days to build a wall,
how many days would 5 workers need?
""",
        "answer": "20"
    },

    # STATISTICS
    {
        "category": "Statistics",
        "question": """
A medical test is 99% accurate.

A disease affects 1 in 1000 people.

Can a positive test still be false?
""",
        "answer": "yes"
    }
]

random.shuffle(questions)

# =====================================================
# INTRO
# =====================================================

if st.session_state.step == 0:

    st.markdown('<div class="big-title">AI Cognitive Dependency Experiment</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="subtitle">

This experiment evaluates:

- Analytical reasoning
- AI trust calibration
- Critical thinking
- Cognitive dependency
- Confidence vs accuracy

You will complete tasks:
1. Without AI
2. With AI assistance
3. Under misleading AI conditions

</div>
""", unsafe_allow_html=True)

    if st.button("Start Experiment"):
        st.session_state.step = 1
        st.rerun()

# =====================================================
# QUESTION ENGINE
# =====================================================

elif st.session_state.step in [1, 2, 3]:

    q = questions[st.session_state.question_index]

    stage_titles = {
        1: "Stage 1 — Independent Reasoning",
        2: "Stage 2 — AI Assisted Reasoning",
        3: "Stage 3 — Misleading AI Environment"
    }

    st.title(stage_titles[st.session_state.step])

    st.markdown(f"### Category: `{q['category']}`")

    st.info(q["question"])

    # -------------------------
    # AI PANEL
    # -------------------------

    if st.session_state.step == 2:

        if st.button("Consult AI"):

            ai_responses = [
                "Consider hidden assumptions carefully.",
                "Break the problem into smaller logical steps.",
                "Verify whether correlation implies causation.",
                "Check whether percentages are symmetric."
            ]

            st.success(random.choice(ai_responses))

    elif st.session_state.step == 3:

        if st.button("Consult AI"):

            misleading = [
                "Yes, correlation always implies causation.",
                "A 20% increase and 20% decrease cancel each other.",
                "Positive medical tests are always reliable.",
                "Humans should fully trust highly accurate AI."
            ]

            st.error(random.choice(misleading))

    # -------------------------
    # ANSWER
    # -------------------------

    answer = st.text_input("Your answer")

    confidence = st.slider(
        "How confident are you?",
        1,
        10,
        5
    )

    # -------------------------
    # SUBMIT
    # -------------------------

    if st.button("Submit Answer"):

        elapsed = round(time.time() - st.session_state.start_time, 2)

        correct = answer.strip().lower() == q["answer"]

        st.session_state.results.append({
            "stage": st.session_state.step,
            "category": q["category"],
            "correct": int(correct),
            "confidence": confidence,
            "time_sec": elapsed,
            "used_ai": int(st.session_state.step != 1)
        })

        st.session_state.question_index += 1
        st.session_state.start_time = time.time()

        # NEXT STAGE
        if st.session_state.question_index >= 2:

            st.session_state.question_index = 0
            st.session_state.step += 1

        # FINISH
        if st.session_state.step >= 4:
            st.session_state.step = 4

        st.rerun()

# =====================================================
# RESULTS
# =====================================================

elif st.session_state.step == 4:

    st.title("Experiment Results")

    df = pd.DataFrame(st.session_state.results)

    st.dataframe(df, use_container_width=True)

    # =================================================
    # METRICS
    # =================================================

    accuracy = df["correct"].mean() * 100
    avg_confidence = df["confidence"].mean()
    avg_time = df["time_sec"].mean()

    # Cognitive dependency
    stage1 = df[df["stage"] == 1]["correct"].mean()
    stage3 = df[df["stage"] == 3]["correct"].mean()

    dependency = max(0, (stage1 - stage3) * 100)

    # =================================================
    # DASHBOARD
    # =================================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Accuracy", f"{accuracy:.1f}%")

    with col2:
        st.metric("Avg Confidence", f"{avg_confidence:.1f}/10")

    with col3:
        st.metric("Avg Response Time", f"{avg_time:.1f}s")

    st.metric("Cognitive Dependency Risk", f"{dependency:.1f}%")

    # =================================================
    # CHARTS
    # =================================================

    stage_acc = df.groupby("stage")["correct"].mean()

    fig, ax = plt.subplots()

    ax.plot(stage_acc.index, stage_acc.values, marker="o")

    ax.set_xlabel("Stage")
    ax.set_ylabel("Accuracy")
    ax.set_title("Accuracy Across Experimental Stages")

    st.pyplot(fig)

    # =================================================
    # INTERPRETATION
    # =================================================

    st.subheader("Interpretation")

    if dependency > 30:
        st.error("""
High cognitive dependency detected.

Performance dropped significantly under misleading AI conditions.
""")

    elif dependency > 10:
        st.warning("""
Moderate dependency detected.

Some evidence of AI over-reliance.
""")

    else:
        st.success("""
Low dependency detected.

Participant maintained independent reasoning.
""")

    # =================================================
    # EXPORT
    # =================================================

    csv = df.to_csv(index=False)

    st.download_button(
        "Download Results CSV",
        csv,
        "experiment_results.csv",
        "text/csv"
    )
