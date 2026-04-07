#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from data import generate_energy_data
from forecast import peak_stats, ewma_forecast
from charts import build_dashboard

df = generate_energy_data(years=2)
stats = peak_stats(df)
forecast = ewma_forecast(df['consumption_mw'], steps=168)

print(f"Data points: {len(df):,}")
print(f"Peak hour: {stats['peak_hour']}:00")
print(f"Peak month: {stats['peak_month']}")
print(f"Weekend avg: {stats['weekend_avg']} MW")
print(f"Weekday avg: {stats['weekday_avg']} MW")

build_dashboard(df, stats, forecast)
print("Dashboard complete!")
