import streamlit as st
from marcel_core import analyze_sentence


st.set_page_config(page_title="Marcel", page_icon="🐈", layout="centered")

EXAMPLES = {
    "Wrong classifier: 两本猫 → 两只猫": "两本猫",
    "Missing classifier: 三猫 → 三只猫": "三猫",
    "二 vs 两: 二只猫 → 两只猫": "二只猫",
    "Combined error: 二狗 → 两只狗": "二狗",
    "Adjective pattern: 三漂亮猫 → 三只漂亮猫": "三漂亮猫",
    "Adjective + 的: 三漂亮的猫 → 三只漂亮的猫": "三漂亮的猫",
    "Correct sentence: 三只猫": "三只猫",
}

with st.sidebar:
    st.title("Marcel 🐈")
    st.markdown("**Rule-based Chinese classifier checker**")

    st.markdown("### What it detects")
    st.write("• Missing classifiers")
    st.write("• Wrong classifier–noun pairs")
    st.write("• 二 vs 两 before classifiers")

    st.markdown("### Current scope")
    st.caption(
        "Marcel is a small educational NLP prototype. "
        "It uses predefined rules and a limited classifier dictionary."
    )

    st.markdown("### Tech")
    st.caption("Python · Streamlit · pytest · Rule-based NLP")

    st.markdown("### Note")
    st.caption(
        "Marcel is a prototype and does not cover full Chinese grammar."
    )


st.title("Marcel 🐈")
st.markdown("## Chinese Classifier Error Checker")

st.write(
    "Marcel detects common Chinese classifier mistakes in learner-generated "
    "sentences and explains corrections in a simple, learner-friendly way."
)

st.markdown("---")

st.markdown("### Try an example")

example_label = st.selectbox(
    "Choose a sample sentence:",
    list(EXAMPLES.keys()),
)

default_sentence = EXAMPLES[example_label]

sentence = st.text_input(
    "Or enter your own Chinese sentence:",
    value=default_sentence,
)

if sentence:
    result = analyze_sentence(sentence)

    st.markdown("### Result")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Original**")
        st.info(result["original_sentence"])

    with col2:
        st.markdown("**Corrected**")
        st.success(result["corrected_sentence"])
    
    st.markdown("### Analysis summary")
    
    st.metric("Total errors", result["total_errors"])
    
    if result["total_errors"] == 0:
        st.success(
        "No classifier errors found. The sentence looks correct within Marcel's current rule set."
        )
    else:
        st.markdown("### Detected errors")

        for index, error in enumerate(result["errors"], start=1):
            error_type = error["type"].replace("_", " ").title()

            with st.container(border=True):
                st.markdown(f"**Error {index}: {error_type}**")
                st.markdown(f"`{error['wrong']}` → `{error['correct']}`")
                st.write(error["explanation"])

    with st.expander("Structured JSON output"):
        st.json(result)

st.markdown("---")
st.caption(
    "Current version: rule-based MVP. Marcel supports a small classifier dictionary "
    "and basic learner error patterns."
)