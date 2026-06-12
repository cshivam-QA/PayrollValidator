class KeyBuilder:

    @staticmethod
    def build(node, key_fields):

        values = []

        for field in key_fields:

            value = node.attrib.get(field)

            if value is None:
                value = "NULL"

            values.append(str(value))

        return "_".join(values)