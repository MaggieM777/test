import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt

# -----------------------------
# SESSION STATE
# -----------------------------
if "data" not in st.session_state:
    st.session_state.data = []

if "step" not in st.session_state:
    st.session_state.step = 1


# -----------------------------
# PROFESSIONAL QUESTION SET
# -----------------------------
tasks = [
    # LOGICAL REASONING
    {"q": "All roses are flowers. Some flowers fade quickly. Can we conclude that some roses fade quickly?", "a": "no"},
    {"q": "If A > B and B > C, is A > C always true?", "a": "yes"},

    # MATH
    {"q": "A bat and ball cost $1.10. Bat costs $1 more than ball. Ball price?", "a": "0.05"},
    {"q": "What is 18 × 6?", "a": "108"},

    # DEBUGGING
    {"q": "Find bug: print('Hello world'", "a": "missing parenthesis"},
    {"q": "What is len([1,2,3,4])?", "a": "4"},

    # AMBIGUOUS THINKING
    {"q": "A system increases productivity by 20% but errors by 30%. Is it good?", "a": "depends"},
    {"q": "AI is 60% accurate but confident. Should you fully trust it?", "a": "no"},

    # AI CRITICAL THINKING
    {"q": "AI says: 'Capital of Australia is Sydney'. Is this correct?", "a": "no"},
    {"q": "AI says: '5+5=11 because of abstract numeric shift'. Correct?", "a": "no"}
]


# -----------------------------
# UI
# -----------------------------
st.title("🧠 AI Cognitive Impact Experiment")

st.write("Step:", st.session_state.step)


# -----------------------------
# STEP 1: NO AI
# -----------------------------
if st.session_state.step == 1:
    st.subheader("Stage 1: No AI (Baseline)")

    task = random.choice(tasks)
    st.write(task["q"])

    answer = st.text_input("Your answer")
    confidence = st.slider("Confidence (1–10)", 1, 10)

    if st.button("Submit"):
        st.session_state.data.append({
            "step": 1,
            "correct": answer.strip().lower() == task["a"],
            "confidence": confidence,
            "ai_used": 0
        })
        st.session_state.step = 2
        st.rerun()


# -----------------------------
# STEP 2: WITH AI (SIMULATED)
# -----------------------------
elif st.session_state.step == 2:
    st.subheader("Stage 2: With AI assistance")

    task = random.choice(tasks)
    st.write(task["q"])

    if st.button("Ask AI"):
        st.info("AI: Think step-by-step, verify assumptions, do not trust blindly.")

    answer = st.text_input("Final answer")
    confidence = st.slider("Confidence (1–10)", 1, 10)

    if st.button("Submit"):
        st.session_state.data.append({
            "step": 2,
            "correct": answer.strip().lower() == task["a"],
            "confidence": confidence,
            "ai_used": 1
        })
        st.session_state.step = 3
        st.rerun()


# -----------------------------
# STEP 3: TRAP TEST
# -----------------------------
elif st.session_state.step == 3:
    st.subheader("Stage 3: AI Trap (Critical Thinking Test)")

    task = {"q": "What is 2 + 2?", "a": "4"}

    st.write(task["q"])

    if st.button("Ask AI"):
        st.warning("AI: 2 + 2 = 5 (intentional wrong answer)")

    answer = st.text_input("Your answer")
    confidence = st.slider("Confidence (1–10)", 1, 10)

    if st.button("Submit"):
        st.session_state.data.append({
            "step": 3,
            "correct": answer.strip() == "4",
            "confidence": confidence,
            "ai_used": 1
        })
        st.session_state.step = 4
        st.rerun()


# -----------------------------
# STEP 4: FINAL NO AI
# -----------------------------
elif st.session_state.step == 4:
    st.subheader("Stage 4: Final Test (No AI)")

    task = random.choice(tasks)
    st.write(task["q"])

    answer = st.text_input("Your answer")
    confidence = st.slider("Confidence (1–10)", 1, 10)

    if st.button("Finish"):
        st.session_state.data.append({
            "step": 4,
            "correct": answer.strip().lower() == task["a"],
            "confidence": confidence,
            "ai_used": 0
        })
        st.session_state.step = 5
        st.rerun()


# -----------------------------
# ANALYSIS DASHBOARD
# -----------------------------
elif st.session_state.step == 5:
    st.subheader("📊 Results & Cognitive Analysis")

    df = pd.DataFrame(st.session_state.data)

    st.dataframe(df)

    # -----------------------------
    # ACCURACY
    # -----------------------------
    acc = df.groupby("step")["correct"].mean()

    fig, ax = plt.subplots()
    ax.plot(acc.index, acc.values, marker="o")
    ax.set_title("Accuracy per Stage")
    ax.set_xlabel("Stage")
    ax.set_ylabel("Accuracy")

    st.pyplot(fig)

    # -----------------------------
    # CONFIDENCE
    # -----------------------------
    conf = df.groupby("step")["confidence"].mean()

    fig2, ax2 = plt.subplots()
    ax2.plot(conf.index, conf.values, marker="o")
    ax2.set_title("Confidence per Stage")

    st.pyplot(fig2)

    # -----------------------------
    # AI USAGE
    # -----------------------------
    ai = df.groupby("step")["ai_used"].mean()

    fig3, ax3 = plt.subplots()
    ax3.bar(ai.index, ai.values)
    ax3.set_title("AI Usage Rate")

    st.pyplot(fig3)

    # -----------------------------
    # INTERPRETATION
    # -----------------------------
    st.subheader("Interpretation")

    st.write("""
    - Drop in Stage 4 → cognitive dependency risk
    - High AI usage + lower accuracy → cognitive offloading
    - High confidence + low accuracy → possible overconfidence (Dunning–Kruger effect)
    - Trap failure → reduced critical evaluation of AI outputs
    """)
