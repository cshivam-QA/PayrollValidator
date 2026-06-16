from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QMessageBox
)

import sys
import os

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "src"
    )
)

from src.run_comparison import run_comparison


class PayrollValidator(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "CB to AC Payroll Validation Tool"
        )

        self.resize(
            900,
            600
        )

        self.cb_folder = ""
        self.ac_folder = ""

        layout = QVBoxLayout()

        self.cb_label = QLabel(
            "CB Folder: Not Selected"
        )

        self.ac_label = QLabel(
            "AC Folder: Not Selected"
        )

        self.status_label = QLabel(
            "Status : Ready"
        )

        cb_button = QPushButton(
            "Browse CB Folder"
        )

        ac_button = QPushButton(
            "Browse AC Folder"
        )

        self.run_button = QPushButton(
            "Run Validation"
        )

        cb_button.clicked.connect(
            self.select_cb_folder
        )

        ac_button.clicked.connect(
            self.select_ac_folder
        )

        self.run_button.clicked.connect(
            self.run_validation
        )

        layout.addWidget(
            self.cb_label
        )

        layout.addWidget(
            cb_button
        )

        layout.addWidget(
            self.ac_label
        )

        layout.addWidget(
            ac_button
        )

        layout.addWidget(
            self.run_button
        )

        layout.addWidget(
            self.status_label
        )

        self.setLayout(
            layout
        )

    def select_cb_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select CB Folder"
        )

        if folder:

            self.cb_folder = folder

            self.cb_label.setText(
                f"CB Folder: {folder}"
            )

    def select_ac_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select AC Folder"
        )

        if folder:

            self.ac_folder = folder

            self.ac_label.setText(
                f"AC Folder: {folder}"
            )

    def run_validation(self):

        if not self.cb_folder:

            QMessageBox.warning(
                self,
                "Validation",
                "Please select CB Folder"
            )

            return

        if not self.ac_folder:

            QMessageBox.warning(
                self,
                "Validation",
                "Please select AC Folder"
            )

            return

        try:

            self.status_label.setText(
                "Status : Running Validation..."
            )

            result = run_comparison(
                self.cb_folder,
                self.ac_folder
            )

            self.status_label.setText(
                "Status : Validation Completed"
            )

            QMessageBox.information(
                self,
                "Validation Complete",
                f"Report Generated\n\n"
                f"Files Processed : {result['total_files']}\n\n"
                f"Report : {result['report_path']}"
            )

        except Exception as e:

            self.status_label.setText(
                "Status : Failed"
            )

            QMessageBox.critical(
                self,
                "Validation Error",
                str(e)
            )


app = QApplication(
    sys.argv
)

window = PayrollValidator()

window.show()

sys.exit(
    app.exec()
)