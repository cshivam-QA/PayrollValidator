from xml_loader import XMLLoader

cb = XMLLoader("../cb_files/payroll_cb.xml")

print("H1:", len(cb.get_h1()))
print("JobCodes:", len(cb.get_jobcodes()))
print("Daily:", len(cb.get_daily()))
print("Shift:", len(cb.get_shift()))
print("Weekly:", len(cb.get_weekly()))
print("Pay Period:", len(cb.get_pay_period()))