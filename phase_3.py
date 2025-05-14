import requests
import sqlite3
import geocoder

def fetch_data_from_api():
    api_key = 'AIzaSyAJYy0a2k8jMg6bPBJ7hvIpH0ivt9VKQgQ'
    address = input("Insert Location: ")
    g = geocoder.google(address, key=api_key)
    if g.ok:
        lat, lng = g.latlng
        print(f'Latitud: {lat}, Longitud: {lng}')
    else:
        print("We couldn't reach the data")
        return


    start_date = input("Insert start date in format YYYY-MM-DD: ")
    end_date = input("Insert end date in format YYYY-MM-DD: ")
    
    timezones = [
    "America/Anchorage",
    "America/Los_Angeles",
    "America/Denver",
    "America/Chicago",
    "America/New_York",
    "America/Sao_Paulo",
    "GMT+0",
    "Europe/London",
    "Europe/Berlin",
    "Europe/Moscow",
    "Africa/Cairo",
    "Asia/Bangkok",
    "Asia/Singapore",
    "Asia/Tokyo",
    "Australia/Sydney",
    "Pacific/Auckland"
]
    for timezone in timezones:
        print(timezone)

    input_value = input("Insert the Time Zone from the list above: ")

    if input_value =="GMT+0":
        input_value = "GMT"
    elif input_value not in timezones:
        print("Insert a valid Time Zone")
        return
    else:
        input_value=input_value.replace("/","%2F")

    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lng}74&start_date={start_date}&end_date={end_date}&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum&timezone={input_value}"
    dates = []
    code = []
    min_temperature = []
    max_temperature = []
    latitude = []
    longitude = []
    
   
    try:
        response = requests.get(f"{url}")
        if response.ok:
            response = response.json()
            
            lat = float(response.get("latitude"))
            long = round(float(response.get("longitude")),2)
            for time, weather_code, min_temp, max_temp in zip(response['daily']['time'],
                                                              response['daily']['weather_code'],
                                                              response['daily']['temperature_2m_min'],
                                                              response['daily']['temperature_2m_max']):
                 dates.append(time)
                 code.append(weather_code)
                 min_temperature.append(min_temp)
                 max_temperature.append(max_temp)
                 latitude.append(lat)
                 longitude.append(long)    
        
    except Exception as ex:
        print(f"There was an error: {ex}") 
    write_to_database(dates, code, min_temperature, max_temperature, latitude, longitude)
    
path = "C:/Users/user/OneDrive - Teesside University/Desktop/Software for Digital Innovation/ICA/CIS4044-N-ICA/CIS4044-N-ICA/db/metro_db.db"

def write_to_database(dates,code, min_temperature,max_temperature, latitude, longitude):
    try:
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()

            cursor.execute("DROP TABLE IF EXISTS [Data];")
            conn.commit()
            cursor.execute("""CREATE TABLE IF NOT EXISTS [Data] (
                            date TEXT NOT NULL,
                            code INT NOT NULL,
                            min_temperature REAL NOT NULL,
                            max_temperature REAL NOT NULL,
                            latitude REAL NOT NULL,
                            longitude REAL NOT NULL
                            );""")
            conn.commit()
            data_to_insert = list(zip(dates, code, min_temperature, max_temperature, latitude, longitude))
            cursor.executemany("""
                INSERT INTO [Data] (date, code, min_temperature, max_temperature, latitude, longitude)
                VALUES (?, ?, ?, ?, ?, ?)
            """, data_to_insert)
            conn.commit()
            print(f'Data successfully storage.')
    except Exception as ex:
        print(f"There was an error with the database: {ex}")

fetch_data_from_api()

