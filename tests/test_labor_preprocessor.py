import xml.etree.ElementTree as ET

from comparator import compare_nodes
from labor_preprocessor import aggregate_weekly_by_employee_job


def make_node(attrib):
    return ET.Element("TM1", attrib)


def test_merges_split_pay_rate_rows_for_same_employee_job_date():
    # A mid-week pay-rate change: same e/j/dt, different "r".
    nodes = [
        make_node({"e": "100312414", "j": "50005", "dt": "20261011", "r": "29.26",
                   "rh": "44.97", "wkh": "44.97", "rp": "1315.72", "pay": "1315.72"}),
        make_node({"e": "100312414", "j": "50005", "dt": "20261011", "r": "33.65",
                   "rh": "10.22", "wkh": "10.22", "rp": "298.94", "pay": "298.94"}),
    ]

    merged = aggregate_weekly_by_employee_job(nodes)

    assert len(merged) == 1
    attrib = merged[0].attrib
    assert attrib["rh"] == "55.19"
    assert attrib["wkh"] == "55.19"
    assert attrib["rp"] == "1614.66"
    assert attrib["pay"] == "1614.66"
    # The rate itself isn't summable; it's left as whichever record came first.
    assert attrib["r"] == "29.26"


def test_tip_credit_and_tips_are_summed_too():
    nodes = [
        make_node({"e": "1", "j": "2", "dt": "20261011", "pay": "10.00", "tcr": "50.00"}),
        make_node({"e": "1", "j": "2", "dt": "20261011", "pay": "5.00", "tcr": "20.00", "tips": "3.00"}),
    ]

    merged = aggregate_weekly_by_employee_job(nodes)

    assert merged[0].attrib["pay"] == "15.0"
    assert merged[0].attrib["tcr"] == "70.0"
    assert merged[0].attrib["tips"] == "3.0"


def test_single_record_is_returned_unchanged():
    node = make_node({"e": "1", "j": "2", "dt": "20261011", "pay": "10.00"})

    merged = aggregate_weekly_by_employee_job([node])

    assert merged == [node]


def test_different_employee_job_or_date_are_not_merged():
    nodes = [
        make_node({"e": "1", "j": "2", "dt": "20261011", "pay": "10.00"}),
        make_node({"e": "1", "j": "9", "dt": "20261011", "pay": "20.00"}),
        make_node({"e": "9", "j": "2", "dt": "20261011", "pay": "30.00"}),
        make_node({"e": "1", "j": "2", "dt": "20261012", "pay": "40.00"}),
    ]

    merged = aggregate_weekly_by_employee_job(nodes)

    assert len(merged) == 4


def test_split_rate_weekly_rows_no_longer_report_as_duplicate_or_mismatch():
    # Reproduces the reported bug: CB splits a WEEKLY record across two pay
    # rates for the same employee/job/date; AC already reports one combined
    # total. Before the fix, WEEKLY's key_fields (e/j/dt, no rate) made the
    # second CB row look like a duplicate of the first, dropping its hours/
    # pay from the comparison and producing false mismatches against AC's
    # total.
    cb_nodes = [
        make_node({"e": "100312414", "j": "50005", "dt": "20261011", "r": "29.26",
                   "rh": "44.97", "wkh": "44.97", "rp": "1315.72", "pay": "1315.72"}),
        make_node({"e": "100312414", "j": "50005", "dt": "20261011", "r": "33.65",
                   "rh": "10.22", "wkh": "10.22", "rp": "298.94", "pay": "298.94"}),
    ]
    ac_nodes = [
        make_node({"e": "100312414", "j": "50005", "dt": "20261011", "r": "29.26",
                   "rh": "55.19", "wkh": "55.19", "rp": "1614.66", "pay": "1614.66"}),
    ]

    cb_nodes = aggregate_weekly_by_employee_job(cb_nodes)
    ac_nodes = aggregate_weekly_by_employee_job(ac_nodes)

    differences, zero_values, missing_records, duplicate_records = compare_nodes(
        cb_nodes, ac_nodes, "WEEKLY", "Poll/Labor/TM0(type=WEEKLY)/TM1", ["e", "j", "dt"]
    )

    assert differences == []
    assert duplicate_records == []
    assert missing_records == []
