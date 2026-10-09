<p align="center">
  <img src="docs/LogoTerraFull.png" alt="TERRA — Import Export Network Analysis" width="800">
</p>

<p align="center">
  <strong>Istat Experimental Statistic for international trade analysis</strong>
</p>

<p align="center">
  An open source dashboard combining interactive visualization, social network
  analysis and data-processing pipelines.
</p>

<p align="center">
  <img alt="European Big Data Hackathon 2021 — 1st place" src="https://img.shields.io/badge/European%20Big%20Data%20Hackathon%202021-1st%20place-D4A72C">
  <img alt="Open source dashboard" src="https://img.shields.io/badge/dashboard-open%20source-2DA44E">
  <img alt="COMEXT and Eurostat data" src="https://img.shields.io/badge/data-COMEXT%20%7C%20Eurostat-0969DA">
</p>

<p align="center">
  <a href="https://doi.org/10.1017/S1474745626101591"><strong>Research article</strong></a>
  · <a href="https://vimeo.com/525488078"><strong>Hackathon pitch</strong></a>
  · <a href="docs/Cosmopolitics%20Graph%20Analysis.pdf"><strong>Graph analysis</strong></a>
</p>

## About TERRA

TERRA was implemented by Istat's team in the context of the **European Big
Data Hackathon 2021**, organized by Eurostat, where it was awarded first place.

The dashboard analyzes international trade relations at macro and micro level,
combining social network analysis, trade indicators and mobility-policy
analysis.

## Architecture

| Component | Role |
|---|---|
| **Vue.js** | Modern JavaScript framework for the dashboard interface. |
| **Docker** | Container-based microservice architecture. |
| **Python** | Network analysis and data-processing components. |
| **R** | Mobility-policy analysis integrated in the pipeline. |

The architecture is scalable and allows Python and R components to be
integrated into the same data-processing pipeline.

## Core Functionalities

| Functionality | Description |
|---|---|
| **Interactive map** | Macro-economic indicators, import and export values, main traded goods and trade partners for EU countries. |
| **Graph analysis** | Monthly COMEXT data by means of transport represented as international trade networks and standard graph measures. |
| **Mobility policy analysis** | Descriptive mobility indices together with daily and monthly indicators of government restrictions. |
| **COVID-19 impact evaluation** | Descriptive statistics, interrupted time-series analysis, nowcasting and forecasting for international trade. |
| **Trade and basket analysis** | Monthly import and export trends by product, including year-over-year changes in CPA product shares during 2020. |

## Dashboard Preview

### Interactive map

![TERRA interactive map](docs/Screenshots/Cosmopolitics%20-%20Interactive%20Map.jpg)

### Graph analysis

![TERRA graph analysis](docs/Screenshots/Cosmopolitics%20-%20Graph%20analysis.jpg)

### BEC analysis

![TERRA BEC analysis](docs/Screenshots/Cosmopolitics%20-%20BEC%20analysis.jpg)

### Basket of traded products

![TERRA basket of traded products](docs/Screenshots/Cosmopolitics%20-%20Basket%20of%20traded%20products.jpg)

## Citation

If you use TERRA in your research, please cite:

> Bruno, M., Brogi, F., Cerasti, E., De Fausti, F., Fronzetti Colladon, A.,
> Guardabascio, B., & Massacci, G. (2026). Exploring the Complexity of
> International Trade Networks with TERRA. *World Trade Review*, 1–24.
> doi:[10.1017/S1474745626101591](https://doi.org/10.1017/S1474745626101591)

```bibtex
@article{bruno2026terra,
  title   = {Exploring the Complexity of International Trade Networks with TERRA},
  author  = {Bruno, M. and Brogi, F. and Cerasti, E. and De Fausti, F. and Fronzetti Colladon, A. and Guardabascio, B. and Massacci, G.},
  journal = {World Trade Review},
  year    = {2026},
  pages   = {1--24},
  doi     = {10.1017/S1474745626101591}
}
```
