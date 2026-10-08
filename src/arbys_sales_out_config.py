NODE_CONFIG = [
    {
        "node": "KEY",
        "path": ".//KEYS/KEY",
        "key_fields": ["c"],
        "display_path": "Poll/KEYS/KEY",
    },
    {
        # DK ids repeat under every KEY, so each DK is keyed by its parent
        # KEY's "c" as well (copied onto the DK as "_key").
        "node": "DK",
        "parent_path": ".//KEYS/KEY",
        "child_tag": "DK",
        "parent_attr": "c",
        "parent_key_as": "_key",
        "key_fields": ["_key", "id"],
        "display_path": "Poll/KEYS/KEY/DK",
    },
    {
        "node": "SD1",
        "path": ".//Sales/SD0/SD1",
        "key_fields": ["id"],
        "display_path": "Poll/Sales/SD0/SD1",
    },
    {
        "node": "PS",
        "path": ".//Sales/PmtSummary/PS",
        "key_fields": ["cb-posID"],
        "display_path": "Poll/Sales/PmtSummary/PS",
    },
    {
        "node": "DSC",
        "path": ".//Discounts/DiscSummary/DSC",
        "key_fields": ["id"],
        "display_path": "Poll/Discounts/DiscSummary/DSC",
    },
    {
        "node": "LOOKUP",
        "parent_path": ".//Lookups/Look",
        "child_tag": "L",
        "parent_attr": "category",
        "parent_key_as": "_category",
        "key_fields": ["_category", "cd"],
        "display_path": "Poll/Lookups/Look/L",
    },
]
