from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = os.environ.get("WEATHER_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if not city:
            error = "Введите название города"
        else:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric",
                "lang": "ru",
            }

            try:
                response = requests.get(url, params=params, timeout=10)
                data = response.json()

                if response.status_code == 200:
                    weather = {
                        "city": data["name"],
                        "country": data["sys"]["country"],
                        "temp": round(data["main"]["temp"]),
                        "feels_like": round(data["main"]["feels_like"]),
                        "description": data["weather"][0]["description"].capitalize(),
                        "humidity": data["main"]["humidity"],
                        "wind": data["wind"]["speed"],
                        "icon": data["weather"][0]["icon"],
                    }
                elif response.status_code == 404:
                    error = f"Город «{city}» не найден"
                else:
                    error = f"Ошибка API: {data.get("message", "неизвестная")}"

            except requests.RequestException:
                error = "Не удалось подключится к сервису погоды"

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)