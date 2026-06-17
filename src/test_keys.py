from xml_loader import XMLLoader
from key_builder import KeyBuilder

cb = XMLLoader("../cb_files/payroll_cb.xml")

daily = cb.get_daily()

print("Total Daily Records:", len(daily))

for node in daily[:5]:
    key = KeyBuilder.build("DAILY", node)
    print(key)
