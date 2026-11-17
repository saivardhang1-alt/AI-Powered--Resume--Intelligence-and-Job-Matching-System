const form = document.getElementById("resumeForm");
const result = document.getElementById("result");

form.addEventListener("submit", async function(event) {
    event.preventDefault();

    const resume = document.getElementById("resume").files[0];
    const jobDescription = document.getElementById("jobDescription").value;

    if (!resume) {
        result.textContent = "Please upload your resume.";
        return;
    }

    const formData = new FormData();

    formData.append("file", resume);
    formData.append("job_description", jobDescription);

    result.textContent = "Analyzing your resume...";

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/analyze-resume/",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Analysis failed");
        }

        const analysis = data.analysis;

       result.innerHTML = `
    <h2>Resume Analysis Result</h2>

    <div class="score-card">
        <h3>ATS Match Score</h3>
        <h1>${analysis.match_score}%</h1>

<div class="progress-bar">
    <div class="progress"
         style="width: ${analysis.match_score}%">
    </div>
</div>
    </div>

    <div class="analysis-card">
        <h3>Matched Skills</h3>
        <p>${analysis.matched_skills.join(", ") || "None"}</p>
    </div>

    <div class="analysis-card">
        <h3>Missing Skills</h3>
        <p>${analysis.missing_skills.join(", ") || "None"}</p>
    </div>

    <div class="analysis-card">
        <h3>Missing Keywords</h3>
        <p>${analysis.missing_keywords.join(", ") || "None"}</p>
    </div>
`;
    } catch (error) {
        result.textContent = "Error: " + error.message;
    }
});
