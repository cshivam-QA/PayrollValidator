def validate_xml_structure(xml_loader, integration):
    validation_paths = {
        "payroll": ".//H0/H1",
        "timekeeping": ".//Labor",
        "food out": ".//Inventory",
        "vendor schedule": ".//Custom/VDRS",
        "schedule out": ".//Labor/SCH0/SCH1",

        # NEW
        "pmix out": ".//PMix/SM0/SM1",
    }

    if integration is None:
        raise ValueError("integration must be provided")

    path = validation_paths.get(integration.lower())

    if not path:
        raise Exception(f"Unsupported Integration: {integration}")

    nodes = xml_loader.get_nodes(path)

    return len(nodes) > 0
