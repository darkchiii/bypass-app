from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape
from main import ParsedCV, Project, Education, Experience
from pathlib import Path

templates_dir = Path(__file__).parent / "data" / "templates"
output_dir = Path(__file__).parent / "data" / "renders"
output_dir.mkdir(exist_ok=True)

env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape()
)

person = ParsedCV(name="Lola Loki", email="lola@lola.com", location="Warsaw", phone = "678 432 280", job_title="Python Developer", bio = "Experienced and excellent Lola Loki", skills = ["Python", "Docker", "DRF"], languages=["English C1", "Polish native"],
                  projects = [Project(title="Project 1", tools = "xyz zyc", description = ["xxxxx", "yyyyy", "zzzzz"], link = "https://lola.com")],
                  experience = [Experience(title = "Developer X", company = "Company Y", date = "05-2021 - 05-2023", description = ["xxxxx", "yyyy", "zzzz"])],
                  education = [Education(degree = "Bachelor", field = "xxx", school_name = "Lola school", date = "06-2018 - 09-2020")])

# Fill HTML template with data
def render_data(json_cv_data:ParsedCV, template):
    template = env.get_template(template)
    html_context = template.render(
        name=json_cv_data.name,
        job_title=json_cv_data.job_title,
        location=json_cv_data.location,
            phone=json_cv_data.phone,
            email=json_cv_data.email,
            bio=json_cv_data.bio,
            skills={"Languages": ["Python"], "Frameworks": ["Django", "FastAPI"]},  # lub cv.skills jako dict
            projects=[p.model_dump() for p in json_cv_data.projects],
            experience=[e.model_dump() for e in json_cv_data.experience],
            education=[e.model_dump() for e in json_cv_data.education],
            languages=json_cv_data.languages
        )
    return html_context

# Save HTML
def save_html(f_name, html_context: str):
    html_path = output_dir / f"html/{f_name}.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_context)
    print("HTML saved.")
    return html_path

# Convert HTML to PDF
def convert_html_to_pdf(f_name, html_context: str):
    pdf_path = output_dir / f"pdf/{f_name}.pdf"
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_context).write_pdf(pdf_path)
    print("PDF saved.")
    return pdf_path


html_context = render_data(json_cv_data=person, template="1.html")
save_html("output_1", html_context)
convert_html_to_pdf("output_1", html_context)
