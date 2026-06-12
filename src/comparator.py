from key_builder import KeyBuilder


def normalize_value(value):

    if value is None:
        return None

    try:
        return float(value)
    except:
        return str(value).strip()


def compare_nodes(cb_nodes, ac_nodes, node_name, path):

    differences = []
    zero_values = []

    cb_map = {
        KeyBuilder.build(node_name, node): node
        for node in cb_nodes
    }

    ac_map = {
        KeyBuilder.build(node_name, node): node
        for node in ac_nodes
    }

    all_keys = set(cb_map.keys()) | set(ac_map.keys())

    for key in all_keys:

        cb = cb_map.get(key)
        ac = ac_map.get(key)

        # Missing Record in CB
        if cb is None:
            differences.append({
                "Type": "Missing Record In CB",
                "Node": node_name,
                "Path": path,
                "Key": key,
                "Attribute": "",
                "CB Value": "",
                "AC Value": "Record Exists"
            })
            continue

        # Missing Record in AC
        if ac is None:
            differences.append({
                "Type": "Missing Record In AC",
                "Node": node_name,
                "Path": path,
                "Key": key,
                "Attribute": "",
                "CB Value": "Record Exists",
                "AC Value": ""
            })
            continue

        attrs = set(cb.attrib.keys()) | set(ac.attrib.keys())

        for attr in attrs:

            cb_val = cb.attrib.get(attr)
            ac_val = ac.attrib.get(attr)

            # Missing Attribute in AC
            if ac_val is None:

                try:
                    if float(cb_val) == 0:
                        zero_values.append({
                            "Node": node_name,
                            "Path": path,
                            "Key": key,
                            "Attribute": attr,
                            "CB Value": cb_val
                        })
                        continue
                except:
                    pass

                differences.append({
                    "Type": "Missing Attribute In AC",
                    "Node": node_name,
                    "Path": path,
                    "Key": key,
                    "Attribute": attr,
                    "CB Value": cb_val,
                    "AC Value": ""
                })

                continue

            # Missing Attribute in CB
            if cb_val is None:

                differences.append({
                    "Type": "Missing Attribute In CB",
                    "Node": node_name,
                    "Path": path,
                    "Key": key,
                    "Attribute": attr,
                    "CB Value": "",
                    "AC Value": ac_val
                })

                continue

            cb_norm = normalize_value(cb_val)
            ac_norm = normalize_value(ac_val)

            if cb_norm != ac_norm:

                differences.append({
                    "Type": "Value Mismatch",
                    "Node": node_name,
                    "Path": path,
                    "Key": key,
                    "Attribute": attr,
                    "CB Value": cb_val,
                    "AC Value": ac_val
                })

    return differences, zero_values