import arbys_sales_out_config
from comparator import compare_nodes
from run_comparison import get_integration_label, get_node_config
from xml_loader import XMLLoader
from xml_validator import validate_xml_structure


SALES_XML = """<Poll search="AC_POS_SALES" location="05875" date="20261007">
  <KEYS>
    <KEY c="posNetSalesAmt" v="{net}"/>
    <KEY c="adjGrossSales" v="879.37">
      <DK id="43" v="{dk43}"/>
      <DK id="45" v="53.90"/>
    </KEY>
    <KEY c="itemCount" v="300">
      <DK id="43" v="15"/>
    </KEY>
  </KEYS>
  <Sales>
    <SD0><SD1 id="43" n="3" net="{sd_net}" g="41.56" ng="3"/></SD0>
  </Sales>
  <Lookups>
    <Look category="PAYMENT_TYPE"><L cd="1" ds="Cash"/></Look>
  </Lookups>
</Poll>"""


def _write(tmp_path, name, **values):
    params = {"net": "813.54", "dk43": "41.56", "sd_net": "38.84"}
    params.update(values)
    path = tmp_path / name
    path.write_text(SALES_XML.format(**params), encoding="utf-8")
    return XMLLoader(str(path))


def _compare(cb, ac):
    results = {}
    for config in arbys_sales_out_config.NODE_CONFIG:
        if "parent_path" in config:
            args = (
                config["parent_path"],
                config["child_tag"],
                config["parent_attr"],
                config["parent_key_as"],
            )
            cb_nodes = cb.get_child_nodes_with_parent(*args)
            ac_nodes = ac.get_child_nodes_with_parent(*args)
        else:
            cb_nodes = cb.get_nodes(config["path"])
            ac_nodes = ac.get_nodes(config["path"])
        results[config["node"]] = compare_nodes(
            cb_nodes, ac_nodes, config["node"], config["display_path"], config["key_fields"]
        )
    return results


def test_dk_children_are_keyed_by_parent_key(tmp_path):
    loader = _write(tmp_path, "cb.xml")

    nodes = loader.get_child_nodes_with_parent(".//KEYS/KEY", "DK", "c", "_key")

    keys = sorted((n.attrib["_key"], n.attrib["id"]) for n in nodes)
    assert keys == [("adjGrossSales", "43"), ("adjGrossSales", "45"), ("itemCount", "43")]


def test_identical_files_report_no_issues(tmp_path):
    results = _compare(_write(tmp_path, "cb.xml"), _write(tmp_path, "ac.xml"))

    for differences, zero_values, missing, duplicates in results.values():
        assert differences == []
        assert missing == []
        assert duplicates == []


def test_dk_value_difference_is_reported_against_its_parent_key(tmp_path):
    results = _compare(_write(tmp_path, "cb.xml"), _write(tmp_path, "ac.xml", dk43="40.00"))

    differences = results["DK"][0]
    assert len(differences) == 1
    assert differences[0]["Key"] == "adjGrossSales_43"
    assert differences[0]["CB Value"] == "41.56"
    assert differences[0]["AC Value"] == "40.00"


def test_key_and_sales_value_differences_are_reported(tmp_path):
    results = _compare(
        _write(tmp_path, "cb.xml"),
        _write(tmp_path, "ac.xml", net="800.00", sd_net="30.00"),
    )

    assert results["KEY"][0][0]["Key"] == "posNetSalesAmt"
    assert results["SD1"][0][0]["Attribute"] == "net"


def test_arbys_sales_out_wiring():
    assert get_node_config("arby's sales out") is arbys_sales_out_config.NODE_CONFIG
    assert get_integration_label("arby's sales out", "AC_POS_SALES") == "Arby's Sales Out"
    # Other integrations keep their existing search-based label.
    assert get_integration_label("payroll", "PAYROLL_EXPORT") == "Payroll Out"


def test_validation_accepts_sales_files_and_rejects_others(tmp_path):
    sales = _write(tmp_path, "cb.xml")
    payroll_path = tmp_path / "payroll.xml"
    payroll_path.write_text('<Poll><H0><H1 id="1"/></H0></Poll>', encoding="utf-8")

    assert validate_xml_structure(sales, "arby's sales out")
    assert not validate_xml_structure(XMLLoader(str(payroll_path)), "arby's sales out")
