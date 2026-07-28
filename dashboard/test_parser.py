from pathlib import Path
from report_parser import ReportParser


def main():
    report_path = (
        Path(__file__).resolve().parent.parent
        / "dist"
        / "reports"
        / "Master_Comparison_Report.xlsx"
    )

    parser = ReportParser(report_path)

    try:
        data = parser.parse()

        stores = data["stores"]

        print("=" * 60)
        print(" XML VALIDATOR DASHBOARD PARSER TEST ")
        print("=" * 60)

        print(f"\nTotal Stores : {len(stores)}\n")

        if stores:
            print("First Store Record\n")

            for key, value in stores[0].items():
                print(f"{key:<20}: {value}")

        print("\n✅ Parser Test Successful!")

    except Exception as e:
        print(f"\n❌ Error : {e}")


if __name__ == "__main__":
    main()