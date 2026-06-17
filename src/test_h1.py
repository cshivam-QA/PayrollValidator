from xml_loader import XMLLoader

cb = XMLLoader("cb_files/payroll_cb.xml")

nodes = cb.get_nodes(".//H0/H1")

ids = [node.attrib.get("id") for node in nodes]

print("Total Nodes :", len(ids))
print("Unique IDs  :", len(set(ids)))

for emp in set(ids):
    if ids.count(emp) > 1:
        print("Duplicate:", emp)
