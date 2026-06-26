import math
from key_builder import KeyBuilder

EXCLUDED_ATTRIBUTES = {"DAILY": ["otr"], "SHIFT": ["otr"], "PAY_PERIOD": ["otr"]}
ATTRIBUTE_TOLERANCE = {
    "r": 0.01,      # Existing rule
    "rp": 0.01,     # New
    "pay": 0.01,    # Existing
    "op": 0.01,     # New
    "dp": 0.01,     # New
}

EXCLUDED_ZERO_ATTRIBUTES = ("trh",)
OPTIONAL_ZERO_ATTRIBUTES = {"rh"}

def normalize_value(value):

    if value is None:
        return None

    try:
        return round(float(value), 4)
    except:
        return str(value).strip()


def is_zero_value(value):

    try:
        return float(value) == 0
    except:
        return False


def build_node_map(nodes, key_fields):

    node_map = {}
    duplicates = []

    for node in nodes:

        key = KeyBuilder.build(node, key_fields)

        if key in node_map:
            duplicates.append(key)
        else:
            node_map[key] = node

    return node_map, duplicates


def compare_nodes(cb_nodes, ac_nodes, node_name, path, key_fields):

    differences = []
    zero_values = []
    missing_records = []
    duplicate_records = []

    cb_map, cb_duplicates = build_node_map(cb_nodes, key_fields)

    ac_map, ac_duplicates = build_node_map(ac_nodes, key_fields)

    # H1 duplicates are valid when exception records exist
    if node_name != "H1":

        for key in cb_duplicates:

            duplicate_records.append({"Node": node_name, "Key": key, "Side": "CB"})

        for key in ac_duplicates:

            duplicate_records.append({"Node": node_name, "Key": key, "Side": "AC"})

    all_keys = set(cb_map.keys()) | set(ac_map.keys())

    for key in all_keys:

        cb = cb_map.get(key)
        ac = ac_map.get(key)

        if cb is None:

            missing_records.append(
                {
                    "Node": node_name,
                    "Key": key,
                    "Missing In": "CB",
                    "CB Attributes": "",
                    "AC Attributes": str(ac.attrib),
                }
            )

            continue

        if ac is None:

            missing_records.append(
                {
                    "Node": node_name,
                    "Key": key,
                    "Missing In": "AC",
                    "CB Attributes": str(cb.attrib),
                    "AC Attributes": "",
                }
            )

            continue

        attrs = set(cb.attrib.keys()) | set(ac.attrib.keys())

        for attr in attrs:
            if attr.lower() == "trh":
                continue
            if attr.lower() == "cb-wi":
                continue
            if attr.lower() == "s":
                continue

            if attr in EXCLUDED_ATTRIBUTES.get(node_name, []):
                continue

            cb_val = cb.attrib.get(attr)
            ac_val = ac.attrib.get(attr)

            if (
                attr not in EXCLUDED_ZERO_ATTRIBUTES
                and cb_val is not None
                and ac_val is not None
            ):

                cb_is_zero = is_zero_value(cb_val)
                ac_is_zero = is_zero_value(ac_val)

                if cb_is_zero and ac_is_zero:
                    continue

                if cb_is_zero and not ac_is_zero:

                    zero_values.append(
                        {
                            "Node": node_name,
                            "Path": path,
                            "Key": key,
                            "Attribute": attr,
                            "Value": cb_val,
                            "Side": "CB",
                        }
                    )

                    continue

                if ac_is_zero and not cb_is_zero:

                    zero_values.append(
                        {
                            "Node": node_name,
                            "Path": path,
                            "Key": key,
                            "Attribute": attr,
                            "Value": ac_val,
                            "Side": "AC",
                        }
                    )

                    continue

            if (
                attr.lower() in OPTIONAL_ZERO_ATTRIBUTES
                and ac_val is None
                and cb_val is not None
                and is_zero_value(cb_val)
            ):
                continue

            if ac_val is None:

                differences.append(
                    {
                        "Node": node_name,
                        "Difference Type": "Missing Attribute In AC",
                        "Path": path,
                        "Key": key,
                        "Attribute": attr,
                        "CB Value": cb_val,
                        "AC Value": "",
                    }
                )

                continue

            if (
                attr.lower() in OPTIONAL_ZERO_ATTRIBUTES
                and cb_val is None
                and ac_val is not None
                and is_zero_value(ac_val)
            ):
                continue

            cb_norm = normalize_value(cb_val)
            ac_norm = normalize_value(ac_val)

            lower_attr = attr.lower()

            try:
                if lower_attr in ATTRIBUTE_TOLERANCE:
                    tolerance = ATTRIBUTE_TOLERANCE[lower_attr]
                    cb_num = round(float(cb_val), 2)
                    ac_num = round(float(ac_val), 2)

                    if abs(cb_num - ac_num) <= (tolerance + 1e-9):
                        continue
            except Exception:
                pass

            if cb_norm != ac_norm:

                differences.append(
                    {
                        "Node": node_name,
                        "Difference Type": "Value Mismatch",
                        "Path": path,
                        "Key": key,
                        "Attribute": attr,
                        "CB Value": cb_val,
                        "AC Value": ac_val,
                    }
                )

    return (
        differences,
        zero_values,
        missing_records,
        duplicate_records,
    )