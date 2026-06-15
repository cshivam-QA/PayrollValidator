import pandas as pd
import os


def generate_master_report(summary):

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

    print()
    print(
        "Master Report Generated"
    )

    print(
        output_file
    )