import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dashboard.pdf_generator import build_report_sections  # noqa: E402

NaN = float("nan")


def test_generic_differences_are_grouped_by_node_and_key():
    report = build_report_sections({
        "differences": [
            {"Node": "PAY_PERIOD", "Path": "P/TM1", "Key": "k1", "Attribute": "rh", "CB Value": "1", "AC Value": "2"},
            {"Node": "PAY_PERIOD", "Path": "P/TM1", "Key": "k1", "Attribute": "pay", "CB Value": "3", "AC Value": "4"},
            {"Node": "DAILY", "Path": "D/TM1", "Key": "k2", "Attribute": "hrs", "CB Value": "8", "AC Value": "7"},
        ]
    })

    assert report["diff_count"] == 3
    pay_period, daily = report["diff_groups"]
    assert (pay_period["node"], pay_period["path"]) == ("PAY_PERIOD", "P/TM1")
    assert [r["first_of_key"] for r in pay_period["rows"]] == [True, False]
    assert daily["rows"][0]["attribute"] == "hrs"


def test_missing_values_drop_the_repeated_key_and_helper_attributes():
    report = build_report_sections({
        "missing": [
            {"Node": "KEY", "Key": "deliveryFeeAmt", "Missing In": "AC",
             "CB Attributes": "{'c': 'deliveryFeeAmt', 'v': '0.00'}", "AC Attributes": NaN},
            {"Node": "DK", "Key": "adjGrossSales_43", "Missing In": "CB", "CB Attributes": NaN,
             "AC Attributes": "{'id': '43', 'v': '5', '_key': 'adjGrossSales'}"},
        ]
    })

    rows = {r["key"]: r for g in report["missing_groups"] for r in g["rows"]}
    assert rows["deliveryFeeAmt"]["attr_text"] == "v = 0.00"
    assert rows["deliveryFeeAmt"]["missing_in"] == "AC"
    assert rows["adjGrossSales_43"]["attr_text"] == "id = 43,   v = 5"


def test_ers_dpkeys_rows_use_type_field_and_details():
    report = build_report_sections({
        "differences": [{"Type": "DK", "Key": "netSales", "DK ID": "43", "Field": "v", "CB Value": "1", "AC Value": "2"},
                        {"Type": "KEY", "Key": "netSales", "DK ID": NaN, "Field": "v", "CB Value": "3", "AC Value": "4"}],
        "missing": [{"Type": "KEY", "Key": "giftCardSold", "DK ID": NaN, "Details": "KEY missing in CB"}],
        "duplicates": [{"Type": "KEY", "Key": "adjGrossSales", "Details": "Duplicate KEY found in AC"}],
    })

    keys = {g["node"]: g["rows"][0]["key"] for g in report["diff_groups"]}
    assert keys == {"DK": "netSales / DK 43", "KEY": "netSales"}
    assert report["missing_groups"][0]["rows"][0]["missing_in"] == "CB"
    assert report["duplicate_rows"][0]["side"] == "AC"


def test_labor_forecast_rows_without_key_use_section_nv_and_dk():
    report = build_report_sections({
        "missing": [{"Node": "DK", "Section": "SALES", "NV": "Lunch", "DK ID": "9", "Missing In": "CB"}],
    })

    assert report["missing_groups"][0]["rows"][0]["key"] == "SALES / Lunch / DK 9"


def test_empty_details_produce_no_sections():
    report = build_report_sections({})

    assert report["diff_count"] == 0 and report["missing_count"] == 0
    assert report["duplicate_rows"] == [] and report["zero_rows"] == []


def test_generated_pdf_keeps_header_and_footer_on_every_page(tmp_path, monkeypatch):
    # xhtml2pdf silently drops the running header (no error) when its
    # content outgrows the header frame, so check the rendered text.
    from pypdf import PdfReader

    from dashboard.pdf_generator import PDFGenerator

    monkeypatch.chdir(tmp_path)
    details = {
        "store": "00999", "cb_date": "20260726", "status": "FAIL",
        "cb_file": "cb.xml", "ac_file": "ac.xml",
        "differences": [
            {"Node": "PAY_PERIOD", "Path": "P/TM1", "Key": f"k{i:03d}", "Attribute": "pay",
             "CB Value": "1.00", "AC Value": "2.00"}
            for i in range(80)
        ],
    }

    pdf = PDFGenerator().generate_store_pdf(
        details, {"generated_on": "08-Oct-2026 05:53 PM"}, report_title="Payroll Out Validation Report"
    )

    pages = PdfReader(str(pdf)).pages
    assert len(pages) > 1
    for number, page in enumerate(pages, start=1):
        text = page.extract_text()
        assert "Payroll Out Validation Report" in text
        assert f"Page {number} of {len(pages)}" in text
