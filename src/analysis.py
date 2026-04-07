import pandas as pd
import numpy as np

def daily_average(df):
    return df.groupby(df['datetime'].dt.date)['consumption_mw'].mean()

def monthly_average(df):
    return df.groupby(df['datetime'].dt.month)['consumption_mw'].mean()

def hourly_profile(df):
    return df.groupby('hour')['consumption_mw'].mean()

def weekend_vs_weekday(df):
    weekend = df[df['is_weekend']]['consumption_mw'].mean()
    weekday = df[~df['is_weekend']]['consumption_mw'].mean()
    return {'weekend': round(weekend, 1), 'weekday': round(weekday, 1)}

def detect_anomalies(df, threshold_std=2.5):
    mean_val = df['consumption_mw'].mean()
    std_val = df['consumption_mw'].std()
    threshold = mean_val + (threshold_std * std_val)
    anomalies = df[df['consumption_mw'] > threshold].copy()
    return anomalies
