from xml_loader import XMLLoader
from file_matcher import get_matching_files
from master_report_generator import generate_master_report


cb_files, ac_files = get_matching_files()

print()
print("CB Files Found :", len(cb_files))
print("AC Files Found :", len(ac_files))
print()

matched = set(cb_files.keys()) & set(ac_files.keys())

print("Matched Files :", len(matched))
print()

summary = []

for key in sorted(matched):

    cb_xml = cb_files[key]
    ac_xml = ac_files[key]

    cb = XMLLoader(cb_xml)
    ac = XMLLoader(ac_xml)

    cb_info = cb.get_root_info()
    ac_info = ac.get_root_info()

    summary.append({

        "Store":
        cb_info.get("location"),

        "Date":
        cb_info.get("date"),

        "CB File":
        cb_xml,

        "AC File":
        ac_xml,

        "Status":
        "MATCHED"

    })

generate_master_report(
    summary
)