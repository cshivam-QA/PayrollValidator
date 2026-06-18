# XML Integration Validation Framework

A Python-based XML Validation and Comparison Tool designed to validate CB (CloudBridge) and AC (AnyConnector) integration outputs.

The tool compares XML files node-by-node, identifies differences, missing records, duplicate records, and generates a consolidated Excel report for QA validation.

---

## Features

### Payroll Validation

* Employee Master (H1)
* Employee Attributes (NV)
* Job Codes
* Daily Labor
* Shift Data
* Exceptions
* Weekly Payroll Summary
* Missing Record Detection
* Duplicate Record Detection
* Zero Value Detection

### Timekeeping Validation

* Employee Master Validation
* Employee Attributes Validation
* Daily Labor Validation
* Shift Validation
* Exception Validation
* Weekly Validation
* Job Code Validation

### Food Out Validation

* Inventory Type Validation
* Inventory Group Validation
* GL Code Validation
* Inventory Daily Validation
* Delivery Validation
* Credit Memo Validation
* Inventory Count Validation
* Inventory Transfer Validation
* Waste Validation

---

## Supported Integrations

* Payroll Out
* Timekeeping Out
* Food Out

---

## Comparison Capabilities

The validator performs:

* Node-Level Comparison
* Attribute-Level Comparison
* Missing Record Detection
* Missing Attribute Detection
* Duplicate Record Detection
* Zero Value Detection
* Value Mismatch Detection

---

## Report Output

The tool generates an Excel report containing:

### MASTER_SUMMARY

Overall comparison status for each file pair.

### ALL_DIFFERENCES

All attribute-level mismatches.

### ALL_MISSING_RECORDS

Records missing in CB or AC.

### ALL_ZERO_VALUES

Zero value records identified during validation.

### ALL_DUPLICATES

Duplicate records detected during comparison.

---

## Technology Stack

* Python 3.x
* PySide6 (Desktop UI)
* OpenPyXL (Excel Reporting)
* XML ElementTree
* PyInstaller

---

## Project Structure

src/

* comparator.py
* file_matcher.py
* key_builder.py
* xml_loader.py
* report_generator.py
* master_report_generator.py
* run_comparison.py

Configuration Files

* payroll_config.py
* timekeeping_config.py
* foodout_bww_config.py
* foodout_arbys_config.py
* foodout_lc_config.py

Desktop Application

* desktop_app.py

---

## How to Run

### Desktop Application

```bash
py desktop_app.py
```

### Generate EXE

```bash
pyinstaller desktop_app.spec
```

---

## Version History

### V1.0

* Payroll Validation Support

### V2.0

* Excel Reporting
* Missing Record Detection
* Duplicate Detection

### V3.0

* Timekeeping Integration Support
* Enhanced Reporting

### V3.2

* Food Out Integration Support
* Client-Specific Food Out Configurations
* Improved XML Comparison Logic
* Enhanced Validation Framework

## V3.3

### Release Highlights

- Added Vendor Schedule Integration
- Added Single File Comparison Mode
- Added XML Structure Validation
- Added Invalid Integration Detection
- Excluded TRH Attribute from Comparison
- Improved Validation Reliability

---

## Author

Shivam Chaurasia

Senior QA Analyst

XML Integration Validation Framework
