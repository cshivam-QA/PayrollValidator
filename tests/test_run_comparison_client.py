import inspect

import foodout_arbys_config
import foodout_bww_config
import foodout_lc_config
from run_comparison import get_node_config, run_comparison


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
