from pathlib import Path
from collections import defaultdict

from openpyxl import load_workbook


class ReportParser:
    """
    Parses Master_Comparison_Report.xlsx
    and prepares dashboard data.
    """

    REQUIRED_SHEETS = [
        "MASTER_SUMMARY",
        "ALL_DIFFERENCES",
        "ALL_MISSING_RECORDS",
        "ALL_DUPLICATES",
        "ALL_ZERO_VALUES",
    ]

    def __init__(self, report_path):

        self.report_path = Path(report_path)

        self.workbook = None

        self.summary_sheet = None
        self.difference_sheet = None
        self.missing_sheet = None
        self.duplicate_sheet = None
        self.zero_sheet = None

    # ==========================================================
    # Validation
    # ==========================================================

    def validate_report(self):

        if not self.report_path.exists():
            raise FileNotFoundError(
                f"Report not found : {self.report_path}"
            )

    def validate_sheets(self):

        missing = [
            sheet
            for sheet in self.REQUIRED_SHEETS
            if sheet not in self.workbook.sheetnames
        ]

        if missing:

            raise ValueError(
                f"Missing worksheet(s): {', '.join(missing)}"
            )

    # ==========================================================
    # Workbook
    # ==========================================================

    def load_workbook(self):

        self.validate_report()

        self.workbook = load_workbook(
            self.report_path,
            data_only=True
        )

        self.validate_sheets()

        self.summary_sheet = self.workbook["MASTER_SUMMARY"]
        self.difference_sheet = self.workbook["ALL_DIFFERENCES"]
        self.missing_sheet = self.workbook["ALL_MISSING_RECORDS"]
        self.duplicate_sheet = self.workbook["ALL_DUPLICATES"]
        self.zero_sheet = self.workbook["ALL_ZERO_VALUES"]

    # ==========================================================
    # Store Summary
    # ==========================================================

    def get_store_summary(self):

        rows = list(
            self.summary_sheet.iter_rows(
                min_row=2,
                values_only=True
            )
        )

        headers = [
            cell.value
            for cell in self.summary_sheet[1]
        ]

        stores = []

        for row in rows:

            if all(value is None for value in row):
                continue

            stores.append(
                dict(zip(headers, row))
            )

        return stores

    # ==========================================================
    # Summary Metrics
    # ==========================================================

    def get_summary(self, stores):

        total_stores = len(stores)

        passed = sum(
            1
            for store in stores
            if str(store["Status"]).upper() == "PASS"
        )

        failed = total_stores - passed

        total_differences = sum(
            int(store["Differences"] or 0)
            for store in stores
        )

        total_missing = sum(
            int(store["Missing Records"] or 0)
            for store in stores
        )

        total_duplicates = sum(
            int(store["Duplicates"] or 0)
            for store in stores
        )

        total_zero_values = sum(
            int(store["Zero Values"] or 0)
            for store in stores
        )

        accuracy = round(
            (passed / total_stores) * 100,
            2
        ) if total_stores else 0

        return {

            "total_stores": total_stores,

            "passed": passed,

            "failed": failed,

            "accuracy": accuracy,

            "differences": total_differences,

            "missing": total_missing,

            "duplicates": total_duplicates,

            "zero_values": total_zero_values

        }

    # ==========================================================
    # Dynamic Sheet Reader
    # ==========================================================

    def read_sheet_records(self, worksheet):

        if worksheet.max_row <= 1:
            return []

        headers = [
            cell.value
            for cell in worksheet[1]
        ]

        if not any(headers):
            return []

        records = []

        for row in worksheet.iter_rows(
            min_row=2,
            values_only=True
        ):

            if all(value is None for value in row):
                continue

            records.append(
                dict(zip(headers, row))
            )

        return records

    # ==========================================================
    # Store Details
    # ==========================================================

    def get_store_details(self):

        details = defaultdict(
            lambda: {
                "differences": [],
                "missing": [],
                "duplicates": [],
                "zero_values": []
            }
        )

        differences = self.read_sheet_records(
            self.difference_sheet
        )

        missing = self.read_sheet_records(
            self.missing_sheet
        )

        duplicates = self.read_sheet_records(
            self.duplicate_sheet
        )

        zero_values = self.read_sheet_records(
            self.zero_sheet
        )
                # ------------------------------------------
        # Differences
        # ------------------------------------------

        for record in differences:

            store = str(
                record.get("Store", "")
            ).strip()

            if not store:
                continue

            details[store]["differences"].append(
                record
            )

        # ------------------------------------------
        # Missing Records
        # ------------------------------------------

        for record in missing:

            store = str(
                record.get("Store", "")
            ).strip()

            if not store:
                continue

            details[store]["missing"].append(
                record
            )

        # ------------------------------------------
        # Duplicate Records
        # ------------------------------------------

        for record in duplicates:

            store = str(
                record.get("Store", "")
            ).strip()

            if not store:
                continue

            details[store]["duplicates"].append(
                record
            )

        # ------------------------------------------
        # Zero Values
        # ------------------------------------------

        for record in zero_values:

            store = str(
                record.get("Store", "")
            ).strip()

            if not store:
                continue

            details[store]["zero_values"].append(
                record
            )

        return dict(details)

    # ==========================================================
    # Chart Data
    # ==========================================================

    def get_chart_data(self, summary):

        return {

            "pass_fail": {

                "labels": [
                    "Passed",
                    "Failed"
                ],

                "values": [
                    summary["passed"],
                    summary["failed"]
                ]

            },

            "issue_distribution": {

                "labels": [
                    "Differences",
                    "Missing",
                    "Duplicates",
                    "Zero Values"
                ],

                "values": [

                    summary["differences"],
                    summary["missing"],
                    summary["duplicates"],
                    summary["zero_values"]

                ]

            }

        }

    # ==========================================================
    # Parser
    # ==========================================================

    def parse(self):

        self.load_workbook()

        stores = self.get_store_summary()

        summary = self.get_summary(
            stores
        )

        charts = self.get_chart_data(
            summary
        )

        details = self.get_store_details()

        return {

            "stores": stores,

            "summary": summary,

            "charts": charts,

            "details": details

        }