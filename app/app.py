from tkinter import E
from tkinter.messagebox import OKCANCEL
from turtle import title
from click import style
import sys, json, requests
import pandas as pd
from PyQt6 import QtWidgets, QtGui, QtCore, uic
from PyQt6.QtWidgets import QMessageBox
from mainwindow_ui import Ui_MainWindow  # Import the generated UI class

# Create a class that inherits from QMainWindow and the generated UI class
class MainWindow(QtWidgets.QMainWindow):

    

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()  # Create an instance of the UI class
        self.ui.setupUi(self)  # Set up the UI in the main window
        self.setWindowTitle("Trade Manager")

        # Connecting the Combobox to manipulate the strategy information text boxes.
        self.ui.comboBox.currentIndexChanged.connect(self.combobox_select_startgey)
        self.ui.selectFile.clicked.connect(self.get_file_path)
        self.ui.exportData.clicked.connect(self.submit)
        self.ui.clearForm.clicked.connect(self.clear_form)
        self.ui.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTimeUtc())
        self.ui.dateTimeEdit.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        self.ui.clearForm.clicked.connect(self.clear_form)
        self.ui.lineEdit.setProperty("mandatoryField", True)

        # Initialise UI elements
        self.target_file_path = self.ui.lineEdit
        self.select_folder_btn = self.ui.selectFile
        self.export_data_btn = self.ui.exportData
        self.strategy_name = self.ui.comboBox
        self.strategy_info = self.ui.textEdit
        self.step1 = self.ui.plainTextEdit
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


    # Define a function to handle button clicks
    def combobox_select_startgey(self, index):
        match index:
            case 0:
                self.ui.textEdit.setText("")
                self.ui.plainTextEdit.setPlainText("")
                self.ui.plainTextEdit_2.setPlainText("")
                self.ui.plainTextEdit_3.setPlainText("")
                self.ui.plainTextEdit_4.setPlainText("")
            case 1:
                self.ui.textEdit.setText("Volume Accumulation Setup is based on price rotation in a consolidated area, price is then driven higher or lower from the accumulation area. Once the Price has returned to this area a trade Long/Short can be taken.")
                self.ui.plainTextEdit.setPlainText("Price is in Rotation for a period of time, then Price id driver higher or lower. PUSH MUST BE SIGNIFICANT.")
                self.ui.plainTextEdit_2.setPlainText("Identify the heaviest volume in the accumulation phase using Volume Profile.")
                self.ui.plainTextEdit_3.setPlainText("Wait for price to retrace back into the area with heavy volume.")
                self.ui.plainTextEdit_4.setPlainText("Enter trade based on bias.")
            case 2:
                self.ui.textEdit.setText("Volume Trend Setup is based on a thin volume profile, based on the trend if price retraces to a significant volume area this allows for a trend continuation trade.")
                self.ui.plainTextEdit.setPlainText("Volume profile is usually thin due to heavy directional push.")
                self.ui.plainTextEdit_2.setPlainText("Volume profile will show volume clusters where price has enabled institutions to accumulate orders")
                self.ui.plainTextEdit_3.setPlainText("Trend must continue past the volume clusters.")
                self.ui.plainTextEdit_4.setPlainText("With trend setup highlight the heaviest volume cluster and wait for price to tap into the area to enter a trend continuation trade.")
            case 3:
                self.ui.textEdit.setText("Volume Rejection Setup is based on a very strong reaction in the market to to either news catalyst or an old strong high or low. This will create a rejection in one direction which can later be used to take a trade in the same direction of the rejection.")
                self.ui.plainTextEdit.setPlainText("Find strong rejection in either direciton.")
                self.ui.plainTextEdit_2.setPlainText("Sudden reversal after the rejection.")
                self.ui.plainTextEdit_3.setPlainText("Price returns to the rejection zone.")
                self.ui.plainTextEdit_4.setPlainText("Enter long or short around the heavy volume clusters.")
            case 4:
                self.ui.textEdit.setText("Volume Reversal Setup is based on price pushing past support or resistance levels, for this strategy price must push past these levels with heavy volume.")
                self.ui.plainTextEdit.setPlainText("Wait for price to push a past support or resistance level.")
                self.ui.plainTextEdit_2.setPlainText("Wait for price to return to the original support or resistance level.")
                self.ui.plainTextEdit_3.setPlainText("Take a reversal trade based on this setup.")
                self.ui.plainTextEdit_4.setPlainText("NOTE: THIS SETUP USUALLY HAPPENS WHEN YOU HAVE A REJECTION SETUP TRADE.")
            case 5:
                self.ui.textEdit.setText("Volume PD POC Setup is based on previous day POC where price usually makes a reaction to this level if it returns to it.")
                self.ui.plainTextEdit.setPlainText("Today's price must be significantlly higher or lower than PD POC level.")
                self.ui.plainTextEdit_2.setPlainText("Wait for price to return to this level.")
                self.ui.plainTextEdit_3.setPlainText("Take a trade where you're expecting price will reject at the POC level.")
                self.ui.plainTextEdit_4.setPlainText("NOTE: THIS TRADE USUALLY WORKS HOWEVER MARKETS CAN PUSH PAST THIS LEVEL AND NOT RESPECT IT.")

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
        
        self.strategy_name.setCurrentIndex(0)
        self.step1.setPlainText("")
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

# Entry point of the application
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # Create the application object

    mainWindow = MainWindow()  # Create an instance of your main window class
    mainWindow.show()  # Show the main window
    sys.exit(app.exec())  # Start the application's event loop


# ADD EXAMPLE BUTTON FOR EACH STRATEGY TO SHOW AN EXAMPLE OF HOW THE TRADE SHOULD LOOK. 
# GET THE EXPORT TO EXCEL TO WORK BY ONLY EXPORTING ONE ITEM
# ALLOW USER TO ENTER AND REMOVE NEW STRATGIES 
# MAKE THE RESET BUTTON WORK BY RESETING ALL FIELDS