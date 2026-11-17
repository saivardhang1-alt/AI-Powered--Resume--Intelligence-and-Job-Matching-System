def calculate_ats_score(resume_text, job_description):

    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())

    if not job_words:
        return 0

    matched_words = resume_words.intersection(job_words)

    score = (len(matched_words) / len(job_words)) * 100

    return round(score, 2)


def get_missing_keywords(resume_text, job_description):

    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())

    missing_words = job_words - resume_words

    return list(missing_words)
