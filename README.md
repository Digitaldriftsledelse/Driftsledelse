# Driftsledelse

An educational and analytical project covering operations management, data analysis, and visualization — primarily focused on Norwegian infrastructure and data science domains.

## Overview

This repository contains Jupyter notebooks, datasets, and visualizations used for learning and applying operations management concepts. Content is organized by topic area and covers a range of analytical methods from portfolio optimization to geospatial flood zone mapping.

All notebooks are written in Norwegian and designed to run on Google Colab.

## Repository Structure

```
Driftsledelse/
├── IND210/           # Portfolio management problems and data analysis notebooks
├── IND310/           # Advanced analysis notebooks
├── Kapitel_1/        # Volcano data and eruption analysis
├── Kapitel_3/        # Spider diagrams and material properties data
├── Temp/             # Geospatial flood zone data (GeoJSON)
├── Visualisering/    # Visualization notebooks and aquaculture statistics
├── vannkraft/        # Hydropower-related files
└── *.ipynb           # Standalone notebooks (interactive diagrams, spider diagrams, etc.)
```

## Topics Covered

- **Operations Management**: Portfolio problems, selection problems, ranking, and sorting
- **Data Visualization**: Bar charts, line charts, area charts, scatter plots, histograms, and interactive maps
- **Geospatial Analysis**: Flood zone mapping using GeoJSON data from Norwegian authorities
- **Infrastructure Analysis**: Cost estimation for infrastructure projects
- **Domain Data**:
  - Aquaculture statistics (salmon and rainbow trout by county)
  - Volcano eruption data
  - Water level monitoring (Oslo)
  - Hydropower infrastructure

## Technology Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Core language |
| Jupyter Notebooks | Interactive analysis and documentation |
| Pandas | Data manipulation |
| Altair / Vega | Interactive visualizations |
| GeoJSON | Geospatial data format |

## Data Sources

- **Kartverket** (Norwegian Mapping Authority): County and municipality relations
- **Norwegian government**: Aquaculture statistics and flood zone data
- **Kartverket Havniva**: Water level data for Oslo

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd Driftsledelse
   ```

2. Open any notebook in [Google Colab](https://colab.research.google.com/) or a local Jupyter environment.

3. Install dependencies if running locally:
   ```bash
   pip install pandas altair jupyter
   ```

## Language

All notebooks and documentation are written in Norwegian (Bokmål/Dano-Norwegian).
