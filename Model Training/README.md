# Model Training Module

## Overview

This module is designed for training debromination rate prediction models, utilizing machine learning algorithms to model and optimize the debromination process. It includes a complete machine learning workflow with data preprocessing, model training, hyperparameter optimization, and result evaluation.

## File Structure

```
Model Training/
├── README.md                              # Documentation
├── requirements.txt                       # Python dependencies
├── train_debromination_models.py         # Main training script
├── organic_debromination_train_dataset.xlsx  # Training dataset
├── organic_debromination_test_dataset.xlsx   # Test dataset
└── train_results/                         # Training results directory
```

## Features

### 1. Data Preprocessing
- **Data Cleaning**: Automatically handles missing values, outliers, and extreme values

### 2. Machine Learning Models
Supports four machine learning algorithms:
- **SVM (Support Vector Machine)**: Support Vector Regression
- **Random Forest**: Random Forest Regression
- **XGBoost**: Extreme Gradient Boosting
- **AdaBoost**: Adaptive Boosting Algorithm

### 3. Hyperparameter Optimization
- **Grid Search**: Grid search optimization
- **Random Search**: Random search optimization (optional)
- **Bayesian Optimization**: Bayesian optimization (optional)

### 4. Model Evaluation
- **Cross Validation**: 5-fold cross validation
- **Evaluation Metrics**: MSE, RMSE, R²
- **Result Saving**: Automatically saves models and prediction results


## Usage

### Install Dependencies
```bash
cd "Model Training"
pip install -r requirements.txt
```

### Run Training
```bash
cd "Model Training"
python train_debromination_models.py
```

### Alternative Manual Installation
If you prefer to install dependencies manually:
```bash
pip install pandas numpy scikit-learn xgboost bayesian-optimization openpyxl joblib scipy
```




