import sys, json, requests
import pandas as pd
from PyQt6 import QtWidgets, QtGui, QtCore, uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDialog
from mainwindow_ui import Ui_MainWindow# Import the generated UI class
from dialog_ui import Ui_Dialog
from removeStrategyDialog_ui import Ui_DialogRemoveStrategy

# class that inherits from QMainWindow and the generated UI class
class MainWindow(QtWidgets.QMainWindow):

    

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()  # Create an instance of the UI class
        self.ui.setupUi(self)  # Set up the UI in the main window
        self.setWindowTitle("Trade Manager")

        # Connecting the Combobox to manipulate the strategy information text boxes.
        self.ui.comboBox.currentIndexChanged.connect(self.update_text_fields)
        self.ui.actionInsert_Strategies.triggered.connect(self.open_dialog)
        self.ui.actionRemove_Strategy.triggered.connect(self.open_Remove_Strategy)
        self.ui.selectFile.clicked.connect(self.get_file_path)
        self.ui.exportData.clicked.connect(self.submit)
        self.ui.clearForm.clicked.connect(self.clear_form)
        self.ui.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTimeUtc())
        self.ui.dateTimeEdit.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        self.ui.clearForm.clicked.connect(self.clear_form)
        self.ui.lineEdit.setProperty("mandatoryField", True)

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

   

    def open_Remove_Strategy(self):
    # Pass the comboBox and combo_data references to RemoveStrategyWindow
        dialog_Remove = RemoveStrategyWindow(
            parent=self, 
            combo_box=self.ui.comboBox, 
            combo_data=self.combo_data
    )
        dialog_Remove.dialog_submitted_Strategy.connect(self.remove_strategy_option)
        dialog_Remove.exec()

    
    # Fucntion which will open up the strategy input dialog window
    def open_dialog(self):
        dialog = DialogWindow(self)
        dialog.dialog_submitted.connect(self.add_combo_option)
        dialog.exec()

    def remove_strategy_option(self, combo_option_to_remove, text_data_to_remove):
        
        del self.combo_data[combo_option_to_remove]
        self.update_text_fields()
        


        
    # 

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
        

class RemoveStrategyWindow(QtWidgets.QDialog):
    dialog_submitted_Strategy = QtCore.pyqtSignal(str, list)

    def __init__(self, parent=None, combo_box=None, combo_data=None):
        super(RemoveStrategyWindow, self).__init__(parent)
        self.ui = Ui_DialogRemoveStrategy()
        self.ui.setupUi(self)
        self.setWindowTitle("Remove Strategy")

        # Store references to the passed combo box and combo data
        self.main_combo_box = combo_box
        self.main_combo_data = combo_data

        # Populate the RemoveStrategyWindow's comboBox with items from MainWindow's comboBox
        self.populate_combo_box()

        # Connect the remove strategy method
        self.ui.buttonBox.accepted.connect(self.remove_strategy)

    def populate_combo_box(self):
        # Ensure the combo box is cleared before populating
        self.ui.comboBoxRemove.clear()

        if self.main_combo_box:
            # Populate the comboBoxRemove with items from MainWindow's comboBox
            for i in range(self.main_combo_box.count()):
                item_text = self.main_combo_box.itemText(i)
                self.ui.comboBoxRemove.addItem(item_text)

    def remove_strategy(self):
        selected_strategy = self.ui.comboBoxRemove.currentText()
        if selected_strategy in self.main_combo_data:
            # Emit signal with the strategy to remove
            self.dialog_submitted_Strategy.emit(selected_strategy, self.main_combo_data[selected_strategy])
        
        self.accept()


        # Entry point of the application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # Create the application object

    mainWindow = MainWindow()  # Create an instance of your main window class
    mainWindow.show()  # Show the main window
    sys.exit(app.exec())  # Start the application's event loop


