from xml_loader import XMLLoader
from file_matcher import get_matching_files
from master_report_generator import generate_master_report
from comparator import compare_nodes
import os


def get_node_config(integration, client="bww"):

    if integration == "payroll":

        from payroll_config import NODE_CONFIG

        return NODE_CONFIG

    elif integration == "timekeeping":

        from timekeeping_config import NODE_CONFIG

        return NODE_CONFIG

    elif integration == "food out":

        if client.lower() == "bww":

            from foodout_bww_config import NODE_CONFIG

        elif client.lower() == "arbys":

            from foodout_arbys_config import NODE_CONFIG

        elif client.lower() == "lc":

            from foodout_lc_config import NODE_CONFIG

        else:

            raise Exception(f"Unsupported Food Out Client: {client}")

        return NODE_CONFIG

    elif integration == "vendor schedule":

        from vendor_schedule_config import NODE_CONFIG

        return NODE_CONFIG

    raise Exception(f"Unsupported Integration: {integration}")


def run_comparison(cb_folder, ac_folder, integration="payroll"):

    node_config = get_node_config(integration)

    cb_files, ac_files = get_matching_files(cb_folder, ac_folder)

    summary = []

    all_differences = []

    all_missing_records = []

    all_zero_values = []

    all_duplicate_records = []

    matched = set(cb_files.keys()) & set(ac_files.keys())

    missing_cb = set(ac_files.keys()) - set(cb_files.keys())

    missing_ac = set(cb_files.keys()) - set(ac_files.keys())

    for key in sorted(matched):

        cb_xml = cb_files[key]

        ac_xml = ac_files[key]

        cb = XMLLoader(cb_xml)

        ac = XMLLoader(ac_xml)

        cb_info = cb.get_root_info()

        file_difference_count = 0

        file_missing_count = 0

        file_zero_count = 0

        file_duplicate_count = 0

        for config in node_config:
            differences, zero_values, missing_records, duplicate_records = (
                compare_nodes(
                    cb.get_nodes(config["path"]),
                    ac.get_nodes(config["path"]),
                    config["node"],
                    config["display_path"],
                    config["key_fields"],
                )
            )

            for row in differences:
                row["Store"] = cb_info.get("location")
                row["Date"] = cb_info.get("date")

            for row in missing_records:
                row["Store"] = cb_info.get("location")
                row["Date"] = cb_info.get("date")

            for row in zero_values:
                row["Store"] = cb_info.get("location")
                row["Date"] = cb_info.get("date")

            for row in duplicate_records:
                row["Store"] = cb_info.get("location")
                row["Date"] = cb_info.get("date")

            all_differences.extend(differences)

            all_missing_records.extend(missing_records)

            all_zero_values.extend(zero_values)

            all_duplicate_records.extend(duplicate_records)

            file_difference_count += len(differences)

            file_missing_count += len(missing_records)

            file_zero_count += len(zero_values)

            file_duplicate_count += len(duplicate_records)

        total_issues = file_difference_count + file_missing_count + file_duplicate_count

        summary.append(
            {
                "Store": cb_info.get("location"),
                "Date": cb_info.get("date"),
                "CB File": os.path.basename(cb_xml),
                "AC File": os.path.basename(ac_xml),
                "Status": ("PASS" if total_issues == 0 else "FAIL"),
                "Differences": file_difference_count,
                "Missing Records": file_missing_count,
                "Zero Values": file_zero_count,
                "Duplicates": file_duplicate_count,
            }
        )
    for key in sorted(missing_ac):

        summary.append(
            {
                "Store": key.split("_")[0],
                "Date": key.split("_")[1],
                "CB File": os.path.basename(cb_files[key]),
                "AC File": "Missing",
                "Status": "AC FILE MISSING",
                "Differences": 0,
                "Missing Records": 0,
                "Zero Values": 0,
                "Duplicates": 0,
            }
        )

    for key in sorted(missing_cb):

        summary.append(
            {
                "Store": key.split("_")[0],
                "Date": key.split("_")[1],
                "CB File": "Missing",
                "AC File": os.path.basename(ac_files[key]),
                "Status": "CB FILE MISSING",
                "Differences": 0,
                "Missing Records": 0,
                "Zero Values": 0,
                "Duplicates": 0,
            }
        )

    summary.sort(key=lambda x: (x["Store"], x["Date"]))

    generate_master_report(
        summary,
        all_differences,
        all_missing_records,
        all_zero_values,
        all_duplicate_records,
    )

    return {
        "success": True,
        "report_path": "reports/Master_Comparison_Report.xlsx",
        "total_files": len(summary),
    }
