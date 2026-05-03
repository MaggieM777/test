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
# TASKS
# -----------------------------
tasks = [
    {"q": "What is 12 * 7?", "a": "84"},
    {"q": "Find error: print('Hello world'", "a": "missing parenthesis"},
    {"q": "Logic: All dogs are animals. Are all animals dogs?", "a": "no"},
]


# -----------------------------
# UI
# -----------------------------
st.title("AI Cognitive Impact Experiment")


# -----------------------------
# STEP 1 - NO AI
# -----------------------------
if st.session_state.step == 1:
    st.subheader("Stage 1: No AI")

    task = random.choice(tasks)
    st.write(task["q"])

    answer = st.text_input("Answer")
    confidence = st.slider("Confidence (1-10)", 1, 10)

    if st.button("Submit"):
        st.session_state.data.append({
            "step": 1,
            "correct": answer.lower().strip() == task["a"],
            "confidence": confidence,
            "ai_used": 0
        })
        st.session_state.step = 2
        st.rerun()


# -----------------------------
# STEP 2 - AI ALLOWED (SIMULATED)
# -----------------------------
elif st.session_state.step == 2:
    st.subheader("Stage 2: With AI")

    task = random.choice(tasks)
    st.write(task["q"])

    if st.button("Ask AI"):
        st.info("AI: Think step-by-step and verify your answer.")

    answer = st.text_input("Final answer")
    confidence = st.slider("Confidence (1-10)", 1, 10)

    if st.button("Submit"):
        st.session_state.data.append({
            "step": 2,
            "correct": answer.lower().strip() == task["a"],
            "confidence": confidence,
            "ai_used": 1
        })
        st.session_state.step = 3
        st.rerun()


# -----------------------------
# STEP 3 - TRAP TEST
# -----------------------------
elif st.session_state.step == 3:
    st.subheader("Stage 3: AI Trap")

    task = {"q": "What is 3 + 3?", "a": "6"}

    st.write(task["q"])

    if st.button("Ask AI"):
        st.warning("AI: 3 + 3 = 7")  # intentional wrong answer

    answer = st.text_input("Answer")
    confidence = st.slider("Confidence (1-10)", 1, 10)

    if st.button("Submit"):
        st.session_state.data.append({
            "step": 3,
            "correct": answer.strip() == "6",
            "confidence": confidence,
            "ai_used": 1
        })
        st.session_state.step = 4
        st.rerun()


# -----------------------------
# STEP 4 - FINAL NO AI
# -----------------------------
elif st.session_state.step == 4:
    st.subheader("Stage 4: Final No AI")

    task = random.choice(tasks)
    st.write(task["q"])

    answer = st.text_input("Answer")
    confidence = st.slider("Confidence (1-10)", 1, 10)

    if st.button("Finish"):
        st.session_state.data.append({
            "step": 4,
            "correct": answer.lower().strip() == task["a"],
            "confidence": confidence,
            "ai_used": 0
        })
        st.session_state.step = 5
        st.rerun()


# -----------------------------
# ANALYSIS
# -----------------------------
elif st.session_state.step == 5:
    st.subheader("Results")

    df = pd.DataFrame(st.session_state.data)

    st.dataframe(df)

    # Accuracy
    acc = df.groupby("step")["correct"].mean()

    fig, ax = plt.subplots()
    ax.plot(acc.index, acc.values, marker="o")
    ax.set_title("Accuracy per Stage")
    ax.set_xlabel("Stage")
    ax.set_ylabel("Accuracy")

    st.pyplot(fig)

    # Confidence
    conf = df.groupby("step")["confidence"].mean()

    fig2, ax2 = plt.subplots()
    ax2.plot(conf.index, conf.values, marker="o")
    ax2.set_title("Confidence per Stage")

    st.pyplot(fig2)

    # AI usage
    ai = df.groupby("step")["ai_used"].mean()

    fig3, ax3 = plt.subplots()
    ax3.bar(ai.index, ai.values)
    ax3.set_title("AI Usage")

    st.pyplot(fig3)

    st.write("Interpretation:")
    st.write("- Drop in stage 4 = dependency risk")
    st.write("- High confidence + low accuracy = overconfidence")
    st.write("- AI usage correlates with performance changes")
