
# Trade Manager - PyQt6 Application

This is a **Trade Manager** application built using **PyQt6**. It provides an interface for managing and tracking trading strategies. Users can insert strategies, update them, remove them, and export data to Excel files.

## Features

- **Custom Window Icon**: A custom icon is set for the window, located in the `assets/` folder.
- **Insert Strategies**: Users can input new trading strategies via a dialog window.
- **Update Strategy Fields**: Information related to a selected strategy is displayed and can be updated dynamically.
- **Remove Strategies**: Users can delete trading strategies from the list.
- **Save and Load Strategies**: Users can save all entered strategies to a file and load them back at a later time.
- **Export Data to Excel**: Users can export their trading data to an Excel file.
- **Clear Form**: Users can reset the form to its default state with one click.

## Installation and Setup

1. Clone the repository or download the source code.
2. Ensure you have the following dependencies installed:
    - `PyQt6`
    - `pandas`
    - `requests`
3. Install the required dependencies using the following command:
    ```bash
    pip install -r requirements.txt
    ```

4. Set the correct paths for the application’s assets (icons, data files, etc.) in the `app.py` file.

## Usage

1. **Run the Application**:
    ```bash
    python app.py
    ```

2. The main window will appear with options to:
   - Insert new strategies
   - Save and load strategy data
   - Export entered data to Excel
   - Clear the form

3. **Inserting Strategies**:
   - Navigate to **File > Insert Strategies** to open the dialog window.
   - Enter the strategy information and save it. It will be added to the dropdown.

4. **Saving/Loading Data**:
   - To save the strategies, go to **File > Save**.
   - To load previously saved strategies, go to **File > Load**.

5. **Exporting to Excel**:
   - Specify the target Excel file path, and then click on "Export Data."

## File Structure

```
app/
├── assets/
│   └── stock-market.png         # Icon for the application window
├── app.py                       # Main application file
├── mainwindow_ui.py              # Generated UI class for main window
├── dialog_ui.py                  # Generated UI class for dialog window
├── trade_data.xlsx               # Example Excel file for exporting/importing
└── README.md                     # This file
```

## Key Classes

- **MainWindow**: The main window of the application where users can add, remove, or update strategies.
- **DialogWindow**: A dialog window for adding new strategies.
- **Strategy Handling**: Strategies are managed using a `combo_data` dictionary where each key is a strategy name and the value is the related data.

## Customization

- To change the application icon, replace the `stock-market.png` file in the `assets` directory or update the path in `app.py`:
  ```python
  self.setWindowIcon(QtGui.QIcon("assets/stock-market.png"))
  ```

## Dependencies

- **PyQt6**: For building the graphical user interface.
- **Pandas**: For handling the data and exporting it to Excel.
- **Requests**: This module is imported but not used in the current version of the app.

## License

This project is licensed under the MIT License.
