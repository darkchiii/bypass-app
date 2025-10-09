from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape
from models import ParsedCV, Project, Education, Experience, Suggestion
from pathlib import Path
from typing import List
import logging

logger = logging.getLogger(__name__)


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

    # Logging dodać
    def render_template(self, cv_data: ParsedCV):
        #Potem dodać template jako argument do wyboru
        template = self.env.get_template("1.html")
        if not template:
            logging.warning(f"Couldn't load template {template}")
            raise FileNotFoundError(f"Couldn't load template {template}")

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

    # Logging dodać
    def generate_pdf(self, cv_data:ParsedCV) -> bytes:
        "Generate cv and return it as bytes"

        html_content = self.render_template(cv_data)
        pdf_bytes = HTML(string=html_content).write_pdf()

        return pdf_bytes

    # Logging dodać
    def save_html(self, cv_data, html_context: str):
        html_path = self.output_dir / f"html/CV_{cv_data.name}.html"
        html_path.parent.mkdir(parents=True, exist_ok=True)

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_context)
        print("HTML saved.")

        return html_path

    # Logging dodać
    # Convert HTML to PDF
    def convert_html_to_pdf(self, cv_data, html_context: str):
        pdf_path = self.generate_pdf_name(name=cv_data.name, jobtitle=cv_data.job_title)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)

        HTML(string=html_context).write_pdf(pdf_path)
        print("PDF saved.")
        return pdf_path

# Logging dodany
def apply_suggestions(base_cv: ParsedCV, suggestions: List[Suggestion]):
    logger.info(f"Applying suggestions to CV: {len(suggestions)} total suggestions")

    modified_cv = base_cv.model_copy(deep=True)
    accepted_suggestions = [s for s in suggestions if s.status in ["modified", "accepted"]]

    logger.info(f"Processing {len(accepted_suggestions)} accepted/modified total suggestions")

    for idx, s in enumerate(accepted_suggestions):
        new_value = s.final_value if s.final_value else s.suggested_value
        logger.debug(f"Processing suggestion {idx}: {s.type} on {s.section}")

        if s.section == "job_title":
            modified_cv.job_title = new_value

        elif s.section == "bio":
            modified_cv.bio = new_value

        elif s.section == "skills":
            if s.target_item_index is not None:
                if s.target_item_index < len(modified_cv.skills):
                    modified_cv.skills[s.target_item_index] = new_value
                else:
                    logger.warning(f"Invalid skill index for {s.target_item_index}")
            else:
                logger.warning(f"Warning: Skills reorder not implemented yet")

        elif s.section == "experience":
            if s.target_item_index is None or s.target_item_index >= len(modified_cv.experience):
                logger.warning(f"Invalid experience item index {s.target_item_index} - skipping suggestion")
                continue
            if s.target_field == "title":
                modified_cv.experience[s.target_item_index].title = new_value
            elif s.target_field == "company":
                modified_cv.experience[s.target_item_index].company = new_value
            elif s.target_field == "date":
                modified_cv.experience[s.target_item_index].date = new_value
            elif s.target_field == "description":
                if s.target_field_index is None:
                    logger.warning(f"Missing description target field index for experience - skipping suggestion")
                    continue

                desc_list = modified_cv.experience[s.target_item_index].description
                if s.target_field_index >= len(desc_list):
                    logger.warning(f"Description index: {s.target_field_index} out of range - skipping suggestion")
                    continue

                modified_cv.experience[s.target_item_index].description[s.target_field_index] = new_value

        elif s.section == "projects":
            if modified_cv.projects is None:
                logger.warning("User has no project section in CV - skipping suggestion")
                continue

            if s.target_item_index is None or s.target_item_index >= len(modified_cv.projects): # tu nie ma bledu? jaka wartosc ma len(modified_cv.projects) ?
                logger.warning(f"Invalid project item index {s.target_item_index} - skipping suggestion")
                continue

            if s.target_field == "title":
                modified_cv.projects[s.target_item_index].title = new_value
            elif s.target_field == "tools":
                modified_cv.projects[s.target_item_index].tools = new_value
            elif s.target_field == "link":
                modified_cv.projects[s.target_item_index].link = new_value
            elif s.target_field == "description":
                if s.target_field_index is None:
                    logger.warning(f"Missing description item index for project - skipping suggestion")
                    continue

                desc_list = modified_cv.projects[s.target_item_index].description
                if s.target_field_index >= len(desc_list):
                    logger.warning(f"Project description items index {s.target_field_index} is out of range - skipping suggestion")
                    continue

                modified_cv.projects[s.target_item_index].description[s.target_field_index] = new_value

        elif s.section == "languages":
            if s.target_item_index is not None:
                if s.target_item_index < len(modified_cv.languages):
                    modified_cv.languages[s.target_item_index] = new_value
                else:
                    logger.warning(f"Invalid language item index {s.target_item_index}")
            else:
                logger.warning(f"Warning: Languages reorder not implemented yet")

        elif s.section == "education":
            if s.target_item_index is None or s.target_item_index >= len(modified_cv.education):
                logger.warning(f"Invalid education item index: {s.target_item_index}")
                continue

            if s.target_field == "degree":
                modified_cv.education[s.target_item_index].degree = new_value
            elif s.target_field == "field":
                modified_cv.education[s.target_item_index].field = new_value
            elif s.target_field == "school_name":
                modified_cv.education[s.target_item_index].school_name = new_value
            elif s.target_field == "date":
                modified_cv.education[s.target_item_index].date = new_value

    logger.info(f"Changes succesfully applied to CV")
    return modified_cv

