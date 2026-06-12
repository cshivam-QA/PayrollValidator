from xml_loader import XMLLoader
from comparator import compare_nodes
from report_generator import generate_reports


cb = XMLLoader("../cb_files/payroll_cb.xml")
ac = XMLLoader("../ac_files/payroll_ac.xml")

differences, zero_values = compare_nodes(
    cb.get_daily(),
    ac.get_daily(),
    "DAILY",
    "Poll/Labor/TM0(type=DAILY)/TM1"
)

print("Total Differences:", len(differences))
print("Total Zero Values:", len(zero_values))

generate_reports(
    differences,
    zero_values
)