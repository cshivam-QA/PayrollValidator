import os

from xml_loader import XMLLoader


def get_xml_key(file_path):

    try:

        xml = XMLLoader(file_path)

        info = xml.get_root_info()

        store = str(info.get("location", "")).strip()

        business_date = str(info.get("date", "")).strip()

        if not store or not business_date:

            return None

        print(
            f"FILE={os.path.basename(file_path)} | "
            f"STORE={store} | "
            f"DATE={business_date}"
        )

        return f"{store}_{business_date}"

    except Exception:

        return None


def get_matching_files(cb_folder, ac_folder):

    cb_files = {}

    ac_files = {}

    if not os.path.exists(cb_folder):

        return {}, {}

    if not os.path.exists(ac_folder):

        return {}, {}

    for file in os.listdir(cb_folder):

        if file.lower().endswith(".xml"):

            full_path = os.path.join(cb_folder, file)

            key = get_xml_key(full_path)

            if key:

                cb_files[key] = full_path

    for file in os.listdir(ac_folder):

        if file.lower().endswith(".xml"):

            full_path = os.path.join(ac_folder, file)

            key = get_xml_key(full_path)

            if key:

                ac_files[key] = full_path

    print("\nCB FILES:")
    for k, v in cb_files.items():
        print(k, "=>", v)

    print("\nAC FILES:")
    for k, v in ac_files.items():
        print(k, "=>", v)

    return cb_files, ac_files
