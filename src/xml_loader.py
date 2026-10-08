import xml.etree.ElementTree as ET


class XMLLoader:

    def __init__(self, file_path):
        self.file_path = file_path

        try:
            self.tree = ET.parse(file_path)
        except ET.ParseError as e:
            raise ValueError(
                f"Invalid or corrupt XML file: {file_path} ({e})"
            ) from e
        except OSError as e:
            raise ValueError(
                f"Unable to read XML file: {file_path} ({e})"
            ) from e

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

    def get_child_nodes_with_parent(self, parent_xpath, child_tag, parent_attr, as_attr):
        """Returns copies of each parent's direct <child_tag> children, with the
        parent's `parent_attr` value added as `as_attr`, so children whose ids
        repeat under different parents can be keyed uniquely."""

        nodes = []

        for parent in self.root.findall(parent_xpath):
            parent_value = parent.attrib.get(parent_attr)
            for child in parent.findall(child_tag):
                attrib = dict(child.attrib)
                attrib[as_attr] = parent_value
                nodes.append(ET.Element(child.tag, attrib))

        return nodes

    def get_root_info(self):

        return {
            "concept": self.root.attrib.get("concept"),
            "location": self.root.attrib.get("location"),
            "date": self.root.attrib.get("date"),
            "search": self.root.attrib.get("search"),
            "created": self.root.attrib.get("created"),
        }
