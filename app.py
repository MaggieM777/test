import streamlit as st
import pandas as pd
import random
import time
import matplotlib.pyplot as plt

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Cognitive Dependency Experiment",
    page_icon="🧠",
    layout="wide"
)

# =====================================================
# CUSTOM STYLING
# =====================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main layout */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Typography */

.big-title {
    font-size: 48px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 10px;
}

.subtitle {
    color: #4B5563;
    font-size: 18px;
    line-height: 1.7;
    margin-bottom: 30px;
}

/* Cards */

.card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #E5E7EB;
    margin-bottom: 20px;
}

/* Question Box */

.question-box {
    background: #F9FAFB;
    padding: 30px;
    border-radius: 18px;
    border-left: 6px solid #2563EB;

    color: #111827;

    font-size: 22px;
    line-height: 1.8;
    font-weight: 500;

    margin-bottom: 20px;
}

.question-box p {
    margin: 0;
}

/* Buttons */

.stButton > button {
    width: 100%;
    height: 3.2em;

    border-radius: 12px;

    border: none;

    background: #2563EB;
    color: white;

    font-size: 16px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #1D4ED8;
}

/* Inputs */

.stTextInput input {
    border-radius: 12px !important;
}

/* Metrics */

[data-testid="metric-container"] {
    background: white;
    border: 1px solid #E5E7EB;
    padding: 15px;
    border-radius: 16px;
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

if "question_sets" not in st.session_state:
    st.session_state.question_sets = {
        1: [],
        2: [],
        3: []
    }

# =====================================================
# QUESTION BANK
# =====================================================

questions = [

    {
        "category": "Logic",
        "difficulty": 2,
        "question": """
All Bloops are Razzies.
All Razzies are Lazzies.

Are all Bloops definitely Lazzies?
""",
        "answer": "yes"
    },

    {
        "category": "Logic",
        "difficulty": 2,
        "question": """
Some Lazzies are Bloops.

Does this mean all Bloops are Lazzies?
""",
        "answer": "no"
    },

    {
        "category": "Logic",
        "difficulty": 1,
        "question": """
If A > B and B > C,
must A > C?
""",
        "answer": "yes"
    },

    {
        "category": "Cognitive Reflection",
        "difficulty": 3,
        "question": """
A bat and a ball cost $1.10 total.

The bat costs $1 more than the ball.

How much does the ball cost?
""",
        "answer": "0.05"
    },

    {
        "category": "Cognitive Reflection",
        "difficulty": 2,
        "question": """
Five machines take 5 minutes to make 5 products.

How long would 100 machines take
to make 100 products?
""",
        "answer": "5"
    },

    {
        "category": "Statistics",
        "difficulty": 3,
        "question": """
A disease affects 1 in 1000 people.

A test is 99% accurate.

Can a positive test still be false?
""",
        "answer": "yes"
    },

    {
        "category": "Statistics",
        "difficulty": 2,
        "question": """
A company increases revenue by 20%
then loses 20%.

Does it return to the original value?
""",
        "answer": "no"
    },

    {
        "category": "Critical Thinking",
        "difficulty": 2,
        "question": """
A headline says:

'Coffee drinkers live longer.'

Does this prove coffee causes longer life?
""",
        "answer": "no"
    },

    {
        "category": "Critical Thinking",
        "difficulty": 3,
        "question": """
An AI system is correct 95% of the time.

Should humans still verify critical decisions?
""",
        "answer": "yes"
    },

    {
        "category": "AI Verification",
        "difficulty": 3,
        "question": """
An AI says:

'Correlation always implies causation.'

Is this scientifically correct?
""",
        "answer": "no"
    },

    {
        "category": "AI Verification",
        "difficulty": 2,
        "question": """
An AI says:

'2% error rate means the system is always safe.'

Is this necessarily true?
""",
        "answer": "no"
    }
]

# =====================================================
# RANDOMIZED STAGES
# =====================================================

if st.session_state.question_sets[1] == []:

    shuffled = questions.copy()
    random.shuffle(shuffled)

    st.session_state.question_sets[1] = shuffled[:4]
    st.session_state.question_sets[2] = shuffled[4:8]
    st.session_state.question_sets[3] = shuffled[0:4]

# =====================================================
# INTRO SCREEN
# =====================================================

if st.session_state.step == 0:

    st.markdown(
        '<div class="big-title">🧠 AI Cognitive Dependency Experiment</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
<div class="subtitle">

This experiment evaluates:

• Analytical reasoning  
• AI trust calibration  
• Cognitive reflection  
• Confidence vs accuracy  
• Susceptibility to misleading AI outputs  

You will complete 3 stages:

1. Independent reasoning  
2. AI-assisted reasoning  
3. Misleading AI environment  

</div>
""", unsafe_allow_html=True)

    st.info("""
This is NOT an IQ test.

The goal is to measure how reasoning changes
when AI systems influence human decisions.
""")

    if st.button("Start Experiment"):

        st.session_state.step = 1
        st.session_state.start_time = time.time()

        st.rerun()

# =====================================================
# QUESTION ENGINE
# =====================================================

elif st.session_state.step in [1, 2, 3]:

    stage_titles = {
        1: "Stage 1 — Independent Reasoning",
        2: "Stage 2 — AI Assisted Reasoning",
        3: "Stage 3 — Misleading AI Environment"
    }

    current_questions = st.session_state.question_sets[
        st.session_state.step
    ]

    q = current_questions[
        st.session_state.question_index
    ]

    st.title(stage_titles[st.session_state.step])

    # =================================================
    # TOP INFO
    # =================================================

    col1, col2 = st.columns([4, 1])

    with col1:

        st.markdown(
            f"""
<div class="card">

<b>Category:</b> {q['category']}<br><br>

<b>Difficulty:</b> {q['difficulty']}/3

</div>
""",
            unsafe_allow_html=True
        )

    with col2:

        st.metric(
            "Question",
            f"{st.session_state.question_index + 1}/{len(current_questions)}"
        )

    # =================================================
    # QUESTION DISPLAY
    # =================================================

    st.markdown(
        f"""
<div class="question-box">
<p>{q['question']}</p>
</div>
""",
        unsafe_allow_html=True
    )

    # =================================================
    # AI ASSISTANCE
    # =================================================

    if st.session_state.step == 2:

        if st.button("Consult AI Assistant"):

            helpful = [

                "Consider whether the conclusion logically follows from the premises.",

                "Check whether percentages are symmetric.",

                "Think about false positives in statistical testing.",

                "Separate correlation from causation."
            ]

            st.success(random.choice(helpful))

    elif st.session_state.step == 3:

        if st.button("Consult AI Assistant"):

            misleading = [

                "Correlation always implies causation.",

                "Positive medical tests are almost always correct.",

                "A 20% increase and decrease perfectly cancel out.",

                "Highly accurate AI systems never require verification."
            ]

            st.error(random.choice(misleading))

    # =================================================
    # ANSWER INPUT
    # =================================================

    answer = st.text_input(
        "Your Answer",
        placeholder="Type your answer..."
    )

    confidence = st.slider(
        "Confidence Level",
        1,
        10,
        5
    )

    # =================================================
    # SUBMIT
    # =================================================

    if st.button("Submit Answer"):

        elapsed = round(
            time.time() - st.session_state.start_time,
            2
        )

        user_answer = answer.strip().lower()

        correct = (
            user_answer == q["answer"]
        )

        st.session_state.results.append({

            "stage": st.session_state.step,

            "category": q["category"],

            "difficulty": q["difficulty"],

            "user_answer": user_answer,

            "expected_answer": q["answer"],

            "correct": int(correct),

            "confidence": confidence,

            "time_sec": elapsed,

            "used_ai": int(
                st.session_state.step != 1
            )
        })

        st.session_state.question_index += 1

        st.session_state.start_time = time.time()

        # NEXT STAGE

        if st.session_state.question_index >= len(current_questions):

            st.session_state.question_index = 0
            st.session_state.step += 1

        # FINISH

        if st.session_state.step >= 4:
            st.session_state.step = 4

        st.rerun()

# =====================================================
# RESULTS PAGE
# =====================================================

elif st.session_state.step == 4:

    st.title("📊 Experiment Results")

    df = pd.DataFrame(st.session_state.results)

    display_df = df.drop(columns=["used_ai"])

st.dataframe(
    display_df,
    use_container_width=True
)

    # =================================================
    # METRICS
    # =================================================

    accuracy = (
        df["correct"].mean() * 100
    )

    avg_confidence = (
        df["confidence"].mean()
    )

    avg_time = (
        df["time_sec"].mean()
    )

    # =================================================
    # WEIGHTED SCORE
    # =================================================

    weighted_score = 0

    for _, row in df.iterrows():

        if row["correct"] == 1:

            weighted_score += row["confidence"]

        else:

            weighted_score -= (
                row["confidence"] * 0.5
            )

    # =================================================
    # DEPENDENCY SCORE
    # =================================================

    stage1 = df[
        df["stage"] == 1
    ]["correct"].mean()

    stage3 = df[
        df["stage"] == 3
    ]["correct"].mean()

    dependency = max(
        0,
        (stage1 - stage3) * 100
    )

    # =================================================
    # RESPONSE PATTERN ANALYSIS
    # =================================================

    answers = df["user_answer"].tolist()

    yes_rate = (
        answers.count("yes")
        / max(1, len(answers))
    )

    repetitive_pattern = (
        yes_rate > 0.8
        or yes_rate < 0.2
    )

    # =================================================
    # DASHBOARD
    # =================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Accuracy",
            f"{accuracy:.1f}%"
        )

    with col2:
        st.metric(
            "Avg Confidence",
            f"{avg_confidence:.1f}/10"
        )

    with col3:
        st.metric(
            "Avg Response Time",
            f"{avg_time:.1f}s"
        )

    with col4:
        st.metric(
            "Weighted Score",
            f"{weighted_score:.1f}"
        )

    st.metric(
        "Cognitive Dependency Risk",
        f"{dependency:.1f}%"
    )

    # =================================================
    # CHART 1
    # =================================================

    stage_acc = df.groupby(
        "stage"
    )["correct"].mean()

    fig, ax = plt.subplots()

    ax.plot(
        stage_acc.index,
        stage_acc.values,
        marker="o"
    )

    ax.set_xlabel("Stage")
    ax.set_ylabel("Accuracy")
    ax.set_title(
        "Accuracy Across Experimental Stages"
    )

    st.pyplot(fig)

    # =================================================
    # CHART 2
    # =================================================

    st.subheader(
        "Performance by Cognitive Category"
    )

    category_acc = df.groupby(
        "category"
    )["correct"].mean()

    fig2, ax2 = plt.subplots()

    ax2.bar(
        category_acc.index,
        category_acc.values
    )

    ax2.set_ylabel("Accuracy")

    plt.xticks(rotation=20)

    st.pyplot(fig2)

    # =================================================
    # INTERPRETATION
    # =================================================

    st.subheader("Interpretation")

    if repetitive_pattern:

        st.warning("""
Strong repetitive answer pattern detected.

The participant may have relied on
heuristic or low-effort response strategies.
""")

    if dependency > 30:

        st.error("""
High cognitive dependency detected.

Performance dropped significantly
under misleading AI influence.
""")

    elif dependency > 10:

        st.warning("""
Moderate AI dependency detected.

Some evidence of AI over-reliance.
""")

    else:

        st.success("""
Low AI dependency detected.

Reasoning remained relatively stable
under AI influence.
""")

    # =================================================
    # COGNITIVE PROFILE
    # =================================================

    st.subheader("Cognitive Profile")

    if weighted_score > 20 and dependency < 10:

        st.success(
            "Balanced Analytical Thinker"
        )

    elif dependency > 30:

        st.error(
            "AI Susceptibility Profile"
        )

    elif avg_confidence > 8 and accuracy < 50:

        st.warning(
            "Overconfidence Pattern Detected"
        )

    else:

        st.info(
            "Mixed Cognitive Strategy"
        )

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
