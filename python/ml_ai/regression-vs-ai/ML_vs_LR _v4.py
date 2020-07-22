#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 20:21:34 2020

@author: nickcostanzino
"""


def NN_structure(layers, perceptrons):

    A = list()
    for n in range(layers):
        A.append(perceptrons)
    return tuple(A)


def NN_structures(layers, perceptrons):

    A = list()

    for i in range(1, layers):
        for j in range(1, perceptrons):
            A.append(NN_structure(i, j))

    A = array(A)
    A = list(A)
    return A


def MSE(prediction, true):

    from sklearn.metrics import mean_squared_error
    mse = mean_squared_error(prediction, true)
    return mse


def process_simulator(f, sigma_X, sigma_e, N):

    import pandas as pd
    import numpy as np
    from scipy.optimize import fsolve
    from sklearn.linear_model import LinearRegression
    from sklearn.neural_network import MLPRegressor
    
    f = 'np.' + f
    
    e = np.random.normal(0,sigma_e,N)
    X = np.random.normal(0,sigma_X,N)
    Y = eval(f) + e
    
    df = pd.DataFrame()
    df['X'] = X
    df['Y'] = Y
    df['e'] = e
    
    return df


def performance_analyzer(func, sigma_X, sigma_e, N, number_of_partitions, number_of_simulations, output_folder):

    import pandas as pd
    import numpy as np
    from sklearn.metrics import r2_score, mean_squared_error
    from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, TimeSeriesSplit
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.neural_network import MLPRegressor
    
    COLUMNS = ['training_data_points', 'testing_data_points', 'LR_intercept', 'LR_slope', 'NN_layers', 'NN_perceptrons', 
               'NN_activation', 'NN_alpha', 'LR-In-Sample-R2', 'NN-In-Sample-R2', 'Best-Possible-In-Sample-R2',
               'LR-Out-Sample-R2', 'NN-Out-Sample-R2', 'Best-Possible-Out-Sample-R2']

    full_results = pd.DataFrame(columns = COLUMNS)
    
    for k in range(number_of_simulations):

        S = process_simulator(func, sigma_X, sigma_e, N)
        
        X = pd.DataFrame(S.X)
        Y = pd.DataFrame(S.Y)
        e = pd.DataFrame(S.e)

        L = len(X)
        
        for l in range(1, number_of_partitions):

            results = pd.DataFrame()
            print(l)
        
            test_L = int(L/number_of_partitions)
            train_L  = int(L/number_of_partitions*l)
            train_start = L- test_L-train_L
            train_end = L- test_L
            
            max_layers = 2
            max_perceptrons = 8
            
            structures = NN_structures(max_layers, max_perceptrons)

            print("NN_Structures:")
            print(structures)
            
            X_train = pd.DataFrame(X[train_start:train_end])
            Y_train = pd.DataFrame(Y[train_start:train_end])
            e_train = pd.DataFrame(e[train_start:train_end])
        
            X_test = pd.DataFrame(X[train_end +1: L])
            Y_test = pd.DataFrame(Y[train_end +1: L])
            e_test = pd.DataFrame(e[train_end +1: L])
            
            LR_regressor = LinearRegression(fit_intercept=True)
            LR_regressor.fit(X_train, Y_train)

            print("Fitted LR")

            NN_regressor = MLPRegressor()

            # default max_iter = 10000
            param_grid = {'hidden_layer_sizes': structures,
                               'activation': ['identity', 'relu'],
                               'alpha': [0.01, 0.001, 0.0001, 0.00001],
                               'learning_rate': ['adaptive'],
                               'solver': ['adam'],
                               'random_state': [0],
                               'early_stopping': [True],
                               'max_iter': [10000],
                               'warm_start': [True]}
            
            tscv = TimeSeriesSplit(n_splits=4)
            NN_gridsearch = GridSearchCV(estimator=NN_regressor, param_grid=param_grid, n_jobs=-1, verbose=False, cv= tscv)

            print("Performing grid search for NN")
            NN_gridsearch.fit(X_train, Y_train)
            print("Finished grid search for NN")

            NN_params = NN_gridsearch.best_params_
            NN_model = NN_gridsearch.best_estimator_
            
            LR_params = np.append([LR_regressor.intercept_], LR_regressor.coef_)
            
            pred_LR = LR_regressor.predict(X_test)
            pred_NN = NN_model.predict(X_test)
            
            insample_LR = LR_regressor.predict(X_train)
            insample_NN = NN_model.predict(X_train)
        
            results.loc[l, COLUMNS[0]] = train_L
            results.loc[l, COLUMNS[1]] = test_L
            results.loc[l, COLUMNS[2]] = LR_params[0]
            results.loc[l, COLUMNS[3]] = LR_params[1]
            results.loc[l, COLUMNS[4]] = len(NN_params['hidden_layer_sizes'])
            results.loc[l, COLUMNS[5]] = sum(NN_params['hidden_layer_sizes'])
            results.loc[l, COLUMNS[6]] = str(NN_params['activation'])
            results.loc[l, COLUMNS[7]] = str(NN_params['alpha'])
            
            results.loc[l, COLUMNS[8]] = LR_regressor.score(X_train,Y_train)
            results.loc[l, COLUMNS[9]] = NN_model.score(X_train,Y_train)
            results.loc[l, COLUMNS[10]] = 1 - (e_train*e_train).sum().values[0]/(((Y_train-Y_train.mean())*(Y_train-Y_train.mean())).sum().values[0])
            
            results.loc[l, COLUMNS[11]] = LR_regressor.score(X_test,Y_test)
            results.loc[l, COLUMNS[12]] = NN_model.score(X_test,Y_test)
            results.loc[l, COLUMNS[13]] = 1 - (e_test*e_test).sum().values[0]/(((Y_test-Y_test.mean())*(Y_test-Y_test.mean())).sum().values[0])
            
            full_results = full_results.append(results, ignore_index=False)

    full_results.to_csv(output_folder + '/' + str(func) + '_' + str(N) + '_' + str(number_of_partitions) + '_.csv')


def main():

    # default values
    # func = 'power(X,3)'
    # sigma_X=2
    # N=10000
    # number_of_partitions = 20
    # number_of_simulations=1000
    # output_folder = 'results'
    func = 'power(X,3)'
    sigma_X = 2
    N = 1000
    number_of_partitions = 2
    number_of_simulations = 1
    output_folder = 'results'

    for i in range(1):
        performance_analyzer(func, sigma_X, 0.5 * i, N, number_of_partitions, number_of_simulations, output_folder)


if __name__ == "__main__":
    main()
        
        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

    
    
    







    
    
    
    