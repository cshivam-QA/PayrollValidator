from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox,
    QComboBox,
    QRadioButton,
)

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.run_comparison import run_comparison


class PayrollValidator(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("XML Integration Validator")

        self.resize(900, 600)

        self.cb_folder = ""
        self.ac_folder = ""
        self.cb_file = ""
        self.ac_file = ""
        self.integration = "payroll"

        layout = QVBoxLayout()
        self.integration_label = QLabel("Integration")

        self.integration_dropdown = QComboBox()
        self.integration_dropdown.addItems(
            ["Payroll", "Timekeeping", "Food Out", "Vendor Schedule"]
        )
        self.folder_radio = QRadioButton("Folder Comparison")
        self.file_radio = QRadioButton("Single File Comparison")

        self.folder_radio.setChecked(True)

        self.cb_label = QLabel("CB Folder: Not Selected")
        self.ac_label = QLabel("AC Folder: Not Selected")
        self.cb_file_label = QLabel("CB File: Not Selected")
        self.ac_file_label = QLabel("AC File: Not Selected")
        self.status_label = QLabel("Status : Ready")

        cb_button = QPushButton("Browse CB Folder")
        ac_button = QPushButton("Browse AC Folder")
        cb_file_button = QPushButton("Browse CB File")
        ac_file_button = QPushButton("Browse AC File")
        self.run_button = QPushButton("Run Validation")

        cb_button.clicked.connect(self.select_cb_folder)
        ac_button.clicked.connect(self.select_ac_folder)
        cb_file_button.clicked.connect(self.select_cb_file)
        ac_file_button.clicked.connect(self.select_ac_file)
        self.run_button.clicked.connect(self.run_validation)

        layout.addWidget(self.integration_label)
        layout.addWidget(self.integration_dropdown)
        layout.addWidget(self.folder_radio)
        layout.addWidget(self.file_radio)
        layout.addWidget(self.cb_label)
        layout.addWidget(cb_button)
        layout.addWidget(self.ac_label)
        layout.addWidget(ac_button)
        layout.addWidget(self.cb_file_label)
        layout.addWidget(cb_file_button)
        layout.addWidget(self.ac_file_label)
        layout.addWidget(ac_file_button)
        layout.addWidget(self.run_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def select_cb_folder(self):

        folder = QFileDialog.getExistingDirectory(self, "Select CB Folder")

        if folder:

            self.cb_folder = folder

            self.cb_label.setText(f"CB Folder: {folder}")

    def select_ac_folder(self):

        folder = QFileDialog.getExistingDirectory(self, "Select AC Folder")

        if folder:

            self.ac_folder = folder

            self.ac_label.setText(f"AC Folder: {folder}")

    def select_cb_file(self):

        file, _ = QFileDialog.getOpenFileName(
            self, "Select CB XML File", "", "XML Files (*.xml)"
        )

        if file:

            self.cb_file = file

            self.cb_file_label.setText(f"CB File: {file}")

    def select_ac_file(self):

        file, _ = QFileDialog.getOpenFileName(
            self, "Select AC XML File", "", "XML Files (*.xml)"
        )

        if file:

            self.ac_file = file

            self.ac_file_label.setText(f"AC File: {file}")

    def run_validation(self):
        if self.folder_radio.isChecked():
            if not self.cb_folder:
                QMessageBox.warning(self, "Validation", "Please select CB Folder")
                return
            if not self.ac_folder:
                QMessageBox.warning(self, "Validation", "Please select AC Folder")
                return
            cb_path = self.cb_folder
            ac_path = self.ac_folder
        else:
            if not self.cb_file:
                QMessageBox.warning(self, "Validation", "Please select CB File")
                return
            if not self.ac_file:
                QMessageBox.warning(self, "Validation", "Please select AC File")
                return
            cb_path = self.cb_file
            ac_path = self.ac_file

        try:
            self.status_label.setText("Status : Running Validation...")

            if self.folder_radio.isChecked():
                result = run_comparison(
                    self.cb_folder,
                    self.ac_folder,
                    self.integration_dropdown.currentText().lower(),
                )
            else:
                result = run_comparison(
                    integration=self.integration_dropdown.currentText().lower(),
                    cb_file=self.cb_file,
                    ac_file=self.ac_file,
                )

            self.status_label.setText("Status : Validation Completed")
            QMessageBox.information(
                self,
                "Validation Complete",
                f"Report Generated\n\n"
                f"Files Processed : {result['total_files']}\n\n"
                f"Report : {result['report_path']}",
            )
        except Exception as e:
            self.status_label.setText("Status : Failed")
            QMessageBox.critical(self, "Validation Error", str(e))


app = QApplication(sys.argv)

window = PayrollValidator()

window.show()

sys.exit(app.exec())
