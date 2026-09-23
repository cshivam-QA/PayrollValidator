import sys
import base64
from datetime import datetime
from io import BytesIO
from pathlib import Path
import shutil

from jinja2 import Environment, FileSystemLoader

from dashboard.report_parser import ReportParser

try:
    from PIL import Image
except ImportError:
    Image = None


class DashboardGenerator:
    """
    Generates HTML Dashboard
    from Master_Comparison_Report.xlsx
    """

    def __init__(self, report_path, store_report_paths=None):
        self.report_path = Path(report_path)
        self.store_report_paths = store_report_paths or {}

        if getattr(sys, "frozen", False):
            self.base_path = Path(sys._MEIPASS) / "dashboard"
        else:
            self.base_path = Path(__file__).resolve().parent

        self.template_dir = self.base_path / "templates"
        self.assets_dir = self.base_path / "assets"

        # Output folder
        if getattr(sys, "frozen", False):
            # EXE ke paas reports folder banega
            output_root = Path(sys.executable).parent
        else:
            # Development mode
            output_root = Path(__file__).resolve().parent.parent.parent

        self.output_dir = output_root / "reports"
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir)
        )

    # ======================================================
    # Copy Assets
    # ======================================================

    def copy_assets(self):

        destination = self.output_dir / "assets"

        destination.mkdir(
            parents=True,
            exist_ok=True
        )

        assets = [
           "style.css",
           "dashboard.js",
           "anyconnector-logo.png"
]

        for asset in assets:

            source = self.assets_dir / asset

            if source.exists():

                shutil.copy2(
                    source,
                    destination / asset
                )

    # ======================================================
    # Logo as embedded Base64 data URI
    # (keeps the generated dashboard a single, self-contained
    # file that opens identically on any machine, with no
    # dependency on a sibling "assets" folder)
    # ======================================================

    def get_logo_data_uri(self):

        logo_path = self.assets_dir / "anyconnector-logo.png"

        if not logo_path.exists():
            return ""

        try:
            if Image is not None:
                image = Image.open(logo_path).convert("RGBA")
                image.thumbnail((128, 128))
                buffer = BytesIO()
                image.save(buffer, format="PNG", optimize=True)
                data = buffer.getvalue()
            else:
                data = logo_path.read_bytes()
        except Exception:
            data = logo_path.read_bytes()

        encoded = base64.b64encode(data).decode("ascii")

        return f"data:image/png;base64,{encoded}"

    # ======================================================
    # Run context (business date range covered by this report)
    # ======================================================

    def format_business_date(self, value):

        value = str(value).strip()

        try:
            return datetime.strptime(value, "%Y%m%d").strftime("%d-%b-%Y")
        except ValueError:
            return value

    def get_run_date_range(self, stores):

        dates = set()

        for store in stores:
            for key in ("CB Date", "AC Date"):
                value = store.get(key)
                if value:
                    dates.add(str(value))

        if not dates:
            return ""

        sorted_dates = sorted(dates)
        formatted = [self.format_business_date(d) for d in sorted_dates]

        if len(formatted) == 1:
            return formatted[0]

        return f"{formatted[0]} – {formatted[-1]}"

    # ======================================================
    # Generate Dashboard
    # ======================================================

    def generate(self):

        parser = ReportParser(self.report_path)

        dashboard_data = parser.parse(
            self.store_report_paths
)

        template = self.env.get_template(
            "dashboard.html"
        )

        html = template.render(
            stores=dashboard_data["stores"],
            summary=dashboard_data["summary"],
            charts=dashboard_data["charts"],
            details=dashboard_data["details"],
            report_title=dashboard_data["report_title"],
            report_info=dashboard_data["report_info"],
            logo_data_uri=self.get_logo_data_uri(),
            run_date_range=self.get_run_date_range(dashboard_data["stores"])
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (
            self.output_dir
            / f"{self.report_path.stem}.html"
        )

        output_file.write_text(
            html,
            encoding="utf-8"
        )

        self.copy_assets()

        print()
        print("=" * 60)
        print(" Dashboard Generated Successfully ")
        print("=" * 60)
        print()

        print(f"Location : {output_file}")
        print()

        return output_file
    # ======================================================
# Run Dashboard Generator
# ======================================================

if __name__ == "__main__":

    report_path = (
        Path(__file__).resolve().parent.parent
        / "dist"
        / "reports"
        / "Master_Comparison_Report.xlsx"
    )

    if not report_path.exists():
        print(f"Report not found: {report_path}")
    else:
        generator = DashboardGenerator(report_path)
        generator.generate()