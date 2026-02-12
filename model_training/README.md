# Precious Metal Recovery and Debromination Rate Prediction System

## Project Overview

This project is an intelligent prediction system based on machine learning, specifically designed for precious metal smelting recovery rate prediction and organic debromination rate prediction in urban mining. The system includes model training modules and a visualization prediction interface, providing data support for precious metal recovery process optimization.

## Project Structure

```
project_prediction/
├── model_train/                          # Model training module
│   ├── train_precious_metal_recovery_models.py    # Precious metal recovery model training
│   ├── train_debromination_models.py              # Debromination model training
│   ├── precious_metal_train_dataset.xlsx          # Precious metal training dataset
│   ├── precious_metal_test_dataset.xlsx           # Precious metal test dataset
│   ├── organic_debromination_train_dataset.xlsx   # Debromination training dataset
│   ├── organic_debromination_test_dataset.xlsx    # Debromination test dataset
│   └── train_results/                             # Training results storage directory
│       ├── precious_metal_results/                # Precious metal model results
│       └── debromination_results/                 # Debromination model results
├── GUI/                                   # Visualization interface module
│   ├── GUI.py                            # Gradio interface main program
│   ├── LOGO.png                          # System logo
│   └── *.json                            # Pre-trained model files
├── README.md                             # Project documentation
└── requirements.txt                      # Dependency package list
```

## Features

### 1. Model Training Module (`model_train/`)

#### Precious Metal Recovery Rate Prediction
- **Supported Metals**: Au (Gold), Ag (Silver), Pd (Palladium), Pt (Platinum), Rh (Rhodium)
- **Input Features**: 37 process parameters (composition, temperature, time, etc.)
- **Model Algorithms**: XGBoost, SVM, Random Forest, AdaBoost
- **Optimization Methods**: Bayesian optimization, Grid search, Random search

#### Debromination Rate Prediction
- **Prediction Target**: Organic debromination efficiency
- **Input Features**: 10 process parameters
- **Model Algorithms**: XGBoost, SVM, Random Forest, AdaBoost
- **Optimization Methods**: Grid search optimization

#### Training Outputs
- Optimized model files
- Prediction results Excel files
- Model evaluation metrics (R², MSE, RMSE)
- Training log files

### 2. Visualization Interface Module (`GUI/`)

- **Interface Framework**: Gradio Web application
- **Functionality**: Real-time precious metal recovery rate prediction

## Installation and Usage

### 1. Environment Requirements
- Python 3.8+
- Windows/Linux/macOS

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Model Training

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

After training completion, model files and results will be saved in the `train_results/` directory.

### 4. Launch Prediction Interface
```bash
cd GUI
python GUI.py
```

After startup, access the displayed local address in your browser (usually `http://127.0.0.1:7860`).

## Technical Architecture

### Machine Learning Algorithms
- **XGBoost**: Gradient boosting decision tree, primary prediction algorithm
- **SVM**: Support vector machine regression
- **Random Forest**: Random forest regression
- **AdaBoost**: Adaptive boosting algorithm

### Hyperparameter Optimization
- **Bayesian Optimization**: Efficient global optimization method
- **Grid Search**: Exhaustive parameter search
- **Random Search**: Random sampling of parameter space
