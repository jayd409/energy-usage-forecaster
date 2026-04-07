import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from utils import save_html
from analysis import daily_average, hourly_profile, monthly_average, detect_anomalies

def chart_daily_with_ma(df):
    fig, ax = plt.subplots(figsize=(12, 5))
    daily = daily_average(df)
    ax.plot(range(len(daily)), daily.values, alpha=0.4, label='Daily', color='steelblue')
    rolling_7 = daily.rolling(7).mean()
    ax.plot(range(len(rolling_7)), rolling_7.values, label='7-Day Moving Avg', color='red', linewidth=2)
    ax.set_xlabel('Days')
    ax.set_ylabel('Consumption (MW)')
    ax.set_title('Daily Energy Consumption with 7-Day Moving Average')
    ax.legend()
    ax.grid(True, alpha=0.3)
    return fig

def chart_hourly_profile(df):
    fig, ax = plt.subplots(figsize=(11, 5))
    hourly = hourly_profile(df)
    ax.bar(hourly.index, hourly.values, color='teal', alpha=0.7)
    ax.set_xlabel('Hour of Day')
    ax.set_ylabel('Avg Consumption (MW)')
    ax.set_title('Hourly Average Consumption Profile')
    ax.set_xticks(range(0, 24, 2))
    return fig

def chart_monthly_bars(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly = monthly_average(df)
    ax.bar(monthly.index, monthly.values, color='orange', alpha=0.7)
    ax.set_xlabel('Month')
    ax.set_ylabel('Avg Consumption (MW)')
    ax.set_title('Monthly Average Consumption (Seasonal Pattern)')
    ax.set_xticks(range(1, 13))
    return fig

def chart_weekend_vs_weekday(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    weekend_data = df[df['is_weekend']]['consumption_mw'].values
    weekday_data = df[~df['is_weekend']]['consumption_mw'].values
    ax.bar(['Weekend', 'Weekday'], [weekend_data.mean(), weekday_data.mean()],
          color=['lightcoral', 'lightgreen'], alpha=0.7)
    ax.set_ylabel('Avg Consumption (MW)')
    ax.set_title('Weekend vs Weekday Consumption')
    return fig

def chart_forecast(df):
    from forecast import ewma_forecast
    fig, ax = plt.subplots(figsize=(12, 5))

    last_2_weeks = df.tail(14*24)
    forecast_7_days = ewma_forecast(df['consumption_mw'], steps=7*24)

    ax.plot(range(len(last_2_weeks)), last_2_weeks['consumption_mw'].values,
           label='Last 2 Weeks (Actual)', color='blue', linewidth=2)
    ax.plot(range(len(last_2_weeks), len(last_2_weeks) + len(forecast_7_days)),
           forecast_7_days, label='Next 7 Days (Forecast)', color='red', linewidth=2, linestyle='--')

    ax.set_xlabel('Hours')
    ax.set_ylabel('Consumption (MW)')
    ax.set_title('Energy Consumption: Actual vs Forecast')
    ax.legend()
    ax.grid(True, alpha=0.3)
    return fig

def chart_anomalies(df):
    fig, ax = plt.subplots(figsize=(12, 5))
    daily = daily_average(df)
    mean_val = daily.mean()
    std_val = daily.std()
    threshold = mean_val + 2.5 * std_val

    anomalies = daily[daily > threshold]
    normal = daily[daily <= threshold]

    ax.scatter(range(len(normal)), normal.values, alpha=0.6, label='Normal', color='blue', s=20)
    ax.scatter(anomalies.index, anomalies.values, alpha=0.8, label='Anomaly', color='red', s=50)
    ax.axhline(threshold, color='red', linestyle='--', alpha=0.5, label='Threshold')
    ax.set_xlabel('Days')
    ax.set_ylabel('Consumption (MW)')
    ax.set_title('Anomaly Detection (Flagged High Consumption Days)')
    ax.legend()
    return fig

def build_dashboard(df, stats, forecast):
    charts = [
        ('Daily Consumption with Moving Average', chart_daily_with_ma(df)),
        ('Hourly Profile', chart_hourly_profile(df)),
        ('Monthly Average', chart_monthly_bars(df)),
        ('Weekend vs Weekday', chart_weekend_vs_weekday(df)),
        ('Forecast', chart_forecast(df)),
        ('Anomaly Detection', chart_anomalies(df)),
    ]

    kpis = [
        ('Peak Hour', f"{stats['peak_hour']}:00"),
        ('Peak Month', stats['peak_month']),
        ('Weekend Avg', f"{stats['weekend_avg']} MW"),
        ('Weekday Avg', f"{stats['weekday_avg']} MW"),
    ]

    save_html(charts, 'Energy Usage Forecaster Dashboard', kpis,
             'outputs/energy_dashboard.html')
