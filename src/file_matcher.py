import os
import re


def get_file_key(file_name):

    match = re.search(
        r"PAYROLL_EXPORT_(\d+)_(\d+)\.xml",
        file_name
    )

    if not match:
        return None

    store = match.group(1)
    business_date = match.group(2)

    return f"{store}_{business_date}"


def get_matching_files():

    cb_folder = "cb_files"
    ac_folder = "ac_files"

    cb_files = {}
    ac_files = {}

    for file in os.listdir(cb_folder):

        if file.endswith(".xml"):

            key = get_file_key(file)

            if key:
                cb_files[key] = os.path.join(
                    cb_folder,
                    file
                )

    for file in os.listdir(ac_folder):

        if file.endswith(".xml"):

            key = get_file_key(file)

            if key:
                ac_files[key] = os.path.join(
                    ac_folder,
                    file
                )

    return cb_files, ac_files