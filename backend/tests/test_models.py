from models import Education, Experience, ParsedCV, Project, JobApplication, Suggestion, JobRequirements

exp1 = Experience(
    title="Python Developer",
    company="TechCorp",
    date="2022-2024",
    description=[
        "Developed REST APIs",
        "Worked with FastAPI"
    ]
)

person = ParsedCV(name="Lola Loki", email="lola@lola.com", location="Warsaw", phone = "678 432 280", job_title="Python Developer", bio = "Experienced and excellent Lola Loki", skills = ["Python", "Docker", "DRF"], languages=["English C1", "Polish native"],
                  projects = [Project(title="Project 1", tools = "xyz zyc", description = ["xxxxx", "yyyyy", "zzzzz"], link = "https://lola.com")],
                  experience = [Experience(title = "Developer X", company = "Company Y", date = "05-2021 - 05-2023", description = ["xxxxx", "yyyy", "zzzz"])],
                  education = [Education(degree = "Bachelor", field = "xxx", school_name = "Lola school", date = "06-2018 - 09-2020")])
print(person)

suggestion1 = Suggestion(
    type="update_field",
    section="job_title",
    target=None,
    current_value="Python Developer",
    suggested_value="Java Developer",
    reason="Match job posting title for ATS optimization",
    status="pending",
    final_value=None
)

suggestion2 = Suggestion(
    type="rewrite",
    section="experience",
    target="experience[0].description[1]",
    current_value="Built REST APIs",
    suggested_value="Designed and implemented RESTful microservices using Java Spring Boot",
    reason="Incorporate job-specific keywords and technologies",
    status="pending",
    final_value=None
)

suggestion3 = Suggestion(
    type="add_keyword",
    section="bio",
    target=None,
    current_value="Backend developer with experience in Python",
    suggested_value="Backend developer specializing in Java and scalable enterprise applications",
    reason="Emphasize Java expertise mentioned in job requirements",
    status="pending",
    final_value=None
)

# Job requirements
job_reqs = JobRequirements(
    job_title="Senior Java Developer",
    company="XYZ Tech",
    key_skills=["Java", "Spring Boot", "Microservices", "PostgreSQL"],
    important_keywords=["scalable", "enterprise", "agile", "CI/CD"],
    responsibilities=[
        "Design and develop microservices architecture",
        "Collaborate with cross-functional teams",
        "Maintain high code quality standards"
    ],
    company_values=["innovation", "continuous learning", "teamwork"],
    tone="technical"
)

job_application = JobApplication(
    job_id="550e8400-e29b-41d4-a716",
    user_id="Lola",
    job_requirements=job_reqs,
    suggestions=[suggestion1, suggestion2, suggestion3],
    status="pending",
    analysis_model="full"
)

print(job_application.model_dump_json(indent=2))