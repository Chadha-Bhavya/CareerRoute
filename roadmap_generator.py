import os
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://ai-roadmap-builder.streamlit.app",
    "X-Title": "AI Roadmap Builder"
}

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_gpt(messages):
    response = httpx.post(BASE_URL, headers=headers, json={
        "model": "openai/gpt-3.5-turbo",
        "messages": messages
    })
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def generate_skill_list(goal):
    messages = [
        {"role": "system", "content": "You are an expert roadmap planner."},
        {"role": "user", "content": f"List 5 essential skills needed to achieve the goal: '{goal}'. Return only a bullet list."}
    ]
    content = ask_gpt(messages)
    skills = content.split("\n")
    return [skill.strip("•- ") for skill in skills if skill.strip()]

def generate_resources_for_skill(skill):
    messages = [
        {"role": "system", "content": "You are an expert educator and mentor."},
        {"role": "user", "content": f"For the skill '{skill}', give me:\n1. Two free learning resources (YouTube, blog, course)\n2. One beginner-friendly project idea.\nReturn in clean bullet points."}
    ]
    return ask_gpt(messages)