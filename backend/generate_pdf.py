from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape
from models import ParsedCV, Project, Education, Experience
from pathlib import Path

class GeneratePDF:
    def __init__(self):
        self.templates_dir = Path(__file__).parent / "data" / "templates"
        self.env = Environment(
        loader=FileSystemLoader(self.templates_dir),
        autoescape=select_autoescape()
        )
        self.output_dir = Path(__file__).parent / "data" / "renders"
        self.output_dir.mkdir(exist_ok=True)

    def generate_pdf_name(self, name, jobtitle):
        clean_name = "".join(name.split())
        clean_job_title = "".join(jobtitle.split())
        return f"CV_{clean_name}_{clean_job_title}.pdf"

        # pdf_path = self.output_dir / f"pdf/CV_{clean_name}_{clean_job_title}.pdf"
        # return pdf_path

    def render_template(self, cv_data: ParsedCV):
        #Potem dodać template jako argument do wyboru
        template = self.env.get_template("1.html")

        html_content = template.render(
            name=cv_data.name,
            job_title = cv_data.job_title,
            location=cv_data.location,
                phone=cv_data.phone,
                email=cv_data.email,
                bio=cv_data.bio,
                skills={"Languages": ["Python"], "Frameworks": ["Django", "FastAPI"]},  # lub cv.skills jako dict
                projects=[p.model_dump() for p in cv_data.projects],
                experience=[e.model_dump() for e in cv_data.experience],
                education=[e.model_dump() for e in cv_data.education],
                languages=cv_data.languages
            )
        return html_content

    def generate_pdf(self, cv_data:ParsedCV) -> bytes:
        "Generate cv and return it as bytes"

        html_content = self.render_template(cv_data)
        pdf_bytes = HTML(string=html_content).write_pdf()

        return pdf_bytes

    def save_html(self, cv_data, html_context: str):
        html_path = self.output_dir / f"html/CV_{cv_data.name}.html"
        html_path.parent.mkdir(parents=True, exist_ok=True)

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_context)
        print("HTML saved.")

        return html_path

    # Convert HTML to PDF
    def convert_html_to_pdf(self, cv_data, html_context: str):
        pdf_path = self.generate_pdf_name(name=cv_data.name, jobtitle=cv_data.job_title)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)

        HTML(string=html_context).write_pdf(pdf_path)
        print("PDF saved.")
        return pdf_path