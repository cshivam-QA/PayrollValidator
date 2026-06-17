NODE_CONFIG = [
    {
        "node": "INVENTORY_TYPE",
        "path": ".//CODES[@type='INVENTORY_TYPE']/CODE",
        "key_fields": ["cd"],
        "display_path": "Poll/Inventory/CODES(type=INVENTORY_TYPE)/CODE",
    },
    {
        "node": "GLCODE",
        "path": ".//CODES[@type='GLCODE']/CODE",
        "key_fields": ["cd"],
        "display_path": "Poll/Inventory/CODES(type=GLCODE)/CODE",
    },
    {
        "node": "INVENTORY_GROUP",
        "path": ".//CODES[@type='INVENTORY_GROUP']/CODE",
        "key_fields": ["cd"],
        "display_path": "Poll/Inventory/CODES(type=INVENTORY_GROUP)/CODE",
    },
    {
        "node": "INV_DAILY",
        "path": ".//INV[@freq='D']/INV1",
        "key_fields": ["cd"],
        "display_path": "Poll/Inventory/INV(freq=D)/INV1",
    },
    {
        "node": "DLV",
        "path": ".//DLV/DLV1",
        "key_fields": ["cd"],
        "display_path": "Poll/Inventory/DLV/DLV1",
    },
    {
        "node": "CM",
        "path": ".//CM/CM1",
        "key_fields": ["cd"],
        "display_path": "Poll/Inventory/CM/CM1",
    },
    {
        "node": "INVC",
        "path": ".//INVC/INVC1",
        "key_fields": ["cd"],
        "display_path": "Poll/Inventory/INVC/INVC1",
    },
    {
        "node": "INVXF",
        "path": ".//INVXF/INVXF1",
        "key_fields": ["cd", "ref"],
        "display_path": "Poll/Inventory/INVXF/INVXF1",
    },
    {
        "node": "WASTE",
        "path": ".//Waste/WI",
        "key_fields": ["c"],
        "display_path": "Poll/Waste/WI",
    },
]
