import sys, json, requests
from unittest import result
import pandas as pd
from PyQt6 import QtWidgets, QtGui, QtCore, uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDialog, QFileDialog
from mainwindow_ui import Ui_MainWindow# Import the generated UI class
from dialog_ui import Ui_Dialog




# class that inherits from QMainWindow and the generated UI class
class MainWindow(QtWidgets.QMainWindow):

    

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()  # Create an instance of the UI class
        self.ui.setupUi(self)  # Set up the UI in the main window
        self.setWindowTitle("Trade Manager")
        self.setWindowIcon(QtGui.QIcon("assets\stock-market.png"))

        # Connecting the Combobox to manipulate the strategy information text boxes.
        self.ui.comboBox.currentIndexChanged.connect(self.update_text_fields)
        self.ui.actionInsert_Strategies.triggered.connect(self.open_dialog)
        self.ui.actionRemove_Strategy.triggered.connect(self.removeStrategy)
        self.ui.removeStrategy.clicked.connect(self.removeStrategy)
        self.ui.selectFile.clicked.connect(self.get_file_path)
        self.ui.exportData.clicked.connect(self.submit)
        self.ui.clearForm.clicked.connect(self.clear_form)
        self.ui.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTimeUtc())
        self.ui.dateTimeEdit.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        self.ui.clearForm.clicked.connect(self.clear_form)
        self.ui.lineEdit.setProperty("mandatoryField", True)
        self.ui.actionSave.triggered.connect(self.save_combo_data)
        self.ui.actionLoad.triggered.connect(self.load_combo_data)
        self.ui.actionClose.triggered.connect(self.close_Application)
        
        

        # Initialise UI elements from MainWindow
        self.target_file_path = self.ui.lineEdit
        self.select_folder_btn = self.ui.selectFile
        self.export_data_btn = self.ui.exportData
        self.strategy_name = self.ui.comboBox
        self.strategy_info = self.ui.textEdit
        self.step1 = self.ui.textEdit
        self.step2 = self.ui.plainTextEdit_2
        self.step3 = self.ui.plainTextEdit_3
        self.step4 = self.ui.plainTextEdit_4
        self.date_time = self.ui.dateTimeEdit
        self.symbol = self.ui.comboBox_2
        self.long_short = self.ui.comboBox_3
        self.entry_price = self.ui.doubleSpinBox
        self.position_size = self.ui.doubleSpinBox_2
        self.exit_price = self.ui.doubleSpinBox_3
        self.initial_invest = self.ui.doubleSpinBox_4
        self.p_l = self.ui.doubleSpinBox_5
        self.win_loss = self.ui.comboBox_4

        # A dictionary to store strategy data
        self.combo_data = {}


    # Function which allows the user to save data to a selected file path
    def save_combo_data(self):
        
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "JSON Files (*.json)")
        if file_path:
            self.save_data(file_path, self.combo_data)

    # Packs the data passed from def save_combo_data function and saves it into a json file at target file path
    def save_data(self, file_path, combo_data):
    
        try:
            with open(file_path, 'w') as file:
                json.dump(combo_data, file, indent=4)  # Save with formatting for readability
                self.save_data_complete(file_path)
        except Exception as e:
            print(f"Failed to save data: {e}")

    # Function to open load dialog window to allow users to load their data
    def load_combo_data(self):
        # Open a dialog to choose which file to load
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "JSON Files (*.json)")
        if file_path:
            global combo_data
            combo_data = self.load_data(file_path)  # Load the data into the combo_data dictionary
            self.combo_data = combo_data
            self.unpack_loaded_data(combo_data)
                   
    # Takes in the data from json file and returns combo_data to be unpacked later
    def load_data(self, file_path):
        try:
            with open(file_path, 'r') as file:
                combo_data = json.load(file)
                print(f"Data loaded from {file_path}")

                return combo_data
        except Exception as e:
            print(f"Failed to load data: {e}")
            return {}
    
    # Function to unpack json data into the combo_data dictionary
    def unpack_loaded_data(self, combo_data):
        
        combo_names = combo_data
        self.ui.comboBox.addItems(combo_names)

    # Function to remove selected strategy
    def removeStrategy(self):
        current_strategy = self.ui.comboBox.currentIndex()
        current_strategy_name = self.ui.comboBox.currentText()

        if current_strategy == -1:
            self.error_no_selected_strategy()
        
        
        else:
            reply = QMessageBox()
            reply.setWindowTitle("Attention")
            reply.setIcon(QMessageBox.Icon.Critical)
            reply.setText("Are you sure you want to remove this strategy")
            reply.setStandardButtons(QMessageBox.StandardButton.Yes | 
                     QMessageBox.StandardButton.No)

            x = reply.exec()

            if x == QMessageBox.StandardButton.Yes:
                           
                self.ui.comboBox.removeItem(current_strategy)
                del self.combo_data[current_strategy_name]
        
    # Fucntion which will open up the strategy input dialog window
    def open_dialog(self):
        dialog = DialogWindow(self)
        dialog.dialog_submitted.connect(self.add_combo_option)
        dialog.exec()
      
    # Function which will add strategies to comboBox
    def add_combo_option(self, combo_option, text_data):
        #Take the combo_option name received from Dialog window and to QComboBox 
        self.ui.comboBox.addItem(combo_option)
        # Take the combo_option as a key and add the text_data as values - text_data is a list containing all the strategy information
        self.combo_data[combo_option] = text_data

    # Updating stratgey fields based on combobox selection
    def update_text_fields(self):

       
        current_option = self.ui.comboBox.currentText()

        if current_option in self.combo_data:
            data = self.combo_data[current_option]
            self.ui.textEdit.setPlainText(data[0])  # Set the first QTextEdit
            self.ui.plainTextEdit.setPlainText(data[1])  # Set the second QTextEdit
            self.ui.plainTextEdit_2.setPlainText(data[2])  # Set the third QTextEdit
            self.ui.plainTextEdit_3.setPlainText(data[3])  # Set the fourth QTextEdit
            self.ui.plainTextEdit_4.setPlainText(data[4])  # Set the fifth QTextEdit
        else:
            # Clear all text fields if no data is found
            self.ui.textEdit.clear()
            self.ui.plainTextEdit.clear()
            self.ui.plainTextEdit_2.clear()
            self.ui.plainTextEdit_3.clear()
            self.ui.plainTextEdit_4.clear()
        
    # Open a file dialog to get the path of an excel file
    def get_file_path(self):
        # Open a folder dialog and get the selected path
        folder_path = QtWidgets.QFileDialog.getOpenFileName(self, caption="Open Folder", filter="*.xlsx")

        # Check if file path was selected
        if folder_path[0]:
            #clear any existing text in the target_file_path widget
            self.target_file_path.clear()

            # Set the selected file path in the target_file_path widget
            self.target_file_path.setText(folder_path[0])
    
    # Retrieve and validate data entered in the UI form
    def get_form_data(self):
        # Extracting values from UI input fields
        file_path = self.target_file_path.text().strip()

        # Extracting all the strategy information based on the selected strategy 
        strategy_name = self.strategy_name.currentText()
        strategy_info = self.strategy_info.toPlainText()
        step_1 = self.step1.toPlainText()
        step_2 = self.step2.toPlainText()
        step_3 = self.step3.toPlainText()
        step_4 = self.step4.toPlainText()

        # Extracting all the trade information provided by user input
        date_time = self.date_time.dateTime()
        date_time_string = date_time.toString(self.ui.dateTimeEdit.displayFormat())
        symbol = self.symbol.currentIndex()
        long_short = self.long_short.currentIndex()
        entry_price = self.entry_price.value()
        position_size = self.position_size.value()
        exit_price = self.exit_price.value()
        initial_invest = self.initial_invest.value()
        profit_loss = self.p_l.value()
        win_loss = self.win_loss.currentIndex()

        # Dictionary containing user input data
        data = {
            "Strategy Name": strategy_name,
            "Strategy Informatio": strategy_info,
            "Strategy Step 1": step_1,
            "Strategy Step 2": step_2,
            "Strategy Step 3": step_3,
            "Strategy Step 4": step_4,
            "Date & Time": date_time_string,
            "Symbol": symbol,
            "Long/Short": long_short,
            "Entry Price": entry_price,
            "Position Size": position_size,
            "Exit Price": exit_price,
            "Initial Investment": initial_invest,
            "P&L": profit_loss,
            "Win/Loss": win_loss
            }
        
              
        return file_path, data

    # Method to clear the form fields
    def clear_form(self):
        
        self.strategy_name.setCurrentIndex(-1)
        self.step1.setText("")
        self.step2.setPlainText("")
        self.step3.setPlainText("")
        self.step4.setPlainText("")
        self.date_time.setDateTime(QtCore.QDateTime.currentDateTimeUtc())
        self.symbol.setCurrentIndex(0)
        self.long_short.setCurrentIndex(0)
        self.entry_price.setValue(2000.00)
        self.position_size.setValue(1.00)
        self.exit_price.setValue(2000.00)
        self.initial_invest.setValue(0.00)
        self.p_l.setValue(0.00)
        self.win_loss.setCurrentIndex(0)
    
    # Method to submit form data to an excel file
    def submit(self):
        
        data = self.get_form_data()
            
        # Unpack data taken from get form data function 
        file_path = data[0]
        user_data = data[1]
        
        # check if file path is empty, if empty raise an error
        if file_path == "":
            self.error_box_message()
            
        # If file path is valid then export the data
        else:
            df = pd.read_excel(file_path)
            user_df = pd.DataFrame(user_data, index=[0])
            new_df = pd.concat([df, user_df], ignore_index=True)
            new_df.to_excel(file_path, index=False)
            self.export_complete_message()
            self.clear_form()
    
    # Message window appearing when no target file is allocated
    def error_box_message(self):
        
       QMessageBox.information(self, "Information", "Select valid target file.")

    # Message window appearing when export is complete
    def export_complete_message(self):
        
        QMessageBox.information(self, "Export Complete", "Data has been exported to target file.")
    
    # Error shown when no strategy is selected whilst trying to remove it
    def error_no_selected_strategy(self):
        QMessageBox.information(self, "No Strategy selected", "Select a valid strategy to delete.")

    # User message when save data action is complete
    def save_data_complete(self, file_path):
        QMessageBox.information(self, f"Save Complete", f"File has been saved successfuly to: {file_path}")

    # Links the Close QAction in file dropdown menu to close application
    def close_Application(self):
        sys.exit()

# Class for dialog
class DialogWindow(QtWidgets.QDialog):

    dialog_submitted = QtCore.pyqtSignal(str, list)

    def __init__(self, parent=None):
        super(DialogWindow, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Strategy Setup")
        
        # Connect Dialog Buttons
        self.ui.buttonBox.accepted.connect(self.load_strategy_data)
        # Initialise UI elements
        

    def load_strategy_data(self):
        
        combo_option = self.ui.strategyNameEdit.toPlainText()

        text_data = [
            self.ui.strategyOverviewEdit.toPlainText(),
            self.ui.strategySetup1.toPlainText(),
            self.ui.strategySetup2.toPlainText(),
            self.ui.strategySetup3.toPlainText(),
            self.ui.strategySetup4.toPlainText()
        ]

        self.dialog_submitted.emit(combo_option, text_data)
        
        self.accept()
        


# Entry point of the application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # Create the application object

    mainWindow = MainWindow()  # Create an instance of your main window class
    mainWindow.show()  # Show the main window
    sys.exit(app.exec())  # Start the application's event loop


