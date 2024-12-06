import datetime
import requests
import re
import os


def _scrape_dn_headlines():
    url = "https://www.dn.se/direkt/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch the website: {response.status_code}")
        return []

    # extract headlines using regex
    html_content = response.text
    pattern = r"<h2>\s*(.*?)\s*</h2>"
    headlines = re.findall(pattern, html_content)

    return headlines


def _display_headlines(headlines):
    if not headlines:
        print("No headlines found.")
        return

    print("\nDN Headlines:\n" + "=" * 20)
    for idx, headline in enumerate(headlines, start=1):
        print(f"{idx}. {headline}")
    print("\nEnd of Headlines\n" + "=" * 20)


def get_latest_headlines_from_dn():
    headlines = _scrape_dn_headlines()
    _display_headlines(headlines)


def get_current_weather(city="Stockholm"):
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["cod"] == 200:
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"] - 273.15  # convert from kelvin to celsius
        print(f"Weather in {city}: {weather} | Temperature: {temp:.2f}°C")
    else:
        print("City not found.")


def get_current_week_number():
    current_date = datetime.datetime.now()
    week_number = current_date.isocalendar()[1]
    return week_number
