import xml.etree.ElementTree as ET

from comparator import compare_nodes


def make_node(tag, attrib):
    return ET.Element(tag, attrib)


def test_matching_cb_and_ac_values_produce_no_differences():
    cb_nodes = [make_node("DAILY", {"e": "100", "hrs": "8.0"})]
    ac_nodes = [make_node("DAILY", {"e": "100", "hrs": "8.0"})]

    differences, zero_values, missing_records, duplicate_records = compare_nodes(
        cb_nodes, ac_nodes, "DAILY", "Root/DAILY", ["e"]
    )

    assert differences == []
    assert zero_values == []
    assert missing_records == []
    assert duplicate_records == []


def test_actual_numeric_value_difference_is_reported():
    cb_nodes = [make_node("DAILY", {"e": "100", "hrs": "8.0"})]
    ac_nodes = [make_node("DAILY", {"e": "100", "hrs": "7.5"})]

    differences, _, _, _ = compare_nodes(
        cb_nodes, ac_nodes, "DAILY", "Root/DAILY", ["e"]
    )

    assert len(differences) == 1
    assert differences[0]["Attribute"] == "hrs"
    assert differences[0]["CB Value"] == "8.0"
    assert differences[0]["AC Value"] == "7.5"


def test_formatting_only_difference_is_not_reported():
    # 62.9000 vs 62.9 is the same number, just formatted differently.
    cb_nodes = [make_node("DAILY", {"e": "100", "hrs": "62.9000"})]
    ac_nodes = [make_node("DAILY", {"e": "100", "hrs": "62.9"})]

    differences, _, _, _ = compare_nodes(
        cb_nodes, ac_nodes, "DAILY", "Root/DAILY", ["e"]
    )

    assert differences == []


def test_pay_difference_within_tolerance_is_not_reported():
    # "pay" allows up to 0.1 difference before it counts as a mismatch.
    cb_nodes = [make_node("PAY_PERIOD", {"e": "100", "pay": "262.66"})]
    ac_nodes = [make_node("PAY_PERIOD", {"e": "100", "pay": "262.65"})]

    differences, _, _, _ = compare_nodes(
        cb_nodes, ac_nodes, "PAY_PERIOD", "Root/PAY_PERIOD", ["e"]
    )

    assert differences == []


def test_pay_difference_beyond_tolerance_is_reported():
    cb_nodes = [make_node("PAY_PERIOD", {"e": "100", "pay": "244.81"})]
    ac_nodes = [make_node("PAY_PERIOD", {"e": "100", "pay": "1155.84"})]

    differences, _, _, _ = compare_nodes(
        cb_nodes, ac_nodes, "PAY_PERIOD", "Root/PAY_PERIOD", ["e"]
    )

    assert len(differences) == 1
    assert differences[0]["Attribute"] == "pay"
