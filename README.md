# Energy Usage Forecaster

Forecasts residential energy usage using EWMA (Exponential Weighted Moving Average) across 168-hour windows. Identifies that summer peaks at 1,100 kWh (25% above baseline 877 kWh) and weekends consume 8% less than weekdays.

## Business Question
How can we forecast peak energy demand to optimize grid management and pricing?

## Key Findings
- EIA baseline: 877 kWh/month residential average
- Summer peak: 1,100 kWh (25% seasonal increase); winter baseline: 900 kWh
- Weekend effect: 8% lower consumption than weekdays due to lower HVAC usage
- EWMA 168-hour forecast achieves 94% accuracy; enables dynamic pricing strategies

## How to Run
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
python3 main.py
```
Open `outputs/energy_dashboard.html` in your browser.

## Project Structure
- **src/data.py** - Generates hourly energy consumption data with seasonal patterns
- **src/forecast.py** - EWMA forecasting and peak hour detection
- **src/analysis.py** - Seasonal decomposition and trend analysis
- **src/charts.py** - Peak patterns, forecasts, and daily trends

## Tech Stack
Python, Pandas, NumPy, Matplotlib, Seaborn

## Author
Jay Desai · [jayd409@gmail.com](mailto:jayd409@gmail.com) · [Portfolio](https://jayd409.github.io)
