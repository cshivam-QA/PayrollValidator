from xml_loader import XMLLoader
from node_config import NODE_CONFIG
from comparator import compare_nodes
from report_generator import generate_report


def get_unique_count(nodes, key_fields):

    unique_keys = set()

    for node in nodes:

        key = "_".join(
            str(node.attrib.get(field, ""))
            for field in key_fields
        )

        unique_keys.add(key)

    return len(unique_keys)


cb = XMLLoader(
    "cb_files/payroll_cb.xml"
)

ac = XMLLoader(
    "ac_files/payroll_ac.xml"
)

all_differences = []
all_missing_records = []
all_zero_values = []
all_duplicate_records = []
summary = []

root_info = []

cb_root = cb.get_root_info()
ac_root = ac.get_root_info()

for key in cb_root.keys():

    root_info.append({
        "Property": key,
        "CB": cb_root.get(key),
        "AC": ac_root.get(key)
    })

for config in NODE_CONFIG:

    node_name = config["node"]

    cb_nodes = cb.get_nodes(
        config["path"]
    )

    ac_nodes = ac.get_nodes(
        config["path"]
    )

    (
        differences,
        zero_values,
        missing_records,
        duplicate_records

    ) = compare_nodes(

        cb_nodes,
        ac_nodes,
        node_name,
        config["display_path"],
        config["key_fields"]

    )

    all_differences.extend(
        differences
    )

    all_missing_records.extend(
        missing_records
    )

    all_zero_values.extend(
        zero_values
    )

    all_duplicate_records.extend(
        duplicate_records
    )

    total_issues = (
        len(differences)
        +
        len(missing_records)
        +
        len(duplicate_records)
    )

    cb_count = get_unique_count(
        cb_nodes,
        config["key_fields"]
    )

    ac_count = get_unique_count(
        ac_nodes,
        config["key_fields"]
    )

    summary.append({

        "Node":
        node_name,

        "CB Count":
        cb_count,

        "AC Count":
        ac_count,

        "Differences":
        total_issues,

        "Status":
        (
            "PASS"
            if total_issues == 0
            else "FAIL"
        )

    })

generate_report(

    summary,

    root_info,

    all_differences,

    all_missing_records,

    all_zero_values,

    all_duplicate_records

)

print()
print(
    "Total Differences:",
    len(all_differences)
)

print(
    "Total Missing Records:",
    len(all_missing_records)
)

print(
    "Total Zero Values:",
    len(all_zero_values)
)

print(
    "Total Duplicates:",
    len(all_duplicate_records)
)

input("\nPress Enter to exit...")