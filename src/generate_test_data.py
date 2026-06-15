import os
import random
import shutil
import zipfile
import pandas as pd
import xml.etree.ElementTree as ET
from copy import deepcopy


SOURCE_FILE = "cb_files/PAYROLL_EXPORT_00221_20260607.xml"

STORES = [
    "00221",
    "00022",
    "00023",
    "06796",
    "08107",
    "01254",
    "01480",
    "05450",
    "07347",
    "08154"
]

DATES = [
    "20260607",
    "20260531",
    "20260524"
]

SCENARIOS = [
    "PASS",
    "VALUE_MISMATCH",
    "MISSING_ATTRIBUTE",
    "MISSING_RECORD",
    "ZERO_VALUE"
]

OUTPUT_FOLDER = "Payroll_Test_Dataset"

random.seed(123)


def save_xml(tree, file_path):
    tree.write(
        file_path,
        encoding="utf-8",
        xml_declaration=True
    )


def create_cb_file(source_tree, store, business_date, output_file):

    tree = deepcopy(source_tree)

    root = tree.getroot()

    root.set("location", store)
    root.set("date", business_date)

    save_xml(tree, output_file)


def create_ac_file(
        source_tree,
        store,
        business_date,
        scenario,
        output_file):

    tree = deepcopy(source_tree)

    root = tree.getroot()

    root.set("location", store)
    root.set("date", business_date)

    daily_node = root.find(
        ".//TM0[@type='DAILY']/TM1"
    )

    if daily_node is not None:

        if scenario == "VALUE_MISMATCH":

            daily_node.set(
                "pay",
                "999.99"
            )

        elif scenario == "MISSING_ATTRIBUTE":

            if "pay" in daily_node.attrib:
                del daily_node.attrib["pay"]

        elif scenario == "ZERO_VALUE":

            daily_node.set(
                "pay",
                "0"
            )

        elif scenario == "MISSING_RECORD":

            parent = root.find(
                ".//TM0[@type='DAILY']"
            )

            if parent is not None:
                parent.remove(daily_node)

    save_xml(tree, output_file)


def create_zip(folder_name, zip_name):

    with zipfile.ZipFile(
            zip_name,
            "w",
            zipfile.ZIP_DEFLATED) as zipf:

        for root, dirs, files in os.walk(folder_name):

            for file in files:

                full_path = os.path.join(
                    root,
                    file
                )

                relative_path = os.path.relpath(
                    full_path,
                    folder_name
                )

                zipf.write(
                    full_path,
                    relative_path
                )


def main():

    if not os.path.exists(SOURCE_FILE):

        print()
        print("Source XML not found")
        print(SOURCE_FILE)

        return

    if os.path.exists(OUTPUT_FOLDER):

        shutil.rmtree(
            OUTPUT_FOLDER
        )

    cb_folder = os.path.join(
        OUTPUT_FOLDER,
        "cb_files"
    )

    ac_folder = os.path.join(
        OUTPUT_FOLDER,
        "ac_files"
    )

    os.makedirs(
        cb_folder,
        exist_ok=True
    )

    os.makedirs(
        ac_folder,
        exist_ok=True
    )

    source_tree = ET.parse(
        SOURCE_FILE
    )

    expected_results = []

    for store in STORES:

        for business_date in DATES:

            scenario = random.choice(
                SCENARIOS
            )

            file_name = (
                f"PAYROLL_EXPORT_{store}_{business_date}.xml"
            )

            cb_file = os.path.join(
                cb_folder,
                file_name
            )

            ac_file = os.path.join(
                ac_folder,
                file_name
            )

            create_cb_file(
                source_tree,
                store,
                business_date,
                cb_file
            )

            create_ac_file(
                source_tree,
                store,
                business_date,
                scenario,
                ac_file
            )

            expected_results.append({

                "Store": store,
                "Date": business_date,
                "Scenario": scenario,
                "Expected Status":
                    "PASS"
                    if scenario == "PASS"
                    else "FAIL"

            })

    pd.DataFrame(
        expected_results
    ).to_csv(

        os.path.join(
            OUTPUT_FOLDER,
            "Expected_Results.csv"
        ),

        index=False

    )

    create_zip(
        OUTPUT_FOLDER,
        "Payroll_Test_Dataset.zip"
    )

    print()
    print("Dataset Generated Successfully")
    print("Payroll_Test_Dataset.zip")


if __name__ == "__main__":
    main()