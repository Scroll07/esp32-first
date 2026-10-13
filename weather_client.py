import time
import urequests

URL = "https://api.open-meteo.com/v1/forecast?latitude=56.11&longitude=47.47&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset&current=temperature_2m,weather_code&timezone=Europe%2FMoscow&past_days=1&forecast_days=2"

WMO_MAP = {
    0: "Ясно",
    1: "В осн. ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    48: "Иней/туман",
    51: "Слабая морось",
    61: "Небольшой дождь",
    63: "Умеренный дождь",
    65: "Сильный дождь",
    71: "Небольшой снег",
    73: "Снегопад",
    75: "Сильный снегопад",
    80: "Ливень",
    95: "Гроза",
}

def parse_weather():
    response = None
    try:
        print("Запрос погоды...")
        response = urequests.get(URL)
        if response.status_code == 200:
            data = response.json()
            
            # Текущие показания прямо сейчас
            cur_temp = data.get("current", {}).get("temperature_2m")
            cur_code = data.get("current", {}).get("weather_code", 0)
            print(f"Сейчас за окном: {cur_temp}°C, {WMO_MAP.get(cur_code, 'Код ' + str(cur_code))}\n")
            
            daily = data.get("daily", {})
            dates = daily.get("time", [])
            codes = daily.get("weather_code", [])
            max_t = daily.get("temperature_2m_max", [])
            min_t = daily.get("temperature_2m_min", [])
            sunrises = daily.get("sunrise", [])
            sunsets = daily.get("sunset", [])

            labels = ["Вчера", "Сегодня", "Завтра"]

            for i in range(min(3, len(dates))):
                label = labels[i]
                date_str = dates[i]
                cond = WMO_MAP.get(codes[i], f"Код {codes[i]}")
                t_max = max_t[i]
                t_min = min_t[i]
                
                # Время восхода и заката обрезаем до HH:MM
                sr = sunrises[i].split("T")[1] if "T" in sunrises[i] else sunrises[i]
                ss = sunsets[i].split("T")[1] if "T" in sunsets[i] else sunsets[i]

                print(f"[{label}] {date_str}:")
                print(f"  Погода: {cond}")
                print(f"  Температура: от {t_min}°C до {t_max}°C")
                print(f"  Солнце: восход {sr}, закат {ss}")
                print("-" * 30)
        else:
            print(f"Ошибка API: {response.status_code}")
    except Exception as e:
        print(f"Ошибка выполнения: {e}")
    finally:
        if response:
            response.close()

if __name__ == "__main__":
    parse_weather()