import subprocess
import json
import sys
STOCKS_DICT = {
    "stocks": ["PETR4", "VALE3", "BBAS3", "B3SA3", "JBSS3"], #substitue for the selected tickers on the react app
    "benchmark": ['BOVA11'],# this is fixed
    "period": [6, 12, 24, 36] # substitue for the selected radiobutton on the react app
}
def run_optimization(stocks, period):
    cmd = [sys.executable, "opt.py", "--stocks", ",".join(stocks), "--period", str(period)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running optimization: {e}")
        print(f"stderr: {e.stderr}")
        return None

def test_optimization():
    stocks = STOCKS_DICT["stocks"]
    periods = STOCKS_DICT["period"]

    for period in periods:
        print(f"\nTesting optimization for period: {period} months")
        result = run_optimization(stocks, period)
        
        if result is None:
            print(f"Failed to run optimization for period {period}")
            continue

        # Check if the result contains the expected keys
        expected_keys = ["tangency_data", "min_variance_data"]
        for key in expected_keys:
            if key not in result:
                print(f"Error: Missing '{key}' in the result")
                continue

            portfolio_data = result[key]
            print(f"\n{key.replace('_', ' ').title()}:")
            
            # Check weights
            weights = portfolio_data.get("weights", {})
            print("Weights:")
            for stock, weight in weights.items():
                print(f"  {stock}: {weight:.4f}")

            # Check performance
            performance = portfolio_data.get("performance", {})
            print("Performance:")
            for metric, value in performance.items():
                print(f"  {metric}: {value:.4f}")

            # Check stats
            stats = portfolio_data.get("stats", {})
            print("Stats:")
            for metric, value in stats.items():
                print(f"  {metric}: {value}")

            # Check cumulative returns
            cum_returns = portfolio_data.get("cumulative_returns", {})
            if cum_returns:
                print("Cumulative Returns:")
                print(f"  First date: {list(cum_returns.keys())[0]}")
                print(f"  Last date: {list(cum_returns.keys())[-1]}")
                print(f"  Number of data points: {len(cum_returns)}")
            else:
                print("Error: Missing cumulative returns data")

if __name__ == "__main__":
    test_optimization()