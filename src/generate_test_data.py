import os
import random
import xml.etree.ElementTree as ET

# ==================================================
# CONFIG
# ==================================================

CB_TEMPLATE = r"CB_00748_0517.xml"

AC_TEMPLATE = r"AC_Payroll_Out_05_18_2026 07_16_47_00748.xml"

CB_OUTPUT = r"Generated_Test_Data\CB"

AC_OUTPUT = r"Generated_Test_Data\AC"

TOTAL_FILES = 500

PASS_FILES = 350

FAIL_FILES = 145

MISSING_FILES = 5


# ==================================================
# CREATE OUTPUT FOLDERS
# ==================================================

os.makedirs(CB_OUTPUT, exist_ok=True)

os.makedirs(AC_OUTPUT, exist_ok=True)


# ==================================================
# STORE DISTRIBUTION
# ==================================================

all_stores = list(range(1, TOTAL_FILES + 1))

random.shuffle(all_stores)

pass_stores = set(all_stores[:PASS_FILES])

fail_stores = set(all_stores[PASS_FILES : PASS_FILES + FAIL_FILES])

missing_stores = set(all_stores[PASS_FILES + FAIL_FILES :])


# ==================================================
# HELPERS
# ==================================================


def update_xml_data(root, store):

    root.attrib["location"] = str(store).zfill(5)

    root.attrib["date"] = "20260531"


def inject_failure(root):

    fail_type = random.choice(["H1", "JOBCODE", "DAILY", "SHIFT", "PAY_PERIOD"])

    if fail_type == "H1":

        node = root.find(".//H0/H1")

        if node is not None:

            node.attrib["fn"] = node.attrib.get("fn", "") + "_FAIL"

    elif fail_type == "JOBCODE":

        node = root.find(".//Labor/JobCodes/J")

        if node is not None:

            node.attrib["c"] = "999999"

    elif fail_type == "DAILY":

        node = root.find(".//TM0[@type='DAILY']/TM1")

        if node is not None:

            node.attrib["rh"] = "999.99"

    elif fail_type == "SHIFT":

        node = root.find(".//TM0[@type='SHIFT']/TM1")

        if node is not None:

            node.attrib["tips"] = "999.99"

    elif fail_type == "PAY_PERIOD":

        node = root.find(".//TM0[@type='PAY_PERIOD']/TM1")

        if node is not None:

            node.attrib["pay"] = "99999.99"


def get_cb_filename(store):

    if store <= 200:

        return f"PAYROLL_EXPORT_" f"{str(store).zfill(5)}" f"_20260531.xml"

    return f"Payroll_Out_" f"05_31_2026 " f"17_09_44_" f"{str(store).zfill(5)}.xml"


def get_ac_filename(store):

    if store <= 200:

        return f"PAYROLL_EXPORT_" f"{str(store).zfill(5)}" f"_20260531.xml"

    return f"Payroll_Out_" f"05_31_2026 " f"17_09_44_" f"{str(store).zfill(5)}.xml"


# ==================================================
# GENERATE FILES
# ==================================================

for store in range(1, TOTAL_FILES + 1):

    cb_tree = ET.parse(CB_TEMPLATE)

    cb_root = cb_tree.getroot()

    update_xml_data(cb_root, store)

    cb_file = os.path.join(CB_OUTPUT, get_cb_filename(store))

    cb_tree.write(cb_file, encoding="utf-8", xml_declaration=True)

    if store in missing_stores:

        continue

    ac_tree = ET.parse(AC_TEMPLATE)

    ac_root = ac_tree.getroot()

    update_xml_data(ac_root, store)

    if store in fail_stores:

        inject_failure(ac_root)

    ac_file = os.path.join(AC_OUTPUT, get_ac_filename(store))

    ac_tree.write(ac_file, encoding="utf-8", xml_declaration=True)


# ==================================================
# SUMMARY
# ==================================================

print()

print("=" * 50)

print("TEST DATASET GENERATED")

print("=" * 50)

print(f"CB FILES      : {TOTAL_FILES}")

print(f"AC FILES      : {TOTAL_FILES - MISSING_FILES}")

print(f"PASS FILES    : {PASS_FILES}")

print(f"FAIL FILES    : {FAIL_FILES}")

print(f"MISSING FILES : {MISSING_FILES}")

print()

print(f"CB Folder : {CB_OUTPUT}")

print(f"AC Folder : {AC_OUTPUT}")

print("=" * 50)
