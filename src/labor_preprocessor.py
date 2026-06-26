from datetime import datetime
import copy
from collections import defaultdict


def filter_exception_records(root, exception_nodes):

    pay_period = root.find(".//TM0[@type='PAY_PERIOD']")

    if pay_period is None:
        return exception_nodes

    begdt = datetime.strptime(
        pay_period.attrib["begdt"], "%Y%m%d"
    ).date()

    enddt = datetime.strptime(
        pay_period.attrib["enddt"], "%Y%m%d"
    ).date()

    filtered = []

    for node in exception_nodes:

        punch_date = datetime.strptime(
            node.attrib["in"].split(" ")[0],
            "%m/%d/%Y"
        ).date()

        if begdt <= punch_date <= enddt:
            filtered.append(node)

    return filtered


def aggregate_pay_period_tm1(nodes):

    grouped = defaultdict(list)

    for node in nodes:

        key = (
            node.attrib.get("e", ""),
            node.attrib.get("j", ""),
            node.attrib.get("dt", ""),
            node.attrib.get("r", ""),
        )

        grouped[key].append(node)

    aggregated_nodes = []

    numeric_fields = [
        "rh",
        "wkh",
        "rp",
        "pay",
        "op",
        "ot",
        "dp",
    ]

    for records in grouped.values():

        if len(records) == 1:
            aggregated_nodes.append(records[0])
            continue

        merged = copy.deepcopy(records[0])

        for field in numeric_fields:

            total = 0.0
            found = False

            for record in records:

                value = record.attrib.get(field)

                if value not in (None, ""):
                    total += float(value)
                    found = True

            if found:
                merged.attrib[field] = str(round(total, 2))

        aggregated_nodes.append(merged)

    return aggregated_nodes