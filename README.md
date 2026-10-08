XML INTEGRATION VALIDATOR
Version : V4.0
=========================================================

OVERVIEW
---------------------------------------------------------

XML Integration Validator is a validation tool developed to
compare CB (CloudBridge) and AC (AnyConnector) XML outputs.

The tool performs automated XML validation and generates
Excel reports, per-store PDF reports, and an interactive
HTML dashboard highlighting differences, missing records,
duplicate records, and zero-value records.

The application helps reduce manual validation effort
and improves accuracy during integration testing.

The tool supports both Single File Comparison and
Bulk Folder Comparison modes, and is available both as a
Windows desktop app (EXE) and as a web application usable
directly from a browser.

---------------------------------------------------------
SUPPORTED INTEGRATIONS
---------------------------------------------------------

1. Payroll Out
2. Payroll Out V2 (exact-match variant, no 0.1 tolerance)
3. Timekeeping Out
4. Food Out (BWW, Arby's, Little Caesars)
5. Vendor Schedule
6. Labor Forecast
7. Schedule Out
8. PMIX Out
9. ERS DPKeys
10. Arby's Sales Out

---------------------------------------------------------
PAYROLL VALIDATION SUPPORT
---------------------------------------------------------

Supported Nodes:

- KEY
- H1
- NV
- JOBCODE
- DAILY
- SHIFT
- WEEKLY
- EXCEPTIONS
- PAY_PERIOD

Validations:

- Value Comparison
- Missing Record Detection
- Missing Attribute Detection
- Duplicate Record Detection
- Zero Value Detection

Payroll Out applies a 0.1 tolerance on numeric hour/pay
attributes (r, wkh, pay, rp, op, dp) so formatting-level or
rounding-level differences aren't reported as mismatches.
Payroll Out V2 uses the same node configuration but with
that tolerance disabled, so every exact difference is
reported, including the ones the 0.1 tolerance would
otherwise hide.

---------------------------------------------------------
TIMEKEEPING VALIDATION SUPPORT
---------------------------------------------------------

Supported Nodes:

- KEY
- H1
- NV
- JOBCODE
- DAILY
- SHIFT
- WEEKLY
- EXCEPTIONS

Validations:

- Value Comparison
- Missing Record Detection
- Missing Attribute Detection
- Duplicate Record Detection
- Zero Value Detection

---------------------------------------------------------
FOOD OUT VALIDATION SUPPORT
---------------------------------------------------------

Supported Client Configurations:

- BWW
- Arby's
- Little Caesars

Supported Nodes:

- INVENTORY_TYPE
- INVENTORY_GROUP
- GLCODE
- INV_DAILY
- INV_NV (BWW Specific)
- DLV
- CM
- INVC
- INVXF
- WASTE

Validations:

- Value Comparison
- Missing Record Detection
- Missing Attribute Detection
- Duplicate Record Detection
- Zero Value Detection

---------------------------------------------------------
VENDOR SCHEDULE VALIDATION SUPPORT
---------------------------------------------------------

Supported Validations:

- Node Level Comparison
- Attribute Level Comparison
- Missing Record Detection
- Missing Attribute Detection
- Duplicate Record Detection
- Zero Value Detection

---------------------------------------------------------
LABOR FORECAST / SCHEDULE OUT / PMIX OUT / ERS DPKEYS
---------------------------------------------------------

Each of these integrations has its own dedicated node
configuration and validation path, and supports:

- Value Comparison
- Missing Record Detection
- Duplicate Record Detection (ERS DPKeys, PMIX Out,
  Schedule Out)
- Zero Value Detection

---------------------------------------------------------
ARBY'S SALES OUT VALIDATION SUPPORT
---------------------------------------------------------

Supported Nodes:

- KEY (KEYS/KEY, keyed by c)
- DK (KEYS/KEY/DK, keyed by parent KEY c + id)
- SD1 (Sales/SD0/SD1, keyed by id)
- PS (Sales/PmtSummary/PS, keyed by cb-posID)
- DSC (Discounts/DiscSummary/DSC, keyed by id)
- LOOKUP (Lookups/Look/L, keyed by category + cd)

Validations:

- Value Comparison (exact match, no tolerance; formatting-only
  differences such as 62.90 vs 62.9 are treated as equal)
- Missing Record Detection (including zero-value KEYs present
  on only one side)
- Missing Attribute Detection
- Duplicate Record Detection (e.g. a KEY repeated in one file)
- Zero Value Detection

The report label "Arby's Sales Out" applies when that option
is selected; the files themselves carry search="AC_POS_SALES".

---------------------------------------------------------
VALIDATION FEATURES
---------------------------------------------------------

- Single File Comparison
- Bulk Folder Comparison
- Multi-file Validation
- Node Level Comparison
- Attribute Level Comparison
- Value Mismatch Detection
- Missing Record Detection
- Missing Attribute Detection
- Duplicate Record Detection
- Zero Value Detection
- Non-comparison statuses (CB/AC file missing, business
  date mismatch) are tracked separately from Pass/Fail so
  they don't get counted as failures

---------------------------------------------------------
REPORT OUTPUT
---------------------------------------------------------

The tool generates, per run:

Master_Comparison_Report.xlsx

Sheets Generated:

1. MASTER_SUMMARY

Overall validation result for each file pair.

2. ALL_DIFFERENCES

All value mismatches detected.

3. ALL_MISSING_RECORDS

Missing records found in CB or AC.

4. ALL_ZERO_VALUES

Records containing zero values.

5. ALL_DUPLICATES

Duplicate records identified during comparison.

Per store, the tool also generates:

- An individual Store_<store>_<date>_Report.xlsx workbook
- A print-friendly PDF validation report (Helvetica,
  ASCII-safe, one page where content allows)

And for the run as a whole:

- An interactive HTML dashboard (KPI summary, Pass/Fail/
  Other filter chips, per-store search, CSV export, dark/
  light theme, and a store-details view linking straight to
  that store's Excel and PDF report)

---------------------------------------------------------
WEB APPLICATION
---------------------------------------------------------

The same comparison pipeline is also available as a web
app (webapp/), so it can be used from a browser with no
install:

https://xml-integration-validator.onrender.com

A permanent sample report (does not expire) is available at:

https://xml-integration-validator.onrender.com/sample

Running a comparison opens the report in a new browser tab
(the upload form stays as-is in the original tab), showing
an animated processing page while the comparison runs in
the background, then switching automatically to the
dashboard once it's ready.

Notes on the hosted (free-tier) web app:

- It goes to sleep after a period of inactivity; the first
  request afterwards can take 20-30 seconds to wake up.
- Only one comparison runs at a time across all users
  (an internal lock protects the report generators, which
  write to fixed file paths rather than per-run paths).
- Generated reports for a run are kept for 24 hours, then
  cleaned up automatically.

---------------------------------------------------------
TECHNOLOGY STACK
---------------------------------------------------------

Programming Language:
- Python

Desktop Framework:
- PySide6

Web Framework:
- Flask
- Gunicorn (production server)

Reporting:
- Pandas
- OpenPyXL
- Jinja2
- xhtml2pdf / ReportLab (PDF reports)
- Pillow (logo/image handling)

Build Tool:
- PyInstaller

Hosting:
- Render (Blueprint deploy via render.yaml)

Version Control:
- Git
- GitHub

---------------------------------------------------------
HOW TO USE (DESKTOP APP)
---------------------------------------------------------

Step 1

Launch:

XMLValidator.exe

Step 2

Select Validation Mode:

- Single File Comparison
- Folder Comparison

Step 3

Select Integration Type:

- Payroll
- Payroll Out V2
- Timekeeping
- Food Out
- Vendor Schedule
- Labor Forecast
- Schedule Out
- PMIX Out
- ERS DPKeys
- Arby's Sales Out

Step 4

Select CB File/Folder

Step 5

Select AC File/Folder

Step 6

Click:

Run Comparison

Step 7

Review the generated Excel report, PDF reports, and HTML
dashboard (opens automatically).

---------------------------------------------------------
HOW TO USE (WEB APP)
---------------------------------------------------------

Step 1

Open https://xml-integration-validator.onrender.com

Step 2

Choose the Integration (and Food Out client, if applicable)

Step 3

Choose Multiple files (folder-style) or Single file pair,
and upload the CB/AC files

Step 4

Click Run Comparison, then review the dashboard, download
the Excel/PDF reports from it

To run the web app locally instead:

    pip install -r requirements-web.txt
    python webapp/app.py
    -> open http://127.0.0.1:5000

---------------------------------------------------------
RECENT ENHANCEMENTS (V4.0)
---------------------------------------------------------

- Added Labor Forecast, Schedule Out, PMIX Out and
  ERS DPKeys integration support
- Added Payroll Out V2 (exact-match, no tolerance)
- Added Arby's Sales Out integration support (KEYS/DK,
  Sales, Payment Summary, Discounts, Lookups)
- Dashboard store details now link to the exact CB/AC XML
  files that were compared ("View" next to each file name)
- Redesigned the HTML dashboard (KPI strip, Pass/Fail/
  Other filter chips, search, CSV export, dark/light theme)
- Redesigned the per-store PDF report (clean single/two
  page enterprise layout, fixed rendering/font bugs)
- Fixed the Failed KPI incorrectly counting CB/AC file
  missing and business-date-mismatch rows as failures
- Added a full web application (Flask) reusing the existing
  comparison pipeline unchanged, deployable for free via a
  Render Blueprint
- Added a permanent, non-expiring sample report link
- Web app: report now opens in a new tab, with an animated
  processing page while the comparison runs in the
  background instead of a blank/loading tab
- Web app: added the AnyConnector logo as the browser tab
  favicon
- Fixed the dashboard title showing a bare "- Validation
  Report" when a CB/AC file missing or business-date
  mismatch row happened to sort first in the store list

---------------------------------------------------------
FUTURE ENHANCEMENTS
---------------------------------------------------------

- Authentication for the web app
- Persistent (non-ephemeral) storage for web-generated
  reports
- Dynamic client selection for more integrations
- Configuration management UI

---------------------------------------------------------
AUTHOR
---------------------------------------------------------

Shivam Chaurasia

Senior QA Analyst

XML Integration Validation Framework

=========================================================
END OF DOCUMENT
=========================================================
