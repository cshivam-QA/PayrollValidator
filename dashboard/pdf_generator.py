from pathlib import Path
from datetime import datetime
import re
import sys

from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa


class PDFGenerator:
    """
    Generates Store Validation PDF Reports
    """

    def __init__(self):

        if getattr(sys, "frozen", False):
            self.base_path = Path(sys._MEIPASS) / "dashboard"
            output_root = Path(sys.executable).parent
        else:
            self.base_path = Path(__file__).resolve().parent
            output_root = Path.cwd()

        self.template_dir = self.base_path / "templates"

        self.output_dir = (
            output_root
            / "reports"
            / "PDF Reports"
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.env = Environment(
            loader=FileSystemLoader(self.template_dir)
        )

    # =====================================================
    # HTML -> PDF
    # =====================================================

    def html_to_pdf(self, html, output_file):

        with open(output_file, "wb") as pdf:

            pisa.CreatePDF(
                src=html,
                dest=pdf
            )

        return output_file

    # =====================================================
    # Generic PDF Generator
    # =====================================================

    def generate(
        self,
        template_name,
        context,
        output_filename,
    ):

        template = self.env.get_template(
            template_name
        )

        html = template.render(
            **context
        )

        output_file = (
            self.output_dir
            / output_filename
        )

        self.html_to_pdf(
            html,
            output_file
        )

        return output_file

    # =====================================================
    # Helpers
    # =====================================================

    def sanitize_filename(self, value):

        value = str(value)

        value = value.replace(" ", "")

        value = re.sub(
            r'[^A-Za-z0-9_-]',
            "",
            value
        )

        return value

    # =====================================================
    # Store PDF
    # =====================================================

    def generate_store_pdf(
        self,
        store_details,
        report_info,
        report_title=None
    ):

        integration = (
            store_details.get("integration")
            or report_info.get("comparison")
            or "Integration"
        )

        business_date = (
            store_details.get("cb_date")
            or store_details.get("ac_date")
            or ""
        )

        context = {

            "integration": integration,

            "store": store_details.get("store"),

            "business_date": business_date,

            "status": store_details.get("status"),

            "generated_on": report_info.get(
                "generated_on",
                datetime.now().strftime(
                    "%d-%b-%Y %I:%M %p"
                )
            ),

            "report_title": report_title
            or f"{integration} Validation Report",

            "details": store_details

        }

        filename = (
            f"{self.sanitize_filename(integration)}"
            f"_Store{self.sanitize_filename(store_details.get('store'))}"
            f"_{self.sanitize_filename(business_date)}"
            f"_Report.pdf"
        )

        return self.generate(

            template_name="store_details_pdf_v2.html",

            context=context,

            output_filename=filename

        )