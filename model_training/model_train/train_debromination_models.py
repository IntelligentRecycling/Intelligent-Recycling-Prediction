#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debromination Rate Prediction Model Training Script
Training and optimization of debromination rate prediction models based on machine learning algorithms
"""

import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_regression
from bayes_opt import BayesianOptimization

# Set random seed
np.random.seed(1234)

# Configure logging
logging.basicConfig(filename='train_results/debromination_results/model_optimization.log', level=logging.INFO, 
                   format='%(asctime)s:%(levelname)s:%(message)s')

def main():
    """Main function: Execute model training workflow"""
    
    # Load training data
    print("Loading training data...")
    df = pd.read_excel('organic_debromination_train_dataset.xlsx', engine='openpyxl')
    
    # Separate features X and target Y
    X = df.iloc[:, :10]
    Y = df.iloc[:, 10:]
    
    # Load test data
    print("Loading test data...")
    df_test = pd.read_excel('organic_debromination_test_dataset.xlsx', engine='openpyxl')
    test_X = df_test.iloc[:, :10]
    
    # Define model dictionary
    models = {
        'SVM': SVR(),
        'RF': RandomForestRegressor(),
        'XGBoost': XGBRegressor(),
        'Adaboost': AdaBoostRegressor()
    }
    
    # Define hyperparameter grids
    param_grids = {
        'SVM': {'C': [1, 10, 100], 'gamma': [0.001, 0.01, 0.1, 1]},
        'RF': {'n_estimators': [10, 50, 100], 'max_depth': [None, 3, 10]},
        'XGBoost': {'n_estimators': [10, 50, 100], 'max_depth': [3, 6, 10], 'learning_rate': [0.01, 0.1, 0.3]},
        'Adaboost': {'n_estimators': [10, 50, 100], 'learning_rate': [0.01, 0.1, 1]}
    }
    
    # Define hyperparameter ranges for Bayesian optimization
    param_ranges = {
        'SVM': {'C': (1, 100), 'gamma': (0.001, 1)},
        'RF': {'n_estimators': (10, 100), 'max_depth': (3, 10)},
        'XGBoost': {'n_estimators': (10, 100), 'max_depth': (3, 10), 'learning_rate': (0.01, 0.3)},
        'Adaboost': {'n_estimators': (10, 100), 'learning_rate': (0.01, 1)}
    }
    
    # Create Excel writers for saving results
    with pd.ExcelWriter('train_results/debromination_results/predicted_results.xlsx', engine='openpyxl') as writer, \
         pd.ExcelWriter('train_results/debromination_results/results.xlsx', engine='openpyxl') as writer1, \
         pd.ExcelWriter('train_results/debromination_results/predicted_VAL_results.xlsx', engine='openpyxl') as writer2:
        
        # Train models for each target variable
        for metal in Y.columns:
            print(f"\nTraining models for {metal}...")
            
            # Create DataFrames to save prediction results
            predictions_df = pd.DataFrame()
            tmp_df = pd.DataFrame()
            predictions_VAL_df = pd.DataFrame()
            
            logging.info(f"Optimizing models for {metal}")
            y = Y[metal]
            
            # Filter out y=0 data
            non_zero_indices = y != 0
            X_filtered = X[non_zero_indices]
            y_filtered = y[non_zero_indices]
            
            print(f"Filtered data shape: {y_filtered.shape}")
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X_filtered, y_filtered, test_size=0.2, random_state=42)
            
            # Train each model
            for model_name, model in models.items():
                print(f"Training {model_name}...")
                logging.info(f"Optimizing {model_name}...")
                
                # Grid Search optimization
                print(f"Optimizing {model_name} with Grid Search...")
                prefix_model = 'Grid'
                grid_search = GridSearchCV(model, param_grids[model_name], cv=5, scoring='neg_mean_squared_error')
                grid_search.fit(X_train, y_train)
                best_params = grid_search.best_params_
                
                # # Random Search optimization
                # print(f"Optimizing {model_name} with Random Search...")
                # prefix_model = 'Random'
                # random_search = RandomizedSearchCV(model, param_grids[model_name], cv=5, scoring='neg_mean_squared_error', n_iter=10, random_state=42)
                # random_search.fit(X_train, y_train)
                # best_params = random_search.best_params_
                
                # # Bayesian optimization
                # print(f"Optimizing {model_name} with Bayesian Optimization...")
                # prefix_model = 'baye'
                # bayes_params, bayes_target = bayesian_optimization(model, param_ranges[model_name], X_train, y_train)
                # best_params = bayes_params
                
                '''
                #### Select the best model when running all 3 methods simultaneously
                # Compare results from three methods and select best hyperparameters
                best_params = grid_search.best_params_
                best_score = grid_search.best_score_
                if random_search.best_score_ > best_score:
                    best_params = random_search.best_params_
                    best_score = random_search.best_score_
                if bayes_target > best_score:
                    best_params = bayes_params 
                print(f" Grid: {grid_search.best_score_}, Random: { random_search.best_score_}, bayes: {bayes_target}")
                print("#####", best_params)
                '''
                
                # Convert specific parameters to integers
                if 'n_estimators' in best_params:
                    best_params['n_estimators'] = int(best_params['n_estimators'])
                if 'max_depth' in best_params:
                    if best_params['max_depth'] is not None:
                        best_params['max_depth'] = int(best_params['max_depth'])
                
                # Train model with best hyperparameters
                model.set_params(**best_params)
                model.fit(X_train, y_train)
                
                # Save model
                if model_name == 'XGBoost':
                    model_op_name = f'train_results/debromination_results/{model_name}_{metal}_{prefix_model}.json'
                    model.save_model(model_op_name)
                else:
                    import joblib
                    model_op_name = f'train_results/debromination_results/{model_name}_{metal}_{prefix_model}.joblib'
                    joblib.dump(model, model_op_name)
                
                # Evaluate on validation set
                predictions_test = model.predict(X_test)
                mse_test = mean_squared_error(y_test, predictions_test)
                rmse_test = np.sqrt(mse_test)
                r2_test = r2_score(y_test, predictions_test)
                
                # Save validation predictions (20% split data)
                predictions_VAL_df[f'{metal}_{model_name}_Predicted'] = predictions_test
                predictions_VAL_df[f'{metal}_{model_name}_GT'] = y_test.values
                
                print(f"Ground Truth: {y_test.values}")
                print(f"Predicted: {predictions_test}")
                
                # Evaluate on training set
                predictions_train = model.predict(X_train)
                mse_train = mean_squared_error(y_train, predictions_train)
                rmse_train = np.sqrt(mse_train)
                r2_train = r2_score(y_train, predictions_train)
                
                # Predict on actual test set
                predictions_X = model.predict(test_X)
                
                # Save prediction results
                predictions_df[f'{model_name}_{prefix_model}'] = predictions_X
                
                # Save evaluation results
                result_row = {
                    'Model': f'{model_name}_{prefix_model}',
                    'MSE_Train': mse_train,
                    'RMSE_Train': rmse_train,
                    'R2_Train': r2_train,
                    'MSE_Test': mse_test,
                    'RMSE_Test': rmse_test,
                    'R2_Test': r2_test,
                    'Best_Params': str(best_params)
                }
                tmp_df = pd.concat([tmp_df, pd.DataFrame([result_row])], ignore_index=True)
                
                print(f"{model_name} - Train R2: {r2_train:.4f}, Test R2: {r2_test:.4f}")
                logging.info(f"{model_name} - Train R2: {r2_train:.4f}, Test R2: {r2_test:.4f}")
            
            # Save results to Excel
            predictions_df.to_excel(writer, sheet_name=f'{metal}_predictions', index=False)
            tmp_df.to_excel(writer1, sheet_name=f'{metal}_results', index=False)
            predictions_VAL_df.to_excel(writer2, sheet_name=f'{metal}_validation', index=False)
            
            print(f"Completed training for {metal}")
    
    print("\nModel training completed! Results saved to 'train_results/debromination_results/' directory.")


def bayesian_optimization(model, params, X_train, y_train):
    """Bayesian optimization function"""
    def train_model(**kwargs):
        # Convert specific parameters to integers
        for param in ['n_estimators', 'max_depth']:
            if param in kwargs:
                kwargs[param] = int(kwargs[param])
        
        model.set_params(**kwargs)
        return cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error').mean()
    
    optimizer = BayesianOptimization(f=train_model, pbounds=params, random_state=1)
    optimizer.maximize(n_iter=10)
    return optimizer.max['params'], optimizer.max['target']


if __name__ == "__main__":
    main()