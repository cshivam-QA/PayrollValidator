from report_parser import ReportParser

parser = ReportParser(r"data\Master_Comparison_Report.xlsx")   # <-- apna path

data = parser.parse()

print("\nDashboard Keys")
print(data.keys())

print("\nStores")
print(data["stores"])

print("\nSummary")
print(data["summary"])

print("\nStore Details")
print(data["details"])

print("\nDifferences Count")
print(
    len(
        data["details"]["00050"]["differences"]
    )
)