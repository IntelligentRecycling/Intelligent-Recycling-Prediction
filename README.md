# Intelligent Recycling Prediction System

## Project Overview

This project is an intelligent recycling prediction system based on machine learning and thermodynamic modeling, specifically designed for precious metal recovery rate prediction and organic debromination rate prediction. The system consists of two main modules: a model training module and a Streamlit-based intelligent recycling strategy demonstration application.

## Project Structure

```
intelligent recycling strategy/
├── model_training/                                    # Model training module
│   ├── model_train/                                   # Training scripts and data
│   │   ├── train_precious_metal_recovery_models.py    # Precious metal recovery model training
│   │   ├── train_debromination_models.py              # Debromination model training
│   │   ├── precious_metal_train_dataset.xlsx          # Precious metal training dataset
│   │   ├── precious_metal_test_dataset.xlsx           # Precious metal test dataset
│   │   ├── organic_debromination_train_dataset.xlsx   # Debromination training dataset
│   │   ├── organic_debromination_test_dataset.xlsx    # Debromination test dataset
│   │   └── train_results/                             # Training results storage directory
│   ├── GUI/                                           # Gradio visualization interface
│   │   ├── GUI.py                                     # Gradio interface main program
│   │   ├── LOGO.png                                   # System logo
│   │   └── *.json                                     # Pre-trained model files
│   ├── README.md                                      # Module documentation
│   └── requirements.txt                               # Dependency package list
│
└── Streamlit-based_intelligent_recycling_strategy_application/  # Intelligent recycling strategy demonstration app
    ├── GUI3.py                                        # Streamlit main program
    ├── thermo_fun.py                                  # Thermodynamic calculation module
    ├── data-thermodynamic.xlsx                       # Thermodynamic data file
    ├── RF_Debromination_rate_Grid.joblib             # Random Forest debromination model
    ├── XGBoost_Debromination_rate_Random.json        # XGBoost debromination model
    ├── README.md                                      # Application documentation
    └── requirements.txt                               # Dependency package list
```

## Module Functions

### 1. Model Training Module (`model_training/`)

#### Precious Metal Recovery Rate Prediction
- **Supported Metals**: Au (Gold), Ag (Silver), Pd (Palladium), Pt (Platinum), Rh (Rhodium)
- **Input Features**: 37 process parameters (composition, temperature, time, etc.)
- **Model Algorithms**: XGBoost, SVM, Random Forest, AdaBoost
- **Optimization Methods**: Bayesian optimization, Grid search, Random search

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

### 2. Intelligent Recycling Strategy Demonstration Application (`Streamlit-based_intelligent_recycling_strategy_application/`)

An intelligent recycling strategy visualization application based on thermodynamic modeling and machine learning models:

#### Core Functions
- **Periodic Table Input Interface**: Intuitive element content input
- **Thermodynamic Condition Settings**: Temperature, pressure, time parameter configuration
- **Metal Recovery Rate Prediction**: Recovery rate calculation based on thermodynamic models
- **Phase Analysis**: Alloy phase, slag phase, gas phase distribution prediction
- **Debromination Rate Prediction**: Debromination efficiency prediction based on machine learning models

#### Technical Features
- **Thermodynamic Modeling**: Metal recovery calculation based on thermodynamic principles
- **Machine Learning Integration**: Integration of trained ML-models
- **Interactive Interface**: User-friendly experience provided by Streamlit framework
- **Real-time Prediction**: Instant prediction results after parameter input

## Installation and Usage

### System Requirements
- Python 3.8+
- Windows/Linux/macOS

### 1. Model Training Module Usage

#### Install Dependencies
```bash
cd model_training
pip install -r requirements.txt
```

#### Train Precious Metal Recovery Models
```bash
cd model_train
python train_precious_metal_recovery_models.py
```

#### Train Debromination Models
```bash
cd model_train
python train_debromination_models.py
```

#### Launch Gradio Prediction Interface for Precious Metal Recovery 
```bash
cd GUI
python GUI.py
```

### 2. Intelligent Recycling Strategy Demonstration Application Usage

#### Install Dependencies
```bash
cd Streamlit-based_intelligent_recycling_strategy_application
pip install -r requirements.txt
```

#### Launch Application
```bash
python -m streamlit run GUI3.py
```

## Technical Architecture

### Machine Learning Algorithms
- **XGBoost**: Gradient boosting decision tree, primary prediction algorithm
- **Random Forest**: Random forest regression
- **SVM**: Support vector machine regression
- **AdaBoost**: Adaptive boosting algorithm

### Thermodynamic Modeling
- Based on thermodynamic equilibrium principles
- Multi-phase system modeling (alloy phase, slag phase, gas phase)
- Analysis of process parameter effects including temperature, pressure, and time

### Hyperparameter Optimization
- **Bayesian Optimization**: Efficient global optimization method
- **Grid Search**: Exhaustive parameter search
- **Random Search**: Random sampling of parameter space

## Application Scenarios

### Urban Mining Development
- Precious metal recovery optimization from electronic waste
- Intelligent adjustment of process parameters
- Recovery efficiency prediction and evaluation

### Environmental Treatment
- Organic pollutant debromination treatment
- Treatment effect prediction
- Process condition optimization

### Industrial Production
- Precious metal smelting process optimization
- Production cost control
- Quality prediction and control

## Key Highlights

1. **Dual Model Integration**: Combines thermodynamic modeling and machine learning prediction
2. **Multi-Algorithm Integration**: Integrates multiple machine learning algorithms to improve prediction accuracy
3. **Visualization Interfaces**: Provides both Gradio and Streamlit interface options
4. **Real-time Prediction**: Supports real-time parameter input and result prediction

