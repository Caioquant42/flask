import numpy as np
import pandas as pd
from scipy.optimize import minimize
import pyfolio as pf
from datetime import datetime, timedelta

from querydb import query_dolphindb  # Import the function from querydb.py


STOCKS_DICT = {
	"stocks": ["PETR4","VALE3","BBAS3","B3SA3","JBSS3"]
}
ddb_data = query_dolphindb()
print(ddb_data)

def filter_stocks(ddb_data, stocks_dict):
    # Filter the DataFrame to include only the specified stocks
    filtered_data = ddb_data[ddb_data['Symbol'].isin(stocks_dict["stocks"])]
    return filtered_data

def calculate_simple_returns(filtered_data):
    # Calculate simple returns for each stock
    filtered_data['simple_return'] = filtered_data.groupby('Symbol')['AdjClose'].pct_change()
    return filtered_data

def calculate_standard_deviation(filtered_data):
    # Calculate the standard deviation of the simple returns for each stock
    std_dev = filtered_data.groupby('Symbol')['simple_return'].std().reset_index()
    std_dev.columns = ['Symbol', 'Standard_Deviation']



def portfolio_sharpe_ratio(weights, returns, cov_matrix, risk_free_rate):
    port_return = portfolio_return(weights, returns)
    port_volatility = portfolio_volatility(weights, cov_matrix)
    return (port_return - risk_free_rate) / port_volatility

def max_sharpe_ratio_portfolio(returns, cov_matrix, risk_free_rate, additional_constraints=None):
    num_assets = len(returns)
    
    def negative_sharpe_ratio(weights):
        return -portfolio_sharpe_ratio(weights, returns, cov_matrix, risk_free_rate)
    
    constraints = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    ]
    
    if additional_constraints:
        constraints.extend(additional_constraints)
    
    bounds = tuple((0, 1) for _ in range(num_assets))
    
    initial_weights = np.array([1.0/num_assets] * num_assets)
    
    result = minimize(negative_sharpe_ratio, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    
    return result.x

def calculate_cumulative_returns(df_precos, weights):
    portfolio_value = (df_precos * weights).sum(axis=1)
    cumulative_returns = (1 + portfolio_value.pct_change()).cumprod()
    return cumulative_returns

def portfolio_volatility(weights, cov_matrix):
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

def portfolio_return(weights, returns):
    return np.sum(returns * weights)

def optimize_portfolio(returns, cov_matrix, target_return, additional_constraints=None):
    num_assets = len(returns)
    
    def objective(weights):
        return portfolio_volatility(weights, cov_matrix)
    
    def constraint_return(weights):
        return portfolio_return(weights, returns) - target_return
    
    def constraint_sum(weights):
        return np.sum(weights) - 1.0
    
    constraints = [
        {'type': 'eq', 'fun': constraint_return},
        {'type': 'eq', 'fun': constraint_sum}
    ]
    
    if additional_constraints:
        constraints.extend(additional_constraints)
    
    bounds = tuple((0, 1) for asset in range(num_assets))
    
    result = minimize(objective, num_assets*[1./num_assets,], method='SLSQP', bounds=bounds, constraints=constraints)
    return result

def minimum_variance_portfolio(cov_matrix, additional_constraints=None):
    num_assets = cov_matrix.shape[0]
    
    def objective(weights):
        return portfolio_volatility(weights, cov_matrix)**2
    
    constraints = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    ]
    
    if additional_constraints:
        constraints.extend(additional_constraints)
    
    bounds = tuple((0, 1) for _ in range(num_assets))
    
    result = minimize(objective, [1./num_assets]*num_assets, method='SLSQP', bounds=bounds, constraints=constraints)
    
    return result.x

def bestallo(ddb_data, stocks, window_size):
	#Retrive dolhphin db database data and filter the selected stocks,
	## calculate log returns of AdjClose
	pass

stats = pf.timeseries.perf_stats(daily_returns)