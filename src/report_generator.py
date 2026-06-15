import os
import pandas as pd


def generate_report(
        summary,
        root_info,
        differences,
        missing_records,
        zero_values,
        duplicate_records):

    os.makedirs("reports", exist_ok=True)

    output_file = (
        "reports/"
        "Payroll_Comparison_Report.xlsx"
    )

    with pd.ExcelWriter(
            output_file,
            engine="openpyxl") as writer:

        pd.DataFrame(
            root_info
        ).to_excel(
            writer,
            sheet_name="ROOT_INFO",
            index=False
        )

        pd.DataFrame(
            summary
        ).to_excel(
            writer,
            sheet_name="SUMMARY",
            index=False
        )

        pd.DataFrame(
            differences
        ).to_excel(
            writer,
            sheet_name="DIFFERENCES",
            index=False
        )

        pd.DataFrame(
            missing_records
        ).to_excel(
            writer,
            sheet_name="MISSING_RECORDS",
            index=False
        )

        pd.DataFrame(
            zero_values
        ).to_excel(
            writer,
            sheet_name="ZERO_VALUES",
            index=False
        )

        pd.DataFrame(
            duplicate_records
        ).to_excel(
            writer,
            sheet_name="DUPLICATE_RECORDS",
            index=False
        )

    print()
    print("Report Generated Successfully")
    print(output_file)