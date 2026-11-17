from ats_scorer import calculate_ats_score, get_missing_keywords
from skill_analyzer import extract_skills, analyze_missing_skills


def match_resume_with_job(resume_text, job_description):

    score = calculate_ats_score(
        resume_text,
        job_description
    )

    resume_skills = extract_skills(resume_text)

    missing_skills = analyze_missing_skills(
        resume_text,
        job_description
    )

    missing_keywords = get_missing_keywords(
        resume_text,
        job_description
    )
    suggestions = []

if missing_skills:
    suggestions.append(
        "Improve your resume by adding relevant missing skills that you genuinely possess."
    )

if missing_keywords:
    suggestions.append(
        "Include relevant missing keywords naturally in your resume."
    )

if score < 50:
    suggestions.append(
        "Consider improving your resume according to the job requirements."
    )

if not suggestions:
    suggestions.append(
        "Your resume has good alignment with the job description. Keep improving your experience and achievements."
    )

    return {
        "match_score": score,
        "matched_skills": resume_skills,
        "missing_skills": missing_skills,
        "missing_keywords": missing_keywords
        "suggestions":suggestions
    }
