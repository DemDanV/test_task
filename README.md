# Project Overview

This Python project, developed using **Python 3**, **PyQt5**, **h5py**, **numpy**, **scipy**, and **pyqtgraph**, implements a GUI application that displays a table and a graph. The project demonstrates handling data stored in a 2D numpy array and offers functionality for editing, saving, and visualizing data interactively.

## Key Features

### 1. Window Structure
- The window contains a **QTableView** displaying numeric data and a graph below the table.
- All data is stored in a **2D numpy array**.

### 2. Table Functionality
- **Editable Column**: One column allows editing values through a dropdown list, limiting selection to integers between 1 and 5.
- **Calculated Column**: Another column automatically recalculates its values based on the data from another column in the same row (signal-based mechanism).
- **Accumulated Values**: One column shows accumulated values derived from another column (also signal-based).
- **Conditional Formatting**: Cells in one column are highlighted in red or green depending on whether the values are negative or positive.

### 3. Graph Functionality
- **Dynamic Plotting**: When selecting two columns, a plot is generated to show the relationship between the second column (y-axis) and the first column (x-axis) using **pyqtgraph**.

### 4. Data Management
- **Save and Load Data**: Buttons allow saving the numpy array to a text file or HDF5 file, and loading the data from either format.
- **Array Management**: Users can adjust the size of the numpy array and fill it with random values, excluding special columns that are auto-calculated.
  
### 5. Extended Features (Optional)
- **HDF5 Dataset Interaction**: An alternative version of the application is available, where data is stored and manipulated directly from an HDF5 dataset without intermediate numpy array caching.

### 6. Code Quality and Optimization
- **Vectorized Calculations**: All operations on the numpy array are vectorized, avoiding loops for tasks such as sum calculations.
- **Thorough Code Documentation**: The code is heavily commented, explaining the purpose and function of each section in detail (comments describe the "what" and "why", not the "how").

---

This project demonstrates the use of Python with PyQt5 and associated libraries for creating a user-friendly, interactive data manipulation interface, with efficient handling and visualization of numerical data.
