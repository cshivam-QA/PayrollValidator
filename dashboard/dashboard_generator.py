from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from datetime import datetime


def generate_dashboard(summary_data):

    template_dir = Path(__file__).parent / "templates"

    env = Environment(loader=FileSystemLoader(template_dir))

    template = env.get_template("dashboard.html")

    html = template.render(summary_data)

    output_path = Path("reports") / "dashboard.html"

    output_path.parent.mkdir(exist_ok=True)

    output_path.write_text(html, encoding="utf-8")

    return str(output_path)
