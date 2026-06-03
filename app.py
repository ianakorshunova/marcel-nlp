import streamlit as st
from marcel_core import analyze_sentence


st.set_page_config(page_title="Marcel", page_icon="🐈", layout="centered")

st.title("Marcel 🐈")
st.subheader("Chinese Classifier Checker")

st.write(
    "Marcel is a small rule-based tool that detects common Chinese classifier mistakes "
    "in learner-generated sentences."
)

st.markdown("### Try an example")

example = st.selectbox(
    "Choose a sample sentence:",
    [
        "两本猫",
        "三猫",
        "二只猫",
        "三漂亮猫",
        "三漂亮的猫",
        "三只猫",
    ],
)

sentence = st.text_input("Or enter your own Chinese sentence:", example)

if sentence:
    result = analyze_sentence(sentence)

    st.markdown("### Corrected sentence")

    if result["total_errors"] == 0:
        st.success(result["corrected_sentence"])
        st.info("No classifier errors found.")
    else:
        st.success(result["corrected_sentence"])

        st.markdown("### Summary")
        st.write(f"Total errors: **{result['total_errors']}**")

        st.markdown("### Detected errors")

        for error in result["errors"]:
            st.markdown(f"**{error['wrong']} → {error['correct']}**")
            st.write(error["explanation"])

    with st.expander("Structured JSON output"):
        st.json(result)

st.markdown("---")
st.caption(
    "Current version: rule-based MVP. Marcel supports a small classifier dictionary "
    "and basic learner error patterns."
)