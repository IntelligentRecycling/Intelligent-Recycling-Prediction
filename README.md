# Intelligent Recycling Prediction System

## Project Overview

This intelligent recycling strategy table provides an intelligent prediction tool for recycling valuable resources—including critical metals and strategically significant yet hazardous halogens—from urban mines (e.g., spent electronics, batteries, and catalysts). It supports rapid assessment of element phase distribution and recovery rates to guide recycling process optimization.

## Project Structure

```
Intelligent-Recycling/
├── Model Training/                                  # Model training module
│   ├── train_debromination_models.py              # Debromination model training script
│   ├── organic_debromination_train_dataset.xlsx   # Debromination training dataset
│   ├── organic_debromination_test_dataset.xlsx    # Debromination test dataset
│   ├── train_results/                             # Training results storage directory
|   └── requirements.txt                           # Dependency package list
└── Intelligent Recycling Strategy Table/          # Intelligent recycling strategy application
    ├── GUI3.py                                    # Streamlit main application
    ├── thermo_fun.py                              # Thermodynamic calculation module
    ├── data-thermodynamic.xlsx                   # Thermodynamic data file
    ├── RF_Debromination_rate_Grid.joblib         # Random Forest debromination model
    ├── XGBoost_Debromination_rate_Random.json    # XGBoost debromination model
    ├── Example data and expected output.docx     # Example data and output documentation
    ├── README.md                                  # Application documentation
    └── requirements.txt                           # Dependency package list
```

## Module Functions

### 1. Model Training Module (`model_training/`)


#### Debromination Rate Prediction
- **Prediction Target**: Organic debromination efficiency
- **Input Features**: 10 process parameters
- **Model Algorithms**: XGBoost, SVM, Random Forest, AdaBoost
- **Optimization Methods**: Bayesian optimization, Grid search, Random search

#### Training Outputs
- Optimized model files
- Prediction results Excel files
- Model evaluation metrics (R², MSE, RMSE)
- Training log files

### 2. Element-level Intelligent Recycling Strategy (`Intelligent Recycling Strategy Table`)

An element-level intelligent recycling strategy visualization application based on thermodynamic modeling and machine learning models:

#### Core Functions
- **Periodic Table Input Interface**: Intuitive element content input
- **Thermodynamic Condition Settings**: Temperature, oxygen partial pressure, time parameter configuration
- **Metal Recovery Rate Prediction**: Recovery rate calculation based on thermodynamic models
- **Phase Analysis**: Alloy phase, slag phase, gas phase distribution prediction
- **Debromination Rate Prediction**: Debromination efficiency prediction based on machine learning models

#### Technical Features
- **Thermodynamic Modeling**: Metal recovery calculation based on thermodynamic principles
- **Machine Learning Integration**: Integration of trained ML-models
- **Interactive Interface**: User-friendly experience provided by Streamlit framework
- **Real-time Prediction**: Instant prediction results after parameter input

## Installation and Usage

### Platform and Hardware Requirements
- **Operating Systems**: Windows 10/11, Linux (Ubuntu 18.04+, CentOS 7+), macOS 10.15+
- **Python Version**: Python 3.8 or higher (recommended: Python 3.9-3.11)
- **Hardware**: Standard computer CPU

### 1. Model Training Module Usage


#### Install Dependencies
```bash
cd "Model Training"
pip install -r requirements.txt
```
*Typical install time on a "normal" desktop computer: 2-5 minutes*


#### Train Debromination Models
```bash
cd "Model Training"
python train_debromination_models.py
```

### 2. Element-level Intelligent Recycling Strategy Usage


#### Install Dependencies
```bash
cd "Intelligent Recycling Strategy Table"
pip install -r requirements.txt
```
*Typical install time on a "normal" desktop computer: 2-5 minutes*


#### Launch Application
```bash
python -m streamlit run GUI3.py
```

#### Instructions

1. **Input Element Content**: Enter element content values in the periodic table
2. **Set Conditions**:
   - T: Temperature (Kelvin)
   - Pre: Oxygen partial pressure (atmosphere)
   - Time: Time (seconds)
3. **Click Submit**: Submit data for calculation
4. **View Results**: Check predicted recovery rates and phase information in the output table

*Real-time response: Prediction results are generated within seconds after parameter input.*

For detailed examples of input data formats and expected output interfaces, please refer to the **"Example data and expected output interfaces.pdf"** file in the project root directory. 


## Technical Architecture

### Machine Learning Algorithms
- **XGBoost**: Gradient boosting decision tree, primary prediction algorithm
- **Random Forest**: Random forest regression
- **SVM**: Support vector machine regression
- **AdaBoost**: Adaptive boosting algorithm

### Thermodynamic Modeling
- Based on redox reaction and multi-phase equilibrium principles
- Multi-phase system modeling (alloy phase, slag phase, gas phase)
- Analysis of process parameter effects including temperature, oxygen partial pressure and time

### Hyperparameter Optimization
- **Bayesian Optimization**: Efficient global optimization method
- **Grid Search**: Exhaustive parameter search
- **Random Search**: Random sampling of parameter space

## Purpose 

This tool is designed to aid researchers and engineers in performing fast, data-driven evaluations as well as research and development of urban mine recycling strategies. It helps in identifying optimal conditions for maximizing resource recovery and minimizing environmental impact, and shortens research and development cycles, supporting decisions in urban mining and circular economy initiatives.

## Key Highlights

1. **Dual Model Integration**: Combines thermodynamic modeling and machine learning prediction
2. **Multi-Algorithm Integration**: Integrates multiple machine learning algorithms to improve prediction accuracy
3. **Visualization Interfaces**: Provides both Gradio and Streamlit interface options
4. **Real-time Prediction**: Supports real-time parameter input and result prediction

## License
MIT License


## Troubleshooting

### Common Issues

1. **"streamlit is not recognized as an internal or external command"**
   - Ensure streamlit is installed: `pip install streamlit`
   - Check if Python environment variables are correctly set

2. **"Module not found" error**
   - Run `pip install -r requirements.txt` to install all dependencies

3. **File path error**
   - Ensure all data files are in the same directory