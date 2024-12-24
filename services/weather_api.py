import requests
import matplotlib.pyplot as plt
from io import BytesIO
from config import TOKEN_WEATHER

BASE_URL = "http://dataservice.accuweather.com"


def get_city_location(city_name: str):
    """Получает ключ местоположения для города."""
    url = f"{BASE_URL}/locations/v1/cities/search"
    params = {"apikey": TOKEN_WEATHER, "q": city_name}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data[0]["Key"] if data else None
    except requests.RequestException as e:
        print(f"Ошибка: {e}")
        return None


def get_weather(city_name: str, interval: int):
    """Получает прогноз погоды для указанного города."""
    location_key = get_city_location(city_name)
    if not location_key:
        return f"Город {city_name} не найден.", None

    url = f"{BASE_URL}/forecasts/v1/daily/{interval}day/{location_key}"
    params = {"apikey": TOKEN_WEATHER, "language": "ru", "metric": True}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        dates = []
        min_temps = []
        max_temps = []
        precipitations = []
        wind_speeds = []
        wind_directions = []

        forecast_text = ""
        for forecast in data["DailyForecasts"]:
            print(forecast)
            date = forecast["Date"][:10]
            min_temp = forecast["Temperature"]["Minimum"]["Value"]
            max_temp = forecast["Temperature"]["Maximum"]["Value"]
            precip = forecast["Day"]["PrecipitationType"]
            wind_speed = forecast["Day"]["Wind"]["Speed"]["Value"]
            wind_direction = forecast["Day"]["Wind"]["Direction"]["Localized"]

            dates.append(date)
            min_temps.append(min_temp)
            max_temps.append(max_temp)
            precipitations.append(precip)
            wind_speeds.append(wind_speed)
            wind_directions.append(wind_direction)

            forecast_text += (
                f"Дата: {date}\n"
                f"Температура: {min_temp}°C - {max_temp}°C\n"
                f"Осадки: {precip}\n"
                f"Ветер: {wind_speed} м/с, направление: {wind_direction}\n\n"
            )

        plot = generate_weather_plot(
            dates, min_temps, max_temps, precipitations, wind_speeds)
        return forecast_text, plot
    except requests.RequestException as e:
        print(f"Ошибка: {e}")
        return "Ошибка получения прогноза погоды.", None


def generate_weather_plot(dates, min_temps, max_temps, precipitations, wind_speeds):
    """Создает график погоды."""
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # График температуры
    ax1.set_xlabel("Дата")
    ax1.set_ylabel("Температура (°C)", color="tab:red")
    ax1.plot(dates, min_temps, label="Мин. температура",
             color="tab:red", linestyle="--")
    ax1.plot(dates, max_temps, label="Макс. температура", color="tab:orange")
    ax1.tick_params(axis="y", labelcolor="tab:red")

    # График осадков
    ax2 = ax1.twinx()
    ax2.set_ylabel("Осадки (%)", color="tab:blue")
    ax2.bar(dates, precipitations, alpha=0.3, color="tab:blue", label="Осадки")
    ax2.tick_params(axis="y", labelcolor="tab:blue")

    # График ветра
    ax2.plot(dates, wind_speeds, label="Скорость ветра (м/с)",
             color="tab:green", linestyle="--")

    fig.tight_layout()
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9))
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf
