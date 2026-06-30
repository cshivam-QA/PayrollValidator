import xml.etree.ElementTree as ET


class XMLLoader:

    def __init__(self, file_path):
        self.file_path = file_path
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()

    def get_root(self):
        return self.root

    def get_nodes(self, xpath):
        return self.root.findall(xpath)
    
    def get_nv_nodes(self):
        nodes = []

        for h1 in self.root.findall(".//H0/H1"):
            employee_id = h1.attrib.get("id")
            for nv in h1.findall("NV"):
                nv.attrib["_employee_id"] = employee_id
                nodes.append(nv)

        return nodes

    def get_root_info(self):

        return {
            "concept": self.root.attrib.get("concept"),
            "location": self.root.attrib.get("location"),
            "date": self.root.attrib.get("date"),
            "search": self.root.attrib.get("search"),
            "created": self.root.attrib.get("created"),
        }
