from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape
from main import ParsedCV, Project, Education, Experience
from pathlib import Path

templates_dir = Path(__file__).parent / "data" / "templates"

env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape()
)
template = env.get_template("1.html")

person = ParsedCV(name="Lola Loki", email="lola@lola.com", location="Warsaw", phone = "678 432 280", job_title="Python Developer", bio = "Experienced and excellent Lola Loki", skills = ["Python", "Docker", "DRF"], languages=["English C1", "Polish native"],
                  projects = [Project(title="Project 1", tools = "xyz zyc", description = ["xxxxx", "yyyyy", "zzzzz"], link = "https://lola.com")],
                  experience = [Experience(title = "Developer X", company = "Company Y", date = "05-2021 - 05-2023", description = ["xxxxx", "yyyy", "zzzz"])],
                  education = [Education(degree = "Bachelor", field = "xxx", school_name = "Lola school", date = "06-2018 - 09-2020")])

html_context =     template.render(
        name=person.name,
        job_title=person.job_title,
        location=person.location,
        phone=person.phone,
        email=person.email,
        bio=person.bio,
        skills={"Languages": ["Python"], "Frameworks": ["Django", "FastAPI"]},  # lub cv.skills jako dict
        projects=[p.model_dump() for p in person.projects],
        experience=[e.model_dump() for e in person.experience],
        education=[e.model_dump() for e in person.education],
        languages=person.languages
    )

output_dir = Path(__file__).parent / "data" / "renders"
output_dir.mkdir(exist_ok=True)
html_path = output_dir / "html/output_1.html"

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_context)
print("HTML saved.")

# Covert template from HTML to PDF
pdf_path = output_dir / "pdf/output.pdf"
HTML(string=html_context).write_pdf(pdf_path)
print("PDF saved")

