from pathlib import Path
from datetime import datetime
from io import BytesIO
import ast
import base64
import re
import sys

from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa

try:
    from PIL import Image
except ImportError:
    Image = None


def parse_attrs(value):
    """
    Jinja filter: parses a Python-dict-repr string (e.g. the
    "{'e': '123', 'j': '456'}" produced by str(node.attrib)) into a
    real dict for pretty key/value rendering. Returns {} for anything
    that isn't a parseable dict (missing/empty/"-").
    """

    if not value or value == "-":
        return {}

    if isinstance(value, dict):
        return value

    try:
        parsed = ast.literal_eval(str(value))
        if isinstance(parsed, dict):
            return parsed
    except (ValueError, SyntaxError):
        pass

    return {}


def fmt_num(value, decimals=2):
    """Jinja filter: formats a numeric string to N decimals; leaves
    non-numeric values (e.g. "-") untouched."""

    try:
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return value



def format_business_date(value):
    """Formats a YYYYMMDD business date string as DD-Mon-YYYY, matching
    the "Generated On" format. Leaves already-formatted/odd values as-is."""

    value = str(value).strip()

    try:
        return datetime.strptime(value, "%Y%m%d").strftime("%d-%b-%Y")
    except ValueError:
        return value


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
        self.assets_dir = self.base_path / "assets"

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

        self.env.filters["parse_attrs"] = parse_attrs
        self.env.filters["fmt_num"] = fmt_num

    # =====================================================
    # Logo as embedded Base64 data URI
    # =====================================================

    def get_logo_data_uri(self):

        logo_path = self.assets_dir / "anyconnector-logo.png"

        if not logo_path.exists():
            return ""

        try:
            if Image is not None:
                image = Image.open(logo_path).convert("RGBA")
                # Sized generously (print resolution) so it stays crisp
                # at the small ~10mm print height the header uses.
                image.thumbnail((240, 240))
                buffer = BytesIO()
                image.save(buffer, format="PNG", optimize=True)
                data = buffer.getvalue()
            else:
                data = logo_path.read_bytes()
        except Exception:
            data = logo_path.read_bytes()

        encoded = base64.b64encode(data).decode("ascii")

        return f"data:image/png;base64,{encoded}"

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

            "business_date": format_business_date(business_date) if business_date else "",

            "status": store_details.get("status"),

            "generated_on": report_info.get(
                "generated_on",
                datetime.now().strftime(
                    "%d-%b-%Y %I:%M %p"
                )
            ),

            "report_title": report_title
            or f"{integration} Validation Report",

            "app_name": "XML Integration Validator",

            "details": store_details,

            "logo_data_uri": self.get_logo_data_uri()

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