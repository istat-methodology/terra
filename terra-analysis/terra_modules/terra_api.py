import requests
import time
import pandas as pd
from datetime import datetime, timedelta


def generate_time_interval(start_date: str, end_date: str, frequency: str) -> list[str]:
    """
    Generate a list of time periods between start_date and end_date.

    Parameters
    ----------
    start_date : str
        Format YYYY-MM
    end_date : str
        Format YYYY-MM
    frequency : str
        'month' or 'quarter'

    Returns
    -------
    list[str]
        List of periods (YYYYMM or YYYYQ)
    """
    start = datetime.strptime(start_date, "%Y-%m")
    end = datetime.strptime(end_date, "%Y-%m")

    periods = []

    def quarter_from_month(month: int) -> int:
        return (month - 1) // 3 + 1

    current = start
    while current <= end:
        if frequency == "quarter":
            period = f"{current.year}{quarter_from_month(current.month):02d}"
            if period not in periods:
                periods.append(period)
        else:
            periods.append(current.strftime("%Y%m"))

        current += timedelta(days=32)
        current = current.replace(day=1)

    return periods


def metrics_to_dataframe(json_data: dict, period: str) -> pd.DataFrame:
    """
    Convert TERRA metrics JSON into a pandas DataFrame.

    Parameters
    ----------
    json_data : dict
        Mapping country -> metrics
    period : str
        Time period identifier

    Returns
    -------
    pd.DataFrame
        One row per country with metrics and period column
    """
    metrics = pd.DataFrame(json_data).reset_index(names="country")
    metrics["period"] = period  # Add the period to the DataFrame
    return metrics


def fetch_graph_time_range(verbose: bool = True) -> tuple[str, str]:
    """
    Fetch the available time range for graph data from the TERRA metadata endpoint.

    Returns
    -------
    tuple[str, str]
        (start_date, end_date) in YYYY-MM format
    """
    endpoint = "https://api.terra.istat.it/cls/metadata"

    if verbose:
        print(f"Endpoint: {endpoint}")

    response = requests.get(endpoint, timeout=30)

    if not response.ok:
        raise RuntimeError(f"Failed to fetch metadata: {response.status_code}")

    metadata = response.json()

    try:
        graph_meta = metadata["graph"]

        start_year = graph_meta["timeStart"]["year"]
        start_month = graph_meta["timeStart"]["month"]

        end_year = graph_meta["timeEnd"]["year"]
        end_month = graph_meta["timeEnd"]["month"]

    except KeyError as exc:
        raise RuntimeError(
            "Unexpected metadata format: missing graph time range"
        ) from exc

    start_date = f"{start_year:04d}-{start_month:02d}"
    end_date = f"{end_year:04d}-{end_month:02d}"

    if verbose:
        print(f"Graph time range: {start_date} → {end_date}")

    return start_date, end_date


def fetch_all_countries(verbose: bool = True) -> list[str]:
    endpoint = "https://api.terra.istat.it/cls/countries?lang=en"

    if verbose:
        print(f"Endpoint: {endpoint}")

    response = requests.get(endpoint, timeout=30)

    if not response.ok:
        raise RuntimeError(f"Failed to fetch countries: {response.status_code}")

    countries = [item["country"] for item in response.json() if "country" in item]

    if verbose:
        print(f"Countries: {countries}")

    return countries


## Get metrics for a given enpoint in a specified time range
def fetch_graph_metrics(
    dataset: str,
    base_payload: dict,
    start_date: str,
    end_date: str,
    frequency: str,
    sleep_seconds: float = 0.5,
    verbose: bool = True,
) -> pd.DataFrame:
    """
    Retrieve graph metrics from the TERRA API over a time range.

    Returns
    -------
    pd.DataFrame
        Columns: country, period, <metrics>
    """
    if frequency not in {"month", "quarter"}:
        raise ValueError("frequency must be 'month' or 'quarter'")

    base_url = "https://api.terra.istat.it/graph/graph"
    endpoint = f"{base_url}{dataset}{'Month' if frequency == 'month' else 'Trim'}"

    if verbose:
        print(f"Endpoint: {endpoint}")

    periods = generate_time_interval(start_date, end_date, frequency)
    metrics_list = []

    for period in periods:
        payload = base_payload.copy()
        payload["period"] = period

        if verbose:
            print(f"Retrieving data for {period}")

        response = requests.post(endpoint, json=payload, timeout=30)

        if response.ok:
            data = response.json().get("metriche", {})
            if data:
                df = metrics_to_dataframe(data, period)
                metrics_list.append(df)
        else:
            if verbose:
                print(f"Request failed for {period}: {response.status_code}")

        if sleep_seconds:
            time.sleep(sleep_seconds)

    if not metrics_list:
        raise RuntimeError("No data retrieved from TERRA API")

    return pd.concat(metrics_list, ignore_index=True)


def fetch_time_series(base_payload: dict, countries: list[str]) -> pd.DataFrame:
    endpoint = "https://api.terra.istat.it/time-series/ts"
    time_series_list = []

    for country in countries:
        payload = base_payload.copy()
        payload["country"] = country

        response = requests.post(endpoint, json=payload, timeout=30)

        if response.ok:
            data = response.json().get("diagMain", {})
            if data:
                df = pd.DataFrame(data)
                df["country"] = country
                time_series_list.append(df)

    if not time_series_list:
        raise RuntimeError("No time series retrieved")

    df = pd.concat(time_series_list, ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])

    return df
