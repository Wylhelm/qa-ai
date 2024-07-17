from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QLabel, QListWidget, QHBoxLayout, QScrollArea, QGridLayout, QLineEdit, QMessageBox, QInputDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
import os
from test_scenario import TestScenario
import os

class MainWindow(QMainWindow):
    def __init__(self, ai_processor, database, image_processor):
        super().__init__()
        self.ai_processor = ai_processor
        self.database = database
        self.image_processor = image_processor
        self.processed_files = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Test Scenario Generator')
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Logos
        logo_layout = QHBoxLayout()
        
        # CGI Logo
        self.cgi_logo_label = QLabel()
        self.cgi_logo_pixmap = QPixmap("CGI1.jpeg")
        self.cgi_logo_label.setPixmap(self.cgi_logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        logo_layout.addWidget(self.cgi_logo_label, alignment=Qt.AlignLeft)
        
        # Spacer
        logo_layout.addStretch()
        
        # Prototype Logo
        self.prototype_logo_label = QLabel()
        prototype_logo_path = os.path.join(os.path.dirname(__file__), "prototype.png")
        self.prototype_logo_pixmap = QPixmap(prototype_logo_path)
        self.prototype_logo_label.setPixmap(self.prototype_logo_pixmap.scaled(300, 300, Qt.KeepAspectRatio))
        logo_layout.addWidget(self.prototype_logo_label, alignment=Qt.AlignRight)
        
        layout.addLayout(logo_layout)
        self.new_scenario_button = QPushButton('Create New Scenario')
        self.new_scenario_button.clicked.connect(self.create_new_scenario)
        layout.addWidget(self.new_scenario_button)

        self.scenario_name_input = QLineEdit()
        self.scenario_name_input.setPlaceholderText("Scenario name...")
        self.scenario_name_input.setEnabled(False)
        layout.addWidget(self.scenario_name_input)

        self.criteria_input = QTextEdit()
        self.criteria_input.setPlaceholderText("Enter criteria here...")
        self.criteria_input.setEnabled(False)
        self.criteria_input.setMinimumHeight(200)  # Set minimum height to match scenario output
        layout.addWidget(self.criteria_input)

        self.upload_files_button = QPushButton('Upload Documents (Word/PDF/TXT)')
        self.upload_files_button.clicked.connect(self.upload_files)
        self.upload_files_button.setEnabled(False)
        layout.addWidget(self.upload_files_button)


        self.generate_button = QPushButton('Generate Test Scenario')
        self.generate_button.clicked.connect(self.generate_scenario)
        layout.addWidget(self.generate_button)


        self.export_button = QPushButton('Export Scenario')
        self.export_button.clicked.connect(self.export_scenario)
        layout.addWidget(self.export_button)

        # Scenario Output Area
        self.scenario_output = QTextEdit()
        self.scenario_output.setReadOnly(True)
        self.scenario_output.setMinimumHeight(200)  # Set minimum height to match criteria input
        layout.addWidget(self.scenario_output)

        # Scenario History Section
        history_layout = QVBoxLayout()
        history_layout.addWidget(QLabel("Scenario History:"))
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.display_scenario)
        history_layout.addWidget(self.history_list)
        
        # Clear History Button
        self.clear_history_button = QPushButton('Clear History')
        self.clear_history_button.clicked.connect(self.clear_scenario_history)
        history_layout.addWidget(self.clear_history_button)

        layout.addLayout(history_layout)
        
        # Quit Button
        self.quit_button = QPushButton('Quit')
        self.quit_button.clicked.connect(self.close)
        layout.addWidget(self.quit_button, alignment=Qt.AlignBottom)

        self.load_scenario_history()

    def create_new_scenario(self):
        scenario_name, ok = QInputDialog.getText(self, 'New Scenario', 'Enter the scenario name:')
        if ok and scenario_name:
            self.scenario_name_input.setText(scenario_name)
            self.criteria_input.clear()
            self.scenario_output.clear()
            self.processed_files = []
            self.enable_inputs()
        else:
            QMessageBox.warning(self, 'Error', 'You must enter a scenario name to continue.')

    def enable_inputs(self):
        self.scenario_name_input.setEnabled(True)
        self.criteria_input.setEnabled(True)
        self.upload_files_button.setEnabled(True)

    def upload_files(self):
        file_names, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "Documents (*.doc *.docx *.pdf *.txt)")
        if file_names:
            self.processed_files = []  # Clear previous processed files
            for file_name in file_names:
                processed_data = self.ai_processor.process_file(file_name)
                self.processed_files.append(processed_data)
            
            # Update criteria input with extracted information
            extracted_info = "\n".join([f"File {i+1}:\n{data.get('extracted_info', '')}\n" for i, data in enumerate(self.processed_files) if 'error' not in data])
            current_criteria = self.criteria_input.toPlainText()
            updated_criteria = f"{current_criteria}\n\nExtracted information from files:\n\n{extracted_info}"
            self.criteria_input.setPlainText(updated_criteria)
            
            # Display confirmation or error message
            if any('error' in data for data in self.processed_files):
                error_messages = [
                    (f"File {i+1}: {data['error']}\n"
                     f"Debug: {data.get('debug_info', 'No debug information available.')}")
                    for i, data in enumerate(self.processed_files) if 'error' in data
                ]
                QMessageBox.warning(self, "Analysis Errors", f"Errors occurred during file analysis:\n\n" + "\n\n".join(error_messages))
                self.scenario_output.setPlainText("Errors occurred during analysis. Please check the files and try again.")
            else:
                self.scenario_output.setPlainText(f"{len(file_names)} file(s) uploaded and analyzed successfully. Please adjust the criteria if necessary before generating the scenario.")


    def generate_scenario(self):
        scenario_name = self.scenario_name_input.text()
        criteria = self.criteria_input.toPlainText()
        if not scenario_name:
            QMessageBox.warning(self, 'Error', 'Please create a new scenario and give it a name first.')
            return
        if not self.processed_files:
            self.scenario_output.setPlainText("Please upload files (images or documents) first.")
            return
        
        scenario = self.ai_processor.generate_scenario(criteria, self.processed_files)
        scenario_with_name = f"Scenario Name: {scenario_name}\n\n{scenario}"
        self.scenario_output.setPlainText(scenario_with_name)

        # Save the scenario to the database
        test_scenario = TestScenario(scenario_name, criteria, scenario_with_name, self.processed_files)
        self.database.save_scenario(test_scenario)
        self.load_scenario_history()

    def export_scenario(self):
        scenario = self.scenario_output.toPlainText()
        if scenario:
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Scenario", "", "Text Files (*.txt)")
            if file_name:
                with open(file_name, 'w') as f:
                    f.write(scenario)

    def load_scenario_history(self):
        self.history_list.clear()
        scenarios = self.database.get_scenarios()
        for scenario in scenarios:
            # Use the scenario name as the main identifier
            scenario_name = scenario.name
            # Get the first line of the criteria
            first_line = scenario.criteria.split('\n')[0].strip()
            # Truncate if it's too long
            criteria_summary = (first_line[:30] + '...') if len(first_line) > 30 else first_line
            self.history_list.addItem(f"{scenario_name} - Criteria: {criteria_summary}")

    def display_scenario(self, item):
        scenario_name = item.text().split(" - ", 1)[0].strip()
        scenarios = self.database.get_scenarios()
        matching_scenario = next((s for s in scenarios if s.name == scenario_name), None)
        if matching_scenario:
            self.scenario_name_input.setText(matching_scenario.name)
            self.scenario_output.setPlainText(matching_scenario.scenario_text)
            self.criteria_input.setPlainText(matching_scenario.criteria)
            self.processed_files = matching_scenario.processed_files
        else:
            self.scenario_output.setPlainText("Scenario not found.")
            self.scenario_name_input.clear()
            self.criteria_input.clear()
            self.processed_files = []
            self.update_thumbnails()

    def clear_scenario_history(self):
        reply = QMessageBox.question(self, 'Clear History', 'Are you sure you want to clear the scenario history? This will delete all stored data.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.database.clear_history()
            self.load_scenario_history()
            self.scenario_name_input.clear()
            self.criteria_input.clear()
            self.scenario_output.clear()
            self.processed_files = []

    def enable_inputs(self):
        self.scenario_name_input.setEnabled(True)
        self.criteria_input.setEnabled(True)
        self.upload_files_button.setEnabled(True)
