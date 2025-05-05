import os
import requests
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

print("Token loaded:", bool(GITHUB_TOKEN))  


def simplify_skill(skill):
    keywords = {
        "quantitative": "quant finance",
        "python": "python data science",
        "c++": "c++ beginner project",
        "statistics": "data analysis",
        "communication": "presentation tool",
        "financial": "finance trading",
        "dataset": "data science",
        "javascript": "html css javascript",
        "react": "react frontend",
        "sql": "mysql postgresql",
        "git": "git github version control"
    }

    skill = skill.lower()
    for key, value in keywords.items():
        if key in skill:
            return value
    return skill

def get_github_projects(skill, max_results=2):
    base_keywords = simplify_skill(skill)
    if not base_keywords or len(base_keywords.split()) < 2:
        base_keywords = "python beginner project"

    query = (
        f"{base_keywords} tutorial example "
        "pushed:>2019-05-01 stars:>5"
    )

    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": max_results * 2
    }

    headers = {
        "Accept": "application/vnd.github+json"
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    if "items" not in data:
        return ["- ⚠️ GitHub API Error: " + data.get("message", "Unknown")]

    items = data["items"]

    projects = []
    for item in items:
        if item["stargazers_count"] < 10:
            continue
        name = item["full_name"]
        link = item["html_url"]
        stars = item["stargazers_count"]
        projects.append(f"- [{name}]({link}) ⭐ {stars} stars")
        if len(projects) >= max_results:
            break

    return projects or ["- _No relevant GitHub repos found._"]