import pandas as pd
import numpy as np
from datetime import timedelta, datetime

np.random.seed(42)

# Galactic events
event_types = ["solar_flare", "cosmic_storm", "asteroid_flyby"]
num_events = 20
event_dates = pd.date_range(
    start="2045-01-01", end="2045-12-31", periods=num_events
).normalize()

galactic_events_data = []
for i, event_date in enumerate(event_dates):
    event_type = np.random.choice(event_types)
    intensity = np.random.randint(5, 11)  # Increased event intensity
    galactic_events_data.append([f"E{i+1:03}", event_date, event_type, intensity])

galactic_events_df = pd.DataFrame(
    galactic_events_data, columns=["event_id", "date", "event_type", "intensity"]
)

# Mars weather
dates = pd.date_range(start="2045-01-01", end="2045-12-31", freq="D")
mars_weather_data = []
for date in dates:
    if date in event_dates:
        # Drastic changes in weather on event days
        avg_temp = np.random.choice([-80, 50])  # Extremely low or high temperature
        solar_radiation = np.random.choice(
            [0, 15]
        )  # Extremely low or high solar radiation
    else:
        avg_temp = np.random.uniform(-80, 20)  # Regular temperature range
        solar_radiation = np.random.uniform(5, 10)  # Regular solar radiation range

    mars_weather_data.append([date, avg_temp, solar_radiation])

mars_weather_df = pd.DataFrame(
    mars_weather_data,
    columns=["date", "avg_temperature_celsius", "solar_radiation_kwh_m2"],
)

# Dictionary to map galactic event dates to event IDs
galactic_event_map = {
    event_date: event_id
    for event_id, event_date in zip(
        galactic_events_df["event_id"], galactic_events_df["date"]
    )
}

# Adjust alien consumption data with galactic event IDs (no intensity in the consumption dataset)
resource_types = ["power", "water", "rare_minerals"]
alien_consumption_data = []

for date in dates:
    event_id = galactic_event_map.get(
        date, None
    )  # Get event ID if it exists for the date
    for resource in resource_types:
        # Base consumption values for each resource with some random fluctuation
        if resource == "power":
            quantity = np.random.uniform(100, 200)
        elif resource == "water":
            quantity = np.random.uniform(50, 100)
        else:  # rare_minerals
            quantity = np.random.uniform(30, 70)

        temperature = mars_weather_df.loc[
            mars_weather_df["date"] == date, "avg_temperature_celsius"
        ].values[0]
        solar_radiation = mars_weather_df.loc[
            mars_weather_df["date"] == date, "solar_radiation_kwh_m2"
        ].values[0]

        # Apply stronger effect of extreme temperatures or solar radiation on consumption
        if temperature < -50 or temperature > 10:
            quantity *= 10  # Increase resource consumption for extreme temperatures
        if solar_radiation > 8:
            quantity *= 6  # Increase consumption during high solar radiation
        if event_id:  # If there's a galactic event
            quantity *= 20  # Galactic events cause large spikes in consumption

        alien_consumption_data.append(
            [date, resource, quantity, temperature, solar_radiation, event_id]
        )

alien_consumption_df = pd.DataFrame(
    alien_consumption_data,
    columns=[
        "date",
        "resource",
        "quantity",
        "temperature",
        "solar_radiation",
        "event_id",
    ],
)

alien_consumption_df.to_csv("data/alien_consumption.csv", index=False)
mars_weather_df.to_csv("data/mars_weather.csv", index=False)
galactic_events_df.to_csv("data/galactic_events.csv", index=False)
