import streamlit as st
from roadmap_generator import generate_skill_list, generate_resources_for_skill
from resource_fetcher import get_youtube_links

from fpdf import FPDF
import markdown
import base64
import re

st.set_page_config(page_title="AI Roadmap Builder", layout="centered")
st.title("🎯 AI Roadmap Builder")

goal = st.text_input("Enter your goal (e.g., Become a quant researcher):")

# -------------------------- Export Helpers --------------------------

def generate_markdown(goal, skill_map):
    md = f"# AI Roadmap for: {goal}\n\n"
    for skill, details in skill_map.items():
        md += f"## {skill}\n{details}\n\n"
    return md

def generate_pdf_from_md(md_content):
    html = markdown.markdown(md_content)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in html.split('\n'):
        pdf.multi_cell(0, 10, line)
    return pdf.output(dest="S").encode("latin1")

def download_button(label, data, filename):
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{label}</a>'
    st.markdown(href, unsafe_allow_html=True)

def remove_emojis(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

# -------------------------- Main Logic --------------------------

if st.button("Generate Full Roadmap"):
    if goal:
        with st.spinner("Generating roadmap..."):
            skills = generate_skill_list(goal)
            st.success("✅ Skill list generated!")

            skill_outputs = {}

            for skill in skills:
                st.subheader(f"📚 {skill}")
                with st.spinner(f"Finding resources and projects for: {skill}"):
                    output = generate_resources_for_skill(skill)
                    links = get_youtube_links(skill)

                    skill_outputs[skill] = (
                        f"{output}\n\n### 📺 YouTube Tutorials:\n"
                        + "\n".join([f"- [{link}]({link})" for link in links])
                    )

                    st.markdown(output)
                    st.markdown("**📺 YouTube Tutorials:**")
                    for link in links:
                        st.markdown(f"- [{link}]({link})")


            # Export
            md = generate_markdown(goal, skill_outputs)
            md_clean = remove_emojis(md)
            st.markdown("---")
            st.subheader("🗂️ Export Roadmap")

            # Markdown download
            download_button("⬇️ Download as Markdown", md_clean, f"{goal}_roadmap.md")

            # PDF download
            pdf_data = generate_pdf_from_md(md_clean)
            b64_pdf = base64.b64encode(pdf_data).decode()
            pdf_link = f'<a href="data:application/pdf;base64,{b64_pdf}" download="{goal}_roadmap.pdf">⬇️ Download as PDF</a>'
            st.markdown(pdf_link, unsafe_allow_html=True)
    else:
        st.warning("Please enter a goal.")