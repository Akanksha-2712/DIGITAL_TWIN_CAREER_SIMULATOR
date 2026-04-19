from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__, static_folder='public', static_url_path='/public')

# ─────────────────────────────────────────────────────────
# MOCK DATABASE – Skills (Categorized) & Careers
# ─────────────────────────────────────────────────────────

skills = [
    # Frontend
    {"id": 1,  "name": "HTML/CSS",              "category": "Frontend"},
    {"id": 2,  "name": "JavaScript",            "category": "Frontend"},
    {"id": 3,  "name": "React.js",              "category": "Frontend"},
    {"id": 4,  "name": "Vue.js",                "category": "Frontend"},
    {"id": 5,  "name": "Tailwind CSS",          "category": "Frontend"},

    # Backend
    {"id": 6,  "name": "Node.js",               "category": "Backend"},
    {"id": 7,  "name": "Python",                "category": "Backend"},
    {"id": 8,  "name": "Java",                  "category": "Backend"},
    {"id": 9,  "name": "PHP/Laravel",           "category": "Backend"},
    {"id": 10, "name": "SQL",                   "category": "Backend"},
    {"id": 11, "name": "Go",                    "category": "Backend"},

    # Full Stack
    {"id": 12, "name": "Next.js",               "category": "Full Stack"},
    {"id": 13, "name": "MERN Stack",            "category": "Full Stack"},
    {"id": 14, "name": "Docker / DevOps",       "category": "Full Stack"},
    {"id": 15, "name": "Cloud (AWS/Azure)",     "category": "Full Stack"},

    # Designing
    {"id": 16, "name": "UI/UX Design",          "category": "Designing"},
    {"id": 17, "name": "Figma",                 "category": "Designing"},
    {"id": 18, "name": "Creative Tools (Adobe)","category": "Designing"},
    {"id": 19, "name": "Prototyping",           "category": "Designing"},

    # Soft Skills
    {"id": 20, "name": "Leadership",            "category": "Soft Skills"},
    {"id": 21, "name": "Communication",         "category": "Soft Skills"},
    {"id": 22, "name": "Project Management",    "category": "Soft Skills"},
    {"id": 23, "name": "Agile & Scrum",         "category": "Soft Skills"},

    # Trending in Market
    {"id": 24, "name": "Machine Learning",      "category": "Trending in Market"},
    {"id": 25, "name": "Data Analysis",         "category": "Trending in Market"},
    {"id": 26, "name": "Generative AI Prompts", "category": "Trending in Market"},
    {"id": 27, "name": "Cybersecurity",         "category": "Trending in Market"},
]

