# Intelligent Recycling Strategy Table

This is a Streamlit-based intelligent recycling strategy table application for modeling and prediction of valuable resource recycling ( including critical metals and halogens.

## Features

- Periodic table input interface
- Condition settings (temperature, oxygen partial pressure, time)
- Element recovery rate prediction
- Phase analysis (alloy phase, slag phase, gas phase)
- Debromination rate prediction

## Installation Requirements

### 1. Python Environment

Ensure your system has Python 3.8 or higher installed.

**Install Python:**
- Method 1: Download and install from [Python official website](https://www.python.org/downloads/)
- Method 2: Search and install Python from Microsoft Store

### 2. Dependencies

Run the following command to install required dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install streamlit pandas numpy scikit-learn xgboost joblib openpyxl
```

## Usage

1. Open Command Prompt or PowerShell
2. Navigate to project directory:
3. Run the application:
   ```bash
   python -m streamlit run GUI3.py
   ```

## Instructions

1. **Input Element Content**: Enter element content values in the Intelligent Recycling Strategy Table
2. **Set Conditions**:
   - T(K): Temperature (Kelvin)
   - Pre(atm): Oxygen partial pressure (atmosphere)
   - Time(s): Time (seconds)
3. **Click Submit**: Submit data for calculation
4. **View Results**: Check predicted recovery rates and phase information in the output table

## File Description

- `GUI3.py`: Main program file
- `thermo_fun.py`: Thermodynamic calculation module
- `data-thermodynamic.xlsx`: Thermodynamic data file
- `RF_Debromination_rate_Grid.joblib`: Random Forest model file
- `XGBoost_Debromination_rate_Random.json`: XGBoost model file

