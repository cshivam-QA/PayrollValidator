class KeyBuilder:

    @staticmethod
    def build(node_type, node):

        if node_type == "H1":
            return node.attrib.get("id")

        if node_type == "JOBCODE":
            return node.attrib.get("c")

        if node_type == "DAILY":
            return f"{node.attrib.get('e')}_{node.attrib.get('j')}"

        if node_type == "SHIFT":
            return f"{node.attrib.get('e')}_{node.attrib.get('j')}_{node.attrib.get('in')}"

        if node_type == "PAY_PERIOD":
            return f"{node.attrib.get('e')}_{node.attrib.get('j')}"

        return None