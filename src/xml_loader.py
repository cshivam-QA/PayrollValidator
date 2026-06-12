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

    def get_root_info(self):

        return {
            "concept": self.root.attrib.get("concept"),
            "location": self.root.attrib.get("location"),
            "date": self.root.attrib.get("date"),
            "search": self.root.attrib.get("search"),
            "created": self.root.attrib.get("created")
        }