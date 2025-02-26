from dolphindb import session
import numpy as np
import pandas as pd
import argparse
import sys
import json
import traceback
import os
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from apps.utils.dict import TICKERS_DICT

survival_tickers = TICKERS_DICT.get('TOP100', [])
thresholds = [-0.03, -0.05, -0.07]


def query_dolphindb():
    # Connect to the DolphinDB server
    s = session()
    s.connect("46.202.149.154", 8848, "admin", "123456")

    # Load the table from the distributed file system
    s.run('t = loadTable("dfs://yfs", "stockdata_1d")')

    # Execute the query to filter the data by Time and select specific columns
    # Use a proper datetime format with T separating the date and time
    ddb_data = s.run('select Datetime, Symbol, AdjClose from t where Datetime > 2000.01.01T03:00:00')
    
    return ddb_data

def hist_interarrival(historical_data, threshold=-0.05):
    below_threshold = historical_data[historical_data['log_return'] < threshold]
    timestamps_sorted = below_threshold.index.sort_values()
    interarrival_time = timestamps_sorted.to_series().diff().dropna()
    return interarrival_time.dt.days

def kaplan_meier_estimator_with_cumulative_hazard(interarrival_days, specific_day=None):
    interarrival_days = interarrival_days.sort_values()

    if interarrival_days.empty:
        return 1.0, 0.0, 0.0  # Return default values when no data points meet the criteria

    n = len(interarrival_days)
    event_counts = interarrival_days.value_counts().sort_index()
    
    survival_prob = 1.0
    cumulative_hazard = 0.0
    survival_probs = []
    hazard_rates = []
    cumulative_hazards = []

    for t, d in event_counts.items():
        at_risk = n
        survival_prob *= (1 - d / at_risk)
        survival_probs.append(survival_prob)
        hazard_rate = d / at_risk
        hazard_rates.append(hazard_rate)
        cumulative_hazard += hazard_rate
        cumulative_hazards.append(cumulative_hazard)
        n -= d

    km_df = pd.DataFrame({
        'Time': event_counts.index,
        'Survival Probability': survival_probs,
        'Hazard Rate': hazard_rates,
        'Cumulative Hazard': cumulative_hazards
    })
    
    if specific_day is not None:
        if km_df.empty:
            return 1.0, 0.0, 0.0  # Return default values when no data points meet the criteria
        closest_day_index = (km_df['Time'] - specific_day).abs().idxmin()
        closest_day = km_df.loc[closest_day_index]
        return closest_day['Survival Probability'], closest_day['Hazard Rate'], closest_day['Cumulative Hazard']

    return km_df

def survival_data(data, ticker):
    # Prepare the data
    df = data[data['Symbol'] == ticker].copy()  # Create a copy to avoid SettingWithCopyWarning
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df = df.set_index('Datetime')
    df = df.sort_index()
    df['log_return'] = np.log(df['AdjClose'] / df['AdjClose'].shift(1))
    return df.dropna()

def last_incident(historical_data, threshold=-0.05):
    below_threshold = historical_data[historical_data['log_return'] < threshold]
    timestamps_sorted = below_threshold.index.sort_values()
    
    today = datetime.today().date()
    if timestamps_sorted.empty:
        return None  # Return None if there are no incidents
    last_available_date = timestamps_sorted.max().date()
    running_days = (today - last_available_date).days

    return running_days

if __name__ == "__main__":
    try:
        print(f"Using thresholds: {thresholds}", file=sys.stderr)

        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Fetch data from DolphinDB
        ddb_data = query_dolphindb()

        all_results = {}

        for ticker in survival_tickers:
            print(f"Processing ticker: {ticker}", file=sys.stderr)

            try:
                # Prepare survival data
                historical_data = survival_data(ddb_data, ticker)

                ticker_results = {}

                for threshold in thresholds:
                    # Calculate interarrival times
                    interarrival_times = hist_interarrival(historical_data, threshold)

                    # Calculate last incident
                    days_since_last_incident = last_incident(historical_data, threshold)

                    # Calculate Kaplan-Meier estimator
                    km_df = kaplan_meier_estimator_with_cumulative_hazard(interarrival_times)

                    # Get the current survival probability, hazard rate, and cumulative hazard
                    if not km_df.empty:
                        current_survival_prob, current_hazard_rate, current_cumulative_hazard = kaplan_meier_estimator_with_cumulative_hazard(interarrival_times, days_since_last_incident)
                    else:
                        current_survival_prob, current_hazard_rate, current_cumulative_hazard = 1.0, 0.0, 0.0

                    # Calculate survival probability, hazard rate, and cumulative hazard for specific days
                    days_to_check = [30, 60, 90]
                    specific_day_results = {}
                    for day in days_to_check:
                        survival_prob, hazard_rate, cumulative_hazard = kaplan_meier_estimator_with_cumulative_hazard(interarrival_times, day)
                        specific_day_results[day] = {
                            "survival_probability": survival_prob,
                            "hazard_rate": hazard_rate,
                            "cumulative_hazard": cumulative_hazard
                        }

                    # Prepare the results dictionary for this threshold
                    threshold_results = {
                        "days_since_last_incident": days_since_last_incident,
                        "current_survival_probability": current_survival_prob,
                        "current_hazard_rate": current_hazard_rate,
                        "current_cumulative_hazard": current_cumulative_hazard,
                        "kaplan_meier_estimator": km_df.to_dict(orient="records"),
                        "specific_day_results": specific_day_results
                    }

                    ticker_results[str(threshold)] = threshold_results

                all_results[ticker] = ticker_results

            except Exception as e:
                print(f"Error processing ticker {ticker}: {str(e)}", file=sys.stderr)
                all_results[ticker] = {"error": str(e)}

        # Create the filename with the timestamp
        filename = f"survival_analysis_all_tickers_multi_threshold.json"
        
        # Construct the full file path
        file_path = os.path.join(current_dir, filename)

        # Save all results to a single JSON file in the current directory
        with open(file_path, "w") as json_file:
            json.dump(all_results, json_file, indent=4)

        print(f"Results saved to: {file_path}", file=sys.stderr)

        # Print the results as JSON
        print(json.dumps(all_results))

    except Exception as e:
        print(f"Error in survival.py: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)