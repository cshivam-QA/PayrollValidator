from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
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

        self.resize(1200, 600)
        self.setStyleSheet("""
QWidget {
    background-color: #1e1e1e;
    color: white;
    font-family: Segoe UI;
    font-size: 11pt;
}
    QRadioButton {
    spacing: 8px;
    font-size: 14px;
    color: white;
}

QRadioButton::indicator {
    width: 16px;
    height: 16px;
}
 QLineEdit {
    background-color: #2d2d30;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 6px;
    color: white;
}                          

QPushButton {
    background-color: #0078d4;
    color: white;
    border-radius: 8px;
    padding: 8px;
}

QPushButton:hover {
    background-color: #1f8fff;
}

QComboBox {
    background-color: #2d2d30;
    border: 1px solid #555;
    border-radius: 6px;
    padding: 6px;
}

QLabel {
    color: white;
}

QRadioButton {
    spacing: 8px;
    margin-right: 20px;                      
}
    QPushButton#runButton {
    background-color: #28a745;
    font-weight: bold;
    font-size: 12pt;
    padding: 10px;
}

QPushButton#runButton:hover {
    background-color: #34c759;
}
    python desktop_app.py#statusLabel {
    background-color: #252526;
    border: 1px solid #3c3c3c;
    border-radius: 8px;
    padding: 8px;
    font-weight: bold;
}
""")
        self.cb_folder = ""
        self.ac_folder = ""
        self.cb_file = ""
        self.ac_file = ""
        self.integration = "payroll"

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("XML Integration Validator")
        title.setStyleSheet("""
        font-size: 22pt;
        font-weight: bold;
        color: #4da6ff;
        """)

        subtitle = QLabel("Compare CB and AC Integration XML Files")
        subtitle.setStyleSheet("""
        font-size: 10pt;
        color: #cccccc;
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        self.integration_label = QLabel("Integration")

        self.integration_dropdown = QComboBox()
        self.integration_dropdown.setFixedHeight(38)
        self.integration_dropdown.addItems(
            ["Payroll", "Timekeeping", "Food Out", "Vendor Schedule", "Labor Forecast", "Schedule Out"]
        )
        self.folder_radio = QRadioButton("Folder Comparison")
        self.file_radio = QRadioButton("Single File Comparison")

        self.folder_radio.setChecked(True)
        self.folder_radio.toggled.connect(self.update_mode)
        self.cb_label = QLabel("CB Folder")
        self.ac_label = QLabel("AC Folder")

        self.cb_path = QLineEdit()
        self.cb_path.setReadOnly(True)
        self.cb_path.setPlaceholderText("Select CB Folder")

        self.ac_path = QLineEdit()
        self.ac_path.setReadOnly(True)
        self.ac_path.setPlaceholderText("Select AC Folder")

        self.cb_file_path = QLineEdit()
        self.cb_file_title = QLabel("CB File")
        self.ac_file_title = QLabel("AC File")
        self.cb_file_path.setReadOnly(True)
        self.cb_file_path.setPlaceholderText("Select CB XML File")

        self.ac_file_path = QLineEdit()
        self.ac_file_path.setReadOnly(True)
        self.ac_file_path.setPlaceholderText("Select AC XML File")

        self.cb_file_label = QLabel("CB XML File")
        self.ac_file_label = QLabel("AC XML File")
        self.status_label = QLabel("🟢 Ready")
        self.status_label.setObjectName("statusLabel")

        self.cb_button = QPushButton("Browse CB Folder")
        self.ac_button = QPushButton("Browse AC Folder")
        self.cb_file_button = QPushButton("Browse CB File")
        self.ac_file_button = QPushButton("Browse AC File")
        self.cb_button.setFixedWidth(140)
        self.ac_button.setFixedWidth(140)
        self.cb_file_button.setFixedWidth(140)
        self.ac_file_button.setFixedWidth(140)
        cb_layout = QHBoxLayout()
        cb_layout.addWidget(self.cb_path)
        cb_layout.addWidget(self.cb_button)

        ac_layout = QHBoxLayout()
        ac_layout.addWidget(self.ac_path)
        ac_layout.addWidget(self.ac_button)

        cb_file_layout = QHBoxLayout()
        cb_file_layout.addWidget(self.cb_file_path)
        cb_file_layout.addWidget(self.cb_file_button)
        self.cb_file_container = QWidget()
        self.cb_file_container.setLayout(cb_file_layout)

        ac_file_layout = QHBoxLayout()
        ac_file_layout.addWidget(self.ac_file_path)
        ac_file_layout.addWidget(self.ac_file_button)
        self.ac_file_container = QWidget()
        self.ac_file_container.setLayout(ac_file_layout)
        self.run_button = QPushButton("▶ Run Comparison")
        self.run_button.setFixedHeight(45)
        self.run_button.setObjectName("runButton")

        self.cb_button.clicked.connect(self.select_cb_folder)
        self.ac_button.clicked.connect(self.select_ac_folder)
        self.cb_file_button.clicked.connect(self.select_cb_file)
        self.ac_file_button.clicked.connect(self.select_ac_file)
        self.run_button.clicked.connect(self.run_validation)

        layout.addWidget(self.integration_label)
        layout.addWidget(self.integration_dropdown)
        radio_layout = QHBoxLayout()

        radio_layout.addWidget(self.folder_radio)
        radio_layout.addWidget(self.file_radio)

        radio_layout.addStretch()
        layout.addLayout(radio_layout)

        layout.addWidget(self.cb_label)
        layout.addLayout(cb_layout)

        layout.addWidget(self.ac_label)
        layout.addLayout(ac_layout)

        layout.addWidget(self.cb_file_title)
        layout.addWidget(self.cb_file_container)

        layout.addWidget(self.ac_file_title)
        layout.addWidget(self.ac_file_container)

        layout.addWidget(self.run_button)
        layout.addWidget(self.status_label)

        self.update_mode()
        self.setLayout(layout)

    def select_cb_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select CB Folder")
        if folder:
            self.cb_folder = folder
            self.cb_path.setText(folder)

    def select_ac_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select AC Folder")
        if folder:
            self.ac_folder = folder
            self.ac_path.setText(folder)

    def select_cb_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Select CB XML File", "", "XML Files (*.xml)"
        )
        if file:
            self.cb_file = file
            self.cb_file_path.setText(file)

    def select_ac_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Select AC XML File", "", "XML Files (*.xml)"
        )
        if file:
            self.ac_file = file
            self.ac_file_path.setText(file)

    def update_mode(self):
        folder_mode = self.folder_radio.isChecked()

        self.cb_label.setVisible(folder_mode)
        self.ac_label.setVisible(folder_mode)

        self.cb_path.setVisible(folder_mode)
        self.ac_path.setVisible(folder_mode)

        self.cb_button.setVisible(folder_mode)
        self.ac_button.setVisible(folder_mode)

        self.cb_file_title.setVisible(not folder_mode)
        self.ac_file_title.setVisible(not folder_mode)

        self.cb_file_container.setVisible(not folder_mode)
        self.ac_file_container.setVisible(not folder_mode)
        
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
            self.status_label.setText("🟡 Running Comparison...")

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

            self.status_label.setText("🟢 Comparison Completed")
            QMessageBox.information(
                self,
                "Validation Complete",
                f"Report Generated\n\n"
                f"Files Processed : {result['total_files']}\n\n"
                f"Report : {result['report_path']}",
            )
        except Exception as e:
            self.status_label.setText("🔴 Failed")
            QMessageBox.critical(self, "Validation Error", str(e))


app = QApplication(sys.argv)

window = PayrollValidator()

window.show()

sys.exit(app.exec())
