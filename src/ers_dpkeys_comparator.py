def compare_ers_dpkeys(cb_root, ac_root):
    """
    Compare ERS DPKeys using KEY -> DK hierarchy.

    Rules:
    - KEY is identified by attribute 'c'
    - DK is identified by attribute 'id'
    - AC DKs with value 0.0 are completely ignored
    - Numeric values are compared without rounding or tolerance
    - Formatting differences such as 62.9000 vs 62.9 are treated as equal
    - Any actual numeric difference, even 0.0001, is reported
    - KEY-level 'v' is also compared
    - Missing and duplicate records are reported
    """

    differences = []
    missing_records = []
    zero_values = []
    duplicate_records = []

    cb_keys = cb_root.findall(".//KEYS/KEY")
    ac_keys = ac_root.findall(".//KEYS/KEY")

    cb_key_map = {}
    ac_key_map = {}

    # -------------------------
    # Build CB KEY map
    # -------------------------
    for key_node in cb_keys:
        key_name = key_node.attrib.get("c", "")

        if key_name in cb_key_map:
            duplicate_records.append({
                "Type": "KEY",
                "Key": key_name,
                "Details": "Duplicate KEY found in CB",
            })
        else:
            cb_key_map[key_name] = key_node

    # -------------------------
    # Build AC KEY map
    # -------------------------
    for key_node in ac_keys:
        key_name = key_node.attrib.get("c", "")

        if key_name in ac_key_map:
            duplicate_records.append({
                "Type": "KEY",
                "Key": key_name,
                "Details": "Duplicate KEY found in AC",
            })
        else:
            ac_key_map[key_name] = key_node

    # -------------------------
    # Compare KEYs
    # -------------------------
    all_key_names = set(cb_key_map) | set(ac_key_map)

    for key_name in sorted(all_key_names):

        cb_key = cb_key_map.get(key_name)
        ac_key = ac_key_map.get(key_name)

        # KEY exists in CB but not AC
        if cb_key is not None and ac_key is None:
            missing_records.append({
                "Type": "KEY",
                "Key": key_name,
                "Details": "KEY missing in AC",
            })
            continue

        # KEY exists in AC but not CB
        if cb_key is None and ac_key is not None:

            meaningful_dks = [
                dk
                for dk in ac_key.findall("./DK")
                if not _is_zero(dk.attrib.get("v"))
            ]

            if meaningful_dks:
                missing_records.append({
                    "Type": "KEY",
                    "Key": key_name,
                    "Details": "KEY missing in CB",
                })

            continue

        # -------------------------
        # Compare KEY-level value
        # -------------------------
        cb_key_value = cb_key.attrib.get("v")
        ac_key_value = ac_key.attrib.get("v")

        if not values_are_equal(cb_key_value, ac_key_value):
            differences.append({
                "Type": "KEY",
                "Key": key_name,
                "Field": "v",
                "CB Value": cb_key_value,
                "AC Value": ac_key_value,
            })

        # -------------------------
        # Build DK maps
        # -------------------------
        cb_dks = {}
        ac_dks = {}

        # -------------------------
        # CB DKs
        # -------------------------
        for dk in cb_key.findall("./DK"):

            dk_id = dk.attrib.get("id", "")

            if dk_id in cb_dks:
                duplicate_records.append({
                    "Type": "DK",
                    "Key": key_name,
                    "DK ID": dk_id,
                    "Details": "Duplicate DK found in CB",
                })
            else:
                cb_dks[dk_id] = dk

        # -------------------------
        # AC DKs
        # -------------------------
        for dk in ac_key.findall("./DK"):

            dk_id = dk.attrib.get("id", "")
            dk_value = dk.attrib.get("v")

            # AC zero-valued DKs are completely ignored.
            if _is_zero(dk_value):
                continue

            if dk_id in ac_dks:
                duplicate_records.append({
                    "Type": "DK",
                    "Key": key_name,
                    "DK ID": dk_id,
                    "Details": "Duplicate DK found in AC",
                })
            else:
                ac_dks[dk_id] = dk

        # -------------------------
        # Compare DKs
        # -------------------------
        all_dk_ids = set(cb_dks) | set(ac_dks)

        for dk_id in sorted(all_dk_ids, key=_sort_dk_id):

            cb_dk = cb_dks.get(dk_id)
            ac_dk = ac_dks.get(dk_id)

            # DK exists in CB but not AC
            if cb_dk is not None and ac_dk is None:
                missing_records.append({
                    "Type": "DK",
                    "Key": key_name,
                    "DK ID": dk_id,
                    "Details": "DK missing in AC",
                })
                continue

            # DK exists in AC but not CB
            if cb_dk is None and ac_dk is not None:
                missing_records.append({
                    "Type": "DK",
                    "Key": key_name,
                    "DK ID": dk_id,
                    "Details": "DK missing in CB",
                })
                continue

            cb_value = cb_dk.attrib.get("v")
            ac_value = ac_dk.attrib.get("v")

            # No tolerance and no rounding.
            # Only formatting differences such as
            # 62.9000 vs 62.9 are treated as equal.
            if not values_are_equal(cb_value, ac_value):
                differences.append({
                    "Type": "DK",
                    "Key": key_name,
                    "DK ID": dk_id,
                    "Field": "v",
                    "CB Value": cb_value,
                    "AC Value": ac_value,
                })

    return (
        differences,
        zero_values,
        missing_records,
        duplicate_records,
    )


def values_are_equal(cb_value, ac_value):
    """
    Compare values numerically when possible.

    Examples:
        62.9000 == 62.9       -> True
        36.4561 == 36.4560    -> False
        3382.8216 == 3382.82  -> False

    No rounding or tolerance is applied.
    """

    try:
        return float(cb_value) == float(ac_value)
    except (ValueError, TypeError):
        return cb_value == ac_value


def _is_zero(value):
    if value in (None, ""):
        return False

    try:
        return float(value) == 0.0
    except (ValueError, TypeError):
        return False


def _sort_dk_id(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return value