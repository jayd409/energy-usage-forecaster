import numpy as np
import pandas as pd

def generate_energy_data(years=2, seed=42):
    """
    Generate residential energy usage data based on EIA (US Energy Information Administration) benchmarks.
    US average household: 877 kWh/month
    Summer peaks (Jul-Aug): ~1,100 kWh, Winter (Dec-Jan): ~950 kWh, Spring/Fall: ~700-800 kWh
    Daily pattern: peak at 7-9am and 6-9pm. Weekend usage ~8% higher than weekdays.
    """
    rng = np.random.default_rng(seed)

    hours = 24 * 365 * years
    dates = pd.date_range('2022-01-01', periods=hours, freq='H')

    # Monthly averages (kWh/day) based on EIA data
    monthly_daily_avg = {
        1: 29.0,   # January - winter peak
        2: 27.0,   # February
        3: 22.0,   # March - spring transition
        4: 19.0,   # April - spring
        5: 20.0,   # May - late spring
        6: 25.0,   # June - summer begins
        7: 35.0,   # July - summer peak
        8: 34.0,   # August - summer peak
        9: 26.0,   # September - fall transition
        10: 21.0,  # October - fall
        11: 20.0,  # November - late fall
        12: 30.0   # December - winter peak
    }

    consumption = []
    for dt in dates:
        hour = dt.hour
        month = dt.month
        is_weekend = dt.dayofweek >= 5
        day_of_year = dt.dayofyear

        # Base daily usage in kWh (distributed across 24 hours)
        base_daily_kwh = monthly_daily_avg[month]
        base_hourly = base_daily_kwh / 24.0

        # Daily cycle: peaks at 7-9am and 6-9pm (morning and evening)
        daily_factor = 1.0
        if 7 <= hour <= 9:
            daily_factor = 1.5  # Morning peak
        elif 18 <= hour <= 21:
            daily_factor = 1.4  # Evening peak
        elif 0 <= hour <= 5:
            daily_factor = 0.7  # Night low
        elif 10 <= hour <= 17:
            daily_factor = 0.9  # Daytime (most people away)

        # Weekend usage ~8% higher than weekdays
        weekend_factor = 1.08 if is_weekend else 1.0

        # Add random variation (±15% with normal distribution)
        noise = rng.normal(1.0, 0.10)
        noise = np.clip(noise, 0.7, 1.3)

        hourly_consumption = base_hourly * daily_factor * weekend_factor * noise

        consumption.append(hourly_consumption)

    df = pd.DataFrame({
        'datetime': dates,
        'consumption_mw': np.clip(consumption, 0.5, None).round(2),  # Min 0.5 kWh/hour
        'hour': dates.hour,
        'day_of_week': dates.dayofweek,
        'month': dates.month,
        'is_weekend': dates.dayofweek >= 5
    })

    return df
