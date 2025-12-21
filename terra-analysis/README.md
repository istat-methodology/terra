# TERRA – Advanced Analyses via API

This repository contains examples of advanced analytical workflows based on data
retrieved directly from the **TERRA APIs**.

While the TERRA web dashboard provides interactive and exploratory visualisations,
some analyses are not directly available through the interface.
The notebooks included here demonstrate how these analyses can be performed
programmatically using the official APIs, with a focus on reproducibility and transparency.

---

## Repository structure

```text
│
├── terra_modules/
│   └── terra_api.py
|
├── terra_graph_advanced_analysis.ipynb
├── terra_time_series_advanced_analysis.ipynb
│
└── README.md
```

## Notebooks

### 1. `terra_graph_advanced_analysis.ipynb`

This notebook shows how to perform advanced analyses on **trade network graphs**
retrieved via the TERRA Graph API.

In particular, it illustrates:

- how to query graph metrics programmatically using the API;
- how to work with extended time ranges not directly exposed in the dashboard;
- examples of exploratory analyses such as:
  - evolution of network indicators over time;
  - country-level comparisons;
  - focus on single-country dynamics (e.g. rotating leadership patterns).

The notebook is fully parameterised and can be easily adapted to different
datasets, frequencies, indicators, and subsets of countries.

### 2. `terra_time_series_advanced_analysis.ipynb`

This notebook focuses on time series data retrieved via the TERRA Time Series API.

It demonstrates:

- how to download and combine country-level time series programmatically,
- how to manage time ranges and ensure consistency across countries,

Examples of comparative visualisation and country-level analysis.

As for the graph notebook, the emphasis is on analyses that go beyond what is
directly available through the dashboard interface.

## TERRA API client (`terra_api.py`)

The file `terra_modules/terra_api.py` provides a lightweight Python client for
interacting with the TERRA APIs.

It includes functions to:

- retrieve metadata and available time ranges;
- fetch graph metrics over time;
- fetch time series data for selected countries;
- generate consistent time intervals for analysis.

The module is intentionally simple and self-contained, and is designed to be
used directly within notebooks or other analytical scripts.

## Usage

1. Clone the repository.
2. Open the notebooks in a Jupyter environment.
3. Adjust the analysis parameters (datasets, time range, indicators, countries)
   directly within the notebooks.
4. Run the notebooks to reproduce the analyses.

All data are retrieved on-the-fly from the TERRA APIs; no local data files are required.

## Notes

- The notebooks are intended as **examples** of what can be achieved via the APIs,
  not as exhaustive analytical pipelines.
- The code is deliberately kept explicit and readable to facilitate reuse and
  adaptation.
- Users are encouraged to modify and extend the analyses to suit their specific
  research questions.
- Feedback and contributions are welcome to improve the examples and the API client.
