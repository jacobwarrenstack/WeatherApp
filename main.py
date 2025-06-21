import requests

# ANSI color codes for terminal text
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

# Function to get weather at specified latitude-longitude
def get_weather(latitude, longitude):
    req_url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude={lat}&longitude={lon}"
        "&current_weather=true&hourly=temperature_2m"
        "&daily=temperature_2m_max,temperature_2m_min,weathercode"
        "&timezone=auto"
    ).format(lat=latitude, lon=longitude)

    r = requests.get(req_url)
    r.raise_for_status()
    return r.json()

# Function to add color and emojis to temperatures
def style_temperature(temp):
    if temp >= 30:
        return f"{RED}🔥{temp}°C{RESET}"  # has a weird space so the others are offset. TO BE FIXED.
    elif temp >= 20:
        return f"{YELLOW}☀️ {temp}°C{RESET}"
    elif temp >= 10:
        return f"{GREEN}🌤️ {temp}°C{RESET}"
    else:
        return f"{BLUE}❄️ {temp}°C{RESET}"

# Function to add color and emojis to wind speeds
def style_windspeed(speed):
    if speed >= 15:
        return f"{RED}💨 {speed} m/s{RESET}"
    elif speed >= 5:
        return f"{YELLOW}🌬️ {speed} m/s{RESET}"
    else:
        return f"{GREEN}🍃 {speed} m/s{RESET}"

if __name__ == "__main__":
    input_lat = input("🌍 Latitude: ").strip()
    input_lon = input("🌍 Longitude: ").strip()

    try:
        data = get_weather(input_lat, input_lon)
        current = data["current_weather"]
        today = data["daily"]

        # Current weather
        temp = current["temperature"]
        wind_speed = current["windspeed"]
        mph_factor = 2.2

        print(f"Now: {style_temperature(temp)}, wind {style_windspeed(wind_speed)} ({round(wind_speed * mph_factor, 1)} mph)")

        # Today's weather
        high = today["temperature_2m_max"][0]
        low = today["temperature_2m_min"][0]

        print(f"Today's High: {style_temperature(high)}")
        print(f"Today's Low: {style_temperature(low)}")

    except requests.exceptions.RequestException as e:
        print(f"{RED}Error fetching weather data: {e}{RESET}")
