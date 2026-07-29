from pathlib import Path
import sys
import pandas as pd

from dashboard.pdf_generator import PDFGenerator


def _filter(df, store, business_date):
    if df.empty:
        return df

    if "Store" not in df.columns:
        return df.iloc[0:0]

    filtered = df[df["Store"].astype(str) == str(store)]

    if "Date" in filtered.columns:
        filtered = filtered[
            filtered["Date"].astype(str) == str(business_date)
        ]

    return filtered


def generate_store_reports(
    summary,
    differences,
    missing_records,
    zero_values,
    duplicate_records,
):
    """
    Generate one Excel report and one PDF report per Store + Business Date.
    """

    # Output folder
    if getattr(sys, "frozen", False):
        base_output = Path(sys.executable).parent / "reports"
    else:
        base_output = Path(__file__).resolve().parent.parent / "dist" / "reports"

    base_output.mkdir(parents=True, exist_ok=True)

    output_folder = base_output / "StoreReports"
    output_folder.mkdir(parents=True, exist_ok=True)

    summary_df = pd.DataFrame(summary)
    diff_df = pd.DataFrame(differences)
    missing_df = pd.DataFrame(missing_records)
    zero_df = pd.DataFrame(zero_values)
    duplicate_df = pd.DataFrame(duplicate_records)

    if summary_df.empty:
        print("No store reports generated.")
        return {}

    generated = set()
    report_paths = {}

    pdf_generator = PDFGenerator()

    for _, row in summary_df.iterrows():

        store = str(row.get("Store", "")).strip()

        business_date = str(row.get("CB Date", "")).strip()

        if not business_date:
            business_date = str(row.get("AC Date", "")).strip()

        key = f"{store}|{business_date}"

        if key in generated:
            continue

        generated.add(key)

        file_name = f"Store_{store}_{business_date}_Report.xlsx"

        file_path = output_folder / file_name

        # Initialize report paths
        report_paths[key] = {
            "excel": str(file_path),
            "pdf": "",
        }

        store_summary = summary_df[
            (summary_df["Store"].astype(str) == store)
            &
            (
                (summary_df["CB Date"].astype(str) == business_date)
                |
                (summary_df["AC Date"].astype(str) == business_date)
            )
        ]

        store_diff = _filter(diff_df, store, business_date)
        store_missing = _filter(missing_df, store, business_date)
        store_zero = _filter(zero_df, store, business_date)
        store_duplicate = _filter(duplicate_df, store, business_date)

        store_details = {
            "store": store,
            "integration": row.get("Integration"),
            "status": row.get("Status"),
            "cb_date": row.get("CB Date"),
            "ac_date": row.get("AC Date"),
            "cb_file": row.get("CB File"),
            "ac_file": row.get("AC File"),
            "differences": store_diff.to_dict("records"),
            "missing": store_missing.to_dict("records"),
            "duplicates": store_duplicate.to_dict("records"),
            "zero_values": store_zero.to_dict("records"),
        }

        report_info = {
            "generated_on": pd.Timestamp.now().strftime(
                "%d-%b-%Y %I:%M %p"
            ),
            "comparison": row.get("Integration"),
        }

        report_title = (
            f"{row.get('Integration')} Validation Report"
        )

        # Excel Report
        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:

            store_summary.to_excel(
                writer,
                sheet_name="SUMMARY",
                index=False,
            )

            store_diff.to_excel(
                writer,
                sheet_name="DIFFERENCES",
                index=False,
            )

            store_missing.to_excel(
                writer,
                sheet_name="MISSING_RECORDS",
                index=False,
            )

            store_zero.to_excel(
                writer,
                sheet_name="ZERO_VALUES",
                index=False,
            )

            store_duplicate.to_excel(
                writer,
                sheet_name="DUPLICATES",
                index=False,
            )

        # PDF Report
        pdf_path = pdf_generator.generate_store_pdf(
            store_details=store_details,
            report_info=report_info,
            report_title=report_title,
        )

        report_paths[key]["pdf"] = str(pdf_path)

    print(f"Generated {len(report_paths)} Store Reports")

    return report_paths