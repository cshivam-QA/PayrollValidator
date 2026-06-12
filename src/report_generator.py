import pandas as pd
import os


def generate_reports(differences, zero_values):

    os.makedirs("../reports", exist_ok=True)

    diff_df = pd.DataFrame(differences)

    zero_df = pd.DataFrame(zero_values)

    diff_df.to_csv(
        "../reports/differences.csv",
        index=False
    )

    zero_df.to_csv(
        "../reports/zero_values.csv",
        index=False
    )

    print("\nReports Generated Successfully")
    print("reports/differences.csv")
    print("reports/zero_values.csv")