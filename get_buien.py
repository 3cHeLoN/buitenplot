"""Script to show a png on teams."""

import numpy as np
import requests
import matplotlib

matplotlib.use("Agg")  # Non-GUI backend
import matplotlib.pyplot as plt
from datetime import datetime, time


def to_intensity(value: int) -> float:
    return float(10 ** ((value - 109) / 32))


def get_image(lat: float, lon: float) -> None:
    """Create a plot image of the rain forecast.

    Args:
        lat (float): The latitude.
        lon (float): The longitude.
    """
    url = f"https://gpsgadget.buienradar.nl/data/raintext/?lat={lat}&lon={lon}"

    # Fetch Buienradar rain forecast data
    response = requests.get(url)
    data = response.text.strip().split("\n")

    # Parse the data into minutes and intensities
    times = []
    intensities = []

    for entry in data:
        if "|" in entry:
            value, timestamp = entry.split("|")

            times.append(timestamp)
            intensities.append(to_intensity(int(value)))

    start_hiking_time = time(12, 15)
    end_hiking_time = time(13, 15)
    colors = [
        "orange"
        if start_hiking_time <= datetime.strptime(t, "%H:%M").time() <= end_hiking_time
        else "lightgrey"
        for t in times
    ]

    # Plot
    plt.figure(figsize=(10, 5))
    plt.bar(times, intensities, color=colors)
    plt.title("Buienradar Rain Forecast (Rotterdam)")
    plt.xlabel("Time")
    plt.ylabel("Rain (mm/h)")
    plt.xticks(rotation=45)
    plt.yticks(np.arange(0, 12, 2))
    plt.ylim(0, 12)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig("buienradar_plot.png")
    print("Plot saved as buienradar_plot.png")


def main():
    get_image(lat=51.924419, lon=4.477733)


if __name__ == "__main__":
    main()
