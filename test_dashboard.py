from dashboard.dashboard_generator import generate_dashboard

generate_dashboard(
    {
        "files_compared": 15,
        "pass_count": 10,
        "fail_count": 5,
        "difference_count": 27,
        "missing_count": 4,
        "duplicate_count": 1,
        "zero_count": 8,
        "integration": "Payroll Out",
        "business_date": "20260621",
        "generated_on": "12 Jul 2026 05:45 PM",
    }
)

print("Dashboard Generated Successfully")
