from xml_loader import XMLLoader


def build_labor_forecast_map(xml_loader):

    result = {}

    root = xml_loader.get_root()

    for dnv1 in root.findall(".//DNV/DNV1"):

        dt = dnv1.attrib.get("dt", "")
        section = dnv1.attrib.get("section", "")

        for nv in dnv1.findall("./NV"):

            n = nv.attrib.get("n", "")

            for dk in nv.findall("./DK"):

                dk_id = dk.attrib.get("id", "")

                key = f"{dt}_{section}_{n}_{dk_id}"
                if key in result:
                    print(f"Duplicate key found: {key}")

                result[key] = {
                    "dt": dt,
                    "section": section,
                    "n": n,
                    "id": dk_id,
                    "value": dk.attrib.get("v"),
                }

    return result
def compare_labor_forecast(cb_xml, ac_xml):

    cb_loader = XMLLoader(cb_xml)
    ac_loader = XMLLoader(ac_xml)

    cb_map = build_labor_forecast_map(cb_loader)
    ac_map = build_labor_forecast_map(ac_loader)

    differences = []
    missing_records = []

    all_keys = set(cb_map.keys()) | set(ac_map.keys())

    for key in all_keys:

        cb = cb_map.get(key)
        ac = ac_map.get(key)

        if cb is None:
            missing_records.append(
                {
                    "Node": "DK",
                    "Date": ac["dt"],
                    "Section": ac["section"],
                    "NV": ac["n"],
                    "DK ID": ac["id"],
                    "Missing In": "CB",
                }
            )
            continue

        if ac is None:
            missing_records.append(
                {
                    "Node": "DK",
                    "Date": cb["dt"],
                    "Section": cb["section"],
                    "NV": cb["n"],
                    "DK ID": cb["id"],
                    "Missing In": "AC",
                }
            )
            continue

        try:
            cb_val = round(float(cb["value"]), 4)
        except:
            cb_val = cb["value"]

        try:
            ac_val = round(float(ac["value"]), 4)
        except:
            ac_val = ac["value"]

        if cb_val != ac_val:
            differences.append(
                {
                    "Node": "DK",
                    "Difference Type": "Value Mismatch",
                    "Date": cb["dt"],
                    "Section": cb["section"],
                    "NV": cb["n"],
                    "DK ID": cb["id"],
                    "Attribute": "v",
                    "CB Value": cb["value"],
                    "AC Value": ac["value"],
                }
            )

    return differences, missing_records