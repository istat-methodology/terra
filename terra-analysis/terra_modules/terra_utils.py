import requests
import time
import pandas as pd
import matplotlib.pyplot as plt 
from datetime import datetime, timedelta

## Function that generates a list of dates in a given range
def generate_year_month_list(start_date, end_date, frequency):
    # Convert start and end dates from strings to datetime objects
    start = datetime.strptime(start_date, "%Y-%m")
    end = datetime.strptime(end_date, "%Y-%m")

    # Initialize a variable to hold the dates
    date_list = []

    # Function to determine the quarter based on the month
    def get_quarter(month):
        if month <= 3:
            return '01'
        elif month <= 6:
            return '02'
        elif month <= 9:
            return '03'
        else:
            return '04'

    # Loop through each month between start and end dates
    current = start
    while current <= end:

        if(frequency == "quarter"):
            year_trimester = f"{current.year}{get_quarter(current.month)}"
            if year_trimester not in date_list:  # Avoid duplicates
                date_list.append(year_trimester)
        else:
            # Add the formatted year-month string to the list
            date_list.append(current.strftime("%Y%m"))
        
        # Increment the month
        # This ensures that the loop moves to the next month in the next iteration
        current += timedelta(days=32)
        current = current.replace(day=1)  # Reset day to the first of the month

    print(f"Time points: {date_list}")
    return date_list


## Function that converts the metrics JSON in a dataframe
def convert_to_dataframe(json_data, period):
    # Convert each key in the JSON data to a DataFrame
    df_degree_centrality = pd.DataFrame(list(json_data["degree_centrality"].items()), columns=['country', 'degree_centrality'])
    df_vulnerability = pd.DataFrame(list(json_data["vulnerability"].items()), columns=['country', 'vulnerability'])
    df_exportation_strength = pd.DataFrame(list(json_data["exportation strenght"].items()), columns=['country', 'exportation_strength'])
    df_hubness = pd.DataFrame(list(json_data["hubness"].items()), columns=['country', 'hubness'])

    # Display the DataFrames
    # print("Degree Centrality:\n", df_degree_centrality.head())
    # print("\nVulnerability:\n", df_vulnerability.head())
    # print("\nExportation Strength:\n", df_exportation_strength.head())
    # print("\nHubness:\n", df_hubness.head())

    # Merging the dataframes on 'Country'
    metrics = pd.merge(df_degree_centrality, df_vulnerability, on='country', how='outer')
    metrics = pd.merge(metrics, df_exportation_strength, on='country', how='outer')
    metrics = pd.merge(metrics, df_hubness, on='country', how='outer')
    
    metrics['period'] = period  # Add the period to the DataFrame
    
    return metrics


## Get metrics for a given enpoint in a specified time range
def get_graph_metrics(dataset, base_payload, start_date, end_date, frequency):

    print(f"Retrieving {dataset} data")

    # Build endpoint url
    base_url = "https://api.terra.istat.it/graph/graph"

    endpoint = base_url + dataset

    if frequency == "month":
        endpoint += "Month"
    else:
         endpoint += "Trim"

    print(f"Endpoint: {endpoint}")

    # Initialize an empty DataFrame to store the responses
    df_responses = pd.DataFrame()

    # List of periods for which you want to perform requests
    periods = generate_year_month_list(start_date, end_date, frequency)

    print(f"Starting data retrieval...")
    
    # Loop through each period and make a POST request
    for period in periods:
        payload = base_payload.copy()
        payload["tg_period"] = period

        print(f"   Retrieving data for {frequency} {period}")

        response = requests.post(endpoint, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Access the specific key in the response
            # Replace 'data' with the actual key you need to access
            data = response.json().get('metriche', {})  # using .get() to avoid KeyError if 'data' does not exist

            if len(data) == 0:
                print("Empty payload in period: ", period )
            else:
                # Add the data to the DataFrame
                df_response = convert_to_dataframe(data, period)
                df_responses = df_responses._append(df_response, ignore_index=True)

            # Add a delay of one second before the next request
            time.sleep(0.5)
        else:
            print(f"Failed with status code: {response.status_code}")
    
    print(f"... done!")
    
    return df_responses

## Get metrics for a given enpoint in a specified time range
def get_time_series(params):

    endpoint = "https://api.terra.istat.it/time-series/itsa"

    df_time_series = {}

    # Make a GET request
    response = requests.get(endpoint, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response here
        data = response.json().get('diagMain', {}) # using .get() to avoid KeyError if 'data' does not exist
        
        if len(data) == 0:
            print("Empty payload!")
        else:
            df_time_series = pd.DataFrame(data)
            # Convert the 'date' column to datetime format for easier manipulation
            df_time_series['date'] = pd.to_datetime(df_time_series['date'])
    else:
        print(f"Failed with status code: {response.status_code}")

    return df_time_series