careers = [
    {
        "id": 1, "title": "Frontend Developer",
        "description": "Create beautiful, responsive user interfaces and web applications.",
        "base_salary": 80000, "growth_rate": 0.05,
        "skills": [{"id": 1, "weight": 5}, {"id": 2, "weight": 5}, {"id": 3, "weight": 4}, {"id": 5, "weight": 3}]
    },
    {
        "id": 2, "title": "Backend / Server Engineer",
        "description": "Build and optimize scalable server-side systems and APIs.",
        "base_salary": 90000, "growth_rate": 0.05,
        "skills": [{"id": 6, "weight": 4}, {"id": 10, "weight": 5}, {"id": 8, "weight": 4}, {"id": 11, "weight": 3}]
    },
    {
        "id": 3, "title": "Full Stack Developer",
        "description": "End-to-end software development spanning frontend and backend architectures.",
        "base_salary": 105000, "growth_rate": 0.06,
        "skills": [{"id": 2, "weight": 4}, {"id": 3, "weight": 4}, {"id": 6, "weight": 4}, {"id": 10, "weight": 3}, {"id": 13, "weight": 4}]
    },
    {
        "id": 4, "title": "UI/UX Designer",
        "description": "Design engaging, user-friendly interfaces with a focus on experience.",
        "base_salary": 75000, "growth_rate": 0.04,
        "skills": [{"id": 16, "weight": 5}, {"id": 17, "weight": 5}, {"id": 19, "weight": 4}, {"id": 21, "weight": 3}]
    },
    {
        "id": 5, "title": "Data Scientist",
        "description": "Extract insights from complex data sets to drive business decisions.",
        "base_salary": 110000, "growth_rate": 0.07,
        "skills": [{"id": 7, "weight": 5}, {"id": 25, "weight": 5}, {"id": 10, "weight": 4}, {"id": 24, "weight": 4}]
    },
    {
        "id": 6, "title": "Product Manager",
        "description": "Lead product strategy, vision, and delivery effectively across teams.",
        "base_salary": 115000, "growth_rate": 0.04,
        "skills": [{"id": 20, "weight": 4}, {"id": 21, "weight": 5}, {"id": 22, "weight": 5}, {"id": 23, "weight": 4}]
    },
    {
        "id": 7, "title": "DevOps & Cloud Engineer",
        "description": "Automate deployments and maintain robust cloud infrastructures.",
        "base_salary": 112000, "growth_rate": 0.06,
        "skills": [{"id": 14, "weight": 5}, {"id": 15, "weight": 5}, {"id": 7, "weight": 3}, {"id": 21, "weight": 2}]
    },
    {
        "id": 8, "title": "AI Solutions Architect",
        "description": "Implement cutting-edge AI and Machine Learning models into production.",
        "base_salary": 135000, "growth_rate": 0.10,
        "skills": [{"id": 24, "weight": 5}, {"id": 26, "weight": 5}, {"id": 7, "weight": 4}, {"id": 15, "weight": 3}]
    },
    {
        "id": 9, "title": "Cybersecurity Analyst",
        "description": "Protect organizational data and mitigate external cyber threats.",
        "base_salary": 95000, "growth_rate": 0.07,
        "skills": [{"id": 27, "weight": 5}, {"id": 10, "weight": 3}, {"id": 7, "weight": 3}, {"id": 21, "weight": 3}]
    },
    {
        "id": 10, "title": "Scrum Master / Agile Coach",
        "description": "Facilitate agile ceremonies and improve team delivery efficiency.",
        "base_salary": 85000, "growth_rate": 0.03,
        "skills": [{"id": 23, "weight": 5}, {"id": 20, "weight": 4}, {"id": 21, "weight": 5}, {"id": 22, "weight": 5}]
    },
]


def get_skill_by_id(skill_id):
    return next((s for s in skills if s["id"] == skill_id), None)


def get_expanded_careers():
    result = []
    for c in careers:
        expanded_skills = []
        for cs in c["skills"]:
            skill_obj = get_skill_by_id(cs["id"])
            if skill_obj:
                expanded_skills.append({
                    "id": skill_obj["id"],
                    "name": skill_obj["name"],
                    "pivot": {"weight": cs["weight"]}
                })
        result.append({**c, "skills": expanded_skills})
    return result


# ─────────────────────────────────────────────────────────
# WEB ROUTES (HTML Pages)
# ─────────────────────────────────────────────────────────

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/results")
def results():
    return render_template("results.html")

@app.route("/compare")
def compare():
    return render_template("compare.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")


# ─────────────────────────────────────────────────────────
# API ROUTES (JSON)
# ─────────────────────────────────────────────────────────

@app.route("/api/skills")
def api_skills():
    return jsonify(skills)

@app.route("/api/careers")
def api_careers():
    return jsonify(get_expanded_careers())

@app.route("/api/simulate", methods=["POST"])
def api_simulate():
    data = request.get_json()
    user_skills = data.get("skills", [])
    experience_level = data.get("experience_level", "Intermediate")

    exp_multiplier = {"Advanced": 1.2, "Intermediate": 1.0, "Beginner": 0.8}.get(experience_level, 1.0)

    all_careers = get_expanded_careers()
    results = []

    for career in all_careers:
        score = 0
        max_score = 0
        missing = []
        required = []

        for skill in career["skills"]:
            weight = skill["pivot"]["weight"]
            max_score += weight
            required.append({"id": skill["id"], "name": skill["name"]})
            if skill["id"] in user_skills:
                score += weight
            else:
                missing.append({"id": skill["id"], "name": skill["name"]})

        match_pct = (score / max_score * 100) if max_score > 0 else 0

        # Filter out careers with less than 15% match
        if match_pct > 15:
            match_pct = min(100, match_pct * exp_multiplier)

            projection = []
            cur_salary = career["base_salary"]
            for i in range(6):
                projection.append({"year": i, "salary": round(cur_salary)})
                cur_salary *= (1 + career["growth_rate"])

            results.append({
                "career_id": career["id"],
                "title": career["title"],
                "description": career["description"],
                "match_percentage": round(match_pct, 1),
                "salary_projection": projection,
                "missing_skills": missing,
                "required_skills": required,
            })

    results.sort(key=lambda x: x["match_percentage"], reverse=True)
    return jsonify(results[:4])


# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
