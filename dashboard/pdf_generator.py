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



def _clean(value):
    """Cell text for the PDF: None/NaN (pandas fills columns a row doesn't
    have with NaN) become ""."""

    if value is None:
        return ""
    if isinstance(value, float) and value != value:
        return ""
    text = str(value).strip()
    return "" if text.lower() == "nan" else text


def _node_of(row):
    # Generic comparator rows use "Node"; ERS DPKeys rows use "Type".
    return _clean(row.get("Node")) or _clean(row.get("Type")) or "-"


def _record_key_of(row):
    key = _clean(row.get("Key"))
    dk_id = _clean(row.get("DK ID"))

    if key:
        return f"{key} / DK {dk_id}" if dk_id else key

    # Labor Forecast rows have no "Key"; they're identified by
    # Section / NV / DK ID instead.
    parts = [_clean(row.get("Section")), _clean(row.get("NV"))]
    if dk_id:
        parts.append(f"DK {dk_id}")
    return " / ".join(p for p in parts if p) or "-"


def _side_from_details(details):
    # ERS DPKeys describes sides in text, e.g. "KEY missing in AC".
    match = re.search(r"\b(?:in|found in)\s+(AC|CB)\b", _clean(details))
    return match.group(1) if match else ""


def _group_by_node(rows):
    groups = {}
    for row in rows:
        groups.setdefault(row["node"], []).append(row)
    return [
        {"node": node, "rows": sorted(items, key=lambda r: r["key"])}
        for node, items in groups.items()
    ]


def build_report_sections(details):
    """Normalizes the per-store differences / missing / duplicate / zero
    rows (whose columns differ between integrations) into one shape the PDF
    template can lay out as compact tables, grouped by node."""

    differences = [
        {
            "node": _node_of(row),
            "key": _record_key_of(row),
            "attribute": _clean(row.get("Attribute")) or _clean(row.get("Field")) or "-",
            "cb": _clean(row.get("CB Value")) or "-",
            "ac": _clean(row.get("AC Value")) or "-",
            "path": _clean(row.get("Path")),
        }
        for row in details.get("differences") or []
    ]

    diff_groups = _group_by_node(differences)
    for group in diff_groups:
        group["path"] = next((r["path"] for r in group["rows"] if r["path"]), "")
        previous_key, band = None, 1
        for row in group["rows"]:
            row["first_of_key"] = row["key"] != previous_key
            if row["first_of_key"]:
                band = 1 - band
            row["band"] = band
            previous_key = row["key"]

    missing = []
    for row in details.get("missing") or []:
        missing_in = _clean(row.get("Missing In")) or _side_from_details(row.get("Details"))
        key = _record_key_of(row)
        attrs = parse_attrs(
            row.get("CB Attributes") if missing_in == "AC" else row.get("AC Attributes")
        )
        values = [
            f"{name} = {value}"
            for name, value in attrs.items()
            # Skip helper attributes added for keying, and any attribute
            # that just repeats the record key shown in its own column.
            if not str(name).startswith("_") and _clean(value) != key
        ]
        missing.append(
            {
                "node": _node_of(row),
                "key": key,
                "missing_in": missing_in or "-",
                "attr_text": ",   ".join(values) or "-",
            }
        )

    zero_values = [
        {
            "node": _node_of(row),
            "key": _record_key_of(row),
            "attribute": _clean(row.get("Attribute")) or "-",
            "value": _clean(row.get("Value")) or "-",
            "side": _clean(row.get("Side")) or "-",
        }
        for row in details.get("zero_values") or []
    ]

    duplicates = [
        {
            "node": _node_of(row),
            "key": _record_key_of(row),
            "side": _clean(row.get("Side")) or _side_from_details(row.get("Details")) or "-",
        }
        for row in details.get("duplicates") or []
    ]

    return {
        "diff_groups": diff_groups,
        "diff_count": len(differences),
        "missing_groups": _group_by_node(missing),
        "missing_count": len(missing),
        "zero_rows": sorted(zero_values, key=lambda r: (r["node"], r["key"])),
        "duplicate_rows": sorted(duplicates, key=lambda r: (r["node"], r["key"])),
    }


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

            "report": build_report_sections(store_details),

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