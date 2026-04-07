import numpy as np
import pandas as pd

def ewma_forecast(series, span=24, steps=168):
    """Forecast next steps hours using EWMA and seasonal component."""
    ewma = series.ewm(span=span, adjust=False).mean()
    last = float(ewma.iloc[-1])

    seasonal = series.tail(168).values
    seasonal_mean = seasonal.mean()

    forecast = []
    for i in range(steps):
        seasonal_adj = seasonal[i % 168] - seasonal_mean
        value = max(0, last + seasonal_adj + np.random.normal(0, 50))
        forecast.append(round(value, 1))

    return forecast

def peak_stats(df):
    return {
        'peak_hour': int(df.groupby('hour')['consumption_mw'].mean().idxmax()),
        'peak_month': int(df.groupby('month')['consumption_mw'].mean().idxmax()),
        'weekend_avg': round(df[df['is_weekend']]['consumption_mw'].mean(), 1),
        'weekday_avg': round(df[~df['is_weekend']]['consumption_mw'].mean(), 1),
    }
