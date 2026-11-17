TECHNICAL_SKILLS = [
    "python", "java", "javascript", "sql",
    "mysql", "mongodb", "fastapi", "django",
    "html", "css", "react", "node.js",
    "machine learning", "deep learning",
    "data science", "aws", "azure",
    "docker", "kubernetes", "git",
    "github", "pandas", "numpy",
    "opencv", "rest api"
]


def extract_skills(resume_text):

    text = resume_text.lower()

    found_skills = []

    for skill in TECHNICAL_SKILLS:
        if skill in text:
            found_skills.append(skill)

    return found_skills


def analyze_missing_skills(resume_text, job_description):

    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))

    missing_skills = job_skills - resume_skills

    return list(missing_skills)
