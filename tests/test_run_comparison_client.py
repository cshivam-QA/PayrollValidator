import inspect
import os

import foodout_arbys_config
import foodout_bww_config
import foodout_lc_config
from run_comparison import attach_xml_paths, get_node_config, run_comparison


def test_attach_xml_paths_keys_rows_like_store_reports():
    store_report_paths = {"00010|20260913": {"excel": "a.xlsx", "pdf": "a.pdf"}}
    xml_sources = [
        ({"Store": "00010", "CB Date": "20260913", "AC Date": "20260913"}, "cb/10.xml", "ac/10.xml"),
        # AC FILE MISSING row: only a CB file.
        ({"Store": "00020", "CB Date": "20260913", "AC Date": ""}, "cb/20.xml", None),
        # CB FILE MISSING row: keyed by the AC date.
        ({"Store": "00030", "CB Date": "", "AC Date": "20260914"}, None, "ac/30.xml"),
    ]

    attach_xml_paths(store_report_paths, xml_sources)

    assert store_report_paths["00010|20260913"] == {
        "excel": "a.xlsx",
        "pdf": "a.pdf",
        "cb_xml": os.path.abspath("cb/10.xml"),
        "ac_xml": os.path.abspath("ac/10.xml"),
    }
    assert store_report_paths["00020|20260913"]["cb_xml"] == os.path.abspath("cb/20.xml")
    assert "ac_xml" not in store_report_paths["00020|20260913"]
    assert store_report_paths["00030|20260914"]["ac_xml"] == os.path.abspath("ac/30.xml")
    assert "cb_xml" not in store_report_paths["00030|20260914"]


def test_food_out_defaults_to_bww_config():
    assert get_node_config("food out") is foodout_bww_config.NODE_CONFIG


def test_food_out_arbys_client_selects_arbys_config():
    assert get_node_config("food out", "arbys") is foodout_arbys_config.NODE_CONFIG


def test_food_out_lc_client_selects_lc_config():
    assert get_node_config("food out", "lc") is foodout_lc_config.NODE_CONFIG


def test_run_comparison_client_parameter_defaults_to_bww():
    signature = inspect.signature(run_comparison)

    assert "client" in signature.parameters
    assert signature.parameters["client"].default == "bww"


def test_run_comparison_existing_parameter_order_is_unchanged():
    # cb_folder, ac_folder, integration, cb_file, ac_file must stay in this
    # order so existing positional calls keep working exactly as before.
    signature = inspect.signature(run_comparison)
    names = list(signature.parameters.keys())

    assert names[:5] == [
        "cb_folder",
        "ac_folder",
        "integration",
        "cb_file",
        "ac_file",
    ]
