# pmix_config.py

NODE_CONFIG = [

    # ------------------------------------------------------------------
    # PMix Item
    # Poll -> PMix -> SM0 -> SM1
    # Unique: Product Code (c)
    # ------------------------------------------------------------------
    {
        "node": "SM1",
        "path": ".//PMix/SM0/SM1",
        "key_fields": ["c"],
        "display_path": "Poll/PMix/SM0/SM1",
    },

    # ------------------------------------------------------------------
    # Product Attributes
    # Poll -> PMix -> SM0 -> SM1 -> NV
    # Unique: Parent Product + Attribute Name
    # ------------------------------------------------------------------
    {
        "node": "NV",
        "path": ".//PMix/SM0/SM1/NV",
        "key_fields": ["_product", "n"],
        "display_path": "Poll/PMix/SM0/SM1/NV",
    },

    # ------------------------------------------------------------------
    # Direct Ingredients
    # Poll -> PMix -> SM0 -> SM1 -> SMI1
    # Unique: Parent Product + Ingredient Code
    # ------------------------------------------------------------------
    {
        "node": "SMI1",
        "path": ".//PMix/SM0/SM1/SMI1",
        "key_fields": ["_product", "cd"],
        "display_path": "Poll/PMix/SM0/SM1/SMI1",
    },

    # ------------------------------------------------------------------
    # Prep Mix
    # Poll -> PMix -> SM0 -> SM1 -> SMP1
    # Unique: Parent Product + Prep Code
    # ------------------------------------------------------------------
    {
        "node": "SMP1",
        "path": ".//PMix/SM0/SM1/SMP1",
        "key_fields": ["_product", "cd"],
        "display_path": "Poll/PMix/SM0/SM1/SMP1",
    },

    # ------------------------------------------------------------------
    # Prep Mix Ingredients
    # Poll -> PMix -> SM0 -> SM1 -> SMP1 -> SMI1
    # Unique: Parent Product + Parent Prep + Ingredient Code
    # ------------------------------------------------------------------
    {
        "node": "SMP1_SMI1",
        "path": ".//PMix/SM0/SM1/SMP1/SMI1",
        "key_fields": ["_product", "_smp1", "cd"],
        "display_path": "Poll/PMix/SM0/SM1/SMP1/SMI1",
    },

]