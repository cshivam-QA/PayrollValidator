import pandas as pd
import os


def generate_master_report(
        summary,
        differences,
        missing_records,
        zero_values,
        duplicate_records):

    os.makedirs(
        "reports",
        exist_ok=True
    )

    output_file = (
        "reports/"
        "Master_Comparison_Report.xlsx"
    )

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        pd.DataFrame(
            summary
        ).to_excel(
            writer,
            sheet_name="MASTER_SUMMARY",
            index=False
        )

        pd.DataFrame(
            differences
        ).to_excel(
            writer,
            sheet_name="ALL_DIFFERENCES",
            index=False
        )

        pd.DataFrame(
            missing_records
        ).to_excel(
            writer,
            sheet_name="ALL_MISSING_RECORDS",
            index=False
        )

        pd.DataFrame(
            zero_values
        ).to_excel(
            writer,
            sheet_name="ALL_ZERO_VALUES",
            index=False
        )

        pd.DataFrame(
            duplicate_records
        ).to_excel(
            writer,
            sheet_name="ALL_DUPLICATES",
            index=False
        )

    print()
    print(
        "Master Report Generated"
    )

    print(
        output_file
    )