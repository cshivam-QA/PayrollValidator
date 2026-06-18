def validate_xml_structure(xml_loader, integration):

    validation_paths = {
        "payroll": ".//H0/H1",
        "timekeeping": ".//Labor",
        "food out": ".//Inventory",
        "vendor schedule": ".//Custom/VDRS",
    }

    path = validation_paths.get(integration.lower())

    if not path:

        raise Exception(f"Unsupported Integration: {integration}")

    nodes = xml_loader.get_nodes(path)

    return len(nodes) > 0
