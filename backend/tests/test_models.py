from backend.models import Education, Experience, ParsedCV, Project

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