import streamlit as st
from roadmap_generator import generate_skill_list

st.set_page_config(page_title="AI Roadmap Builder", layout="centered")
st.title("🎯 AI Roadmap Builder")

goal = st.text_input("Enter your goal (e.g., Become a Quant Researcher):")

if st.button("Generate Roadmap"):
    if goal:
        with st.spinner("Generating roadmap..."):
            skills = generate_skill_list(goal)
            st.success("Here’s your initial skill list:")
            for i, skill in enumerate(skills, 1):
                st.write(f"{i}. {skill}")
    else:
        st.warning("Please enter a goal.")