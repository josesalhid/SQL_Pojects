# Author: Jose Carlos Saldana Hidalgo
# Student ID: E4202165

import sqlite3
# Phase 1 - Starter
# 
# Note: Display all real/float numbers to 2 decimal places.    
'''
Satisfactory
'''
path = "C:/Users/user/OneDrive - Teesside University/Desktop/Software for Digital Innovation/ICA/CIS4044-N-ICA/CIS4044-N-ICA/db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
with sqlite3.connect(path) as conn:
     conn.row_factory = sqlite3.Row

def select_all_countries():
    cursor = conn.cursor()
    # Queries the database and selects all the countries 
    # stored in the countries table of the database.
    # The returned results are then printed to the 
    # console.
    try:                        
        # Define the query
            query = cursor.execute("SELECT * FROM countries")
           
        # Get a cursor object from the database connection
        # that will be used to execute database query.

        # Execute the query via the cursor object.

        # Iterate over the results and display the results.
            for row in query:
                print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")

    except sqlite3.OperationalError as ex:
        print(ex)

def select_all_cities():
    cursor = conn.cursor()
    try:
        query = conn.execute("SELECT * FROM cities")
        for row in query:
            print(f"City Id: {row['id']} -- City Name: {row['name']} -- City Longitude: {row['longitude']} -- City Latitude{row['latitude']} -- Country ID {row['country_id']}")

    except sqlite3.OperationalError as ex:
        print(ex)

def average_annual_temperature(conn, cityID, year):
    
    cursor = conn.cursor()
    try:
        query = cursor.execute('''SELECT AVG(dw.mean_temp),c.name
                                FROM daily_weather_entries dw
                                INNER JOIN [cities] c ON dw.city_id = c.id 
                                WHERE dw.city_id = ? 
                                AND dw.date LIKE ?''',(cityID,f'{year}%'))
            
        for row in query:
            avg_temp = round(row[0],2)
            city_name = row[1]
            print(f"The average temperature for city ID {cityID} city name {city_name} in year {year} is {avg_temp:.2f} °C")
    except sqlite3.OperationalError as ex:
        print(ex)

def average_seven_day_precipitation(conn, cityID, start_date):
    
    cursor = conn.cursor()
    query = '''SELECT AVG(dw.precipitation),c.name
                FROM daily_weather_entries dw
                INNER JOIN [cities] c ON dw.city_id = c.id 
                WHERE dw.city_id = ? 
                AND dw.date BETWEEN ? AND DATE(?, '+7 days')'''
    result = cursor.execute(query,(cityID,start_date, start_date))

        
    for row in result:
        precipitation = round(row[0],2)
        city_name = row[1]
        print(f"The average seven day precipitation for city ID {cityID} city name {city_name} from {start_date} is {precipitation} cm³")
    
def average_mean_temp_by_city(conn, date_from, date_to):
   
    cursor = conn.cursor()
    query = '''SELECT AVG(dw.mean_temp),c.name
                FROM daily_weather_entries dw
                INNER JOIN [cities] c ON dw.city_id = c.id 
                WHERE dw.date BETWEEN ? AND ?
                GROUP BY c.name'''
    cursor.execute(query,(date_from,date_to))
    results = cursor.fetchall()
      
    for row in results:
        mean_temp = round(row[0], 2)  
        city_name = row[1]
        print(f"City: {city_name}, Average Temperature: {mean_temp}°C")

def average_annual_precipitation_by_country(conn, year):
    cursor = conn.cursor() 
    query = '''SELECT AVG(dw.precipitation),c.name
                FROM daily_weather_entries dw
                INNER JOIN [cities] ci ON ci.id = dw.city_id
                INNER JOIN [countries] c ON ci.country_id = c.id
                WHERE dw.date LIKE ?
                GROUP BY c.name'''
    cursor.execute(query,(f'{year}%',))
    results = cursor.fetchall()
      
    for row in results:
        precipitation = round(row[0], 2)  
        country_name = row[1]
        print(f"Country: {country_name}, Annual Average Precipitation: {precipitation}cm³")


'''
Excellent

You have gone beyond the basic requirements for this aspect.

'''
def execute():  
    while True:
        initiate= input("Do you want to start the program? (Y/N): ").upper()
        if initiate == "Y":
            print("A - Select all countries")
            print("B - Select all cities")
            print("C - Average annual temperature for desired city ID in desired year")
            print("D - Average seven day precipitation for desired city ID starting from desired date")
            print("E - Average mean temperature by city between desired dates")
            print("F - Average annual precipitation by country for desired year")
            choice = input("Enter the letter corresponding to the function you want to execute: ").upper()
            try:
                
                if choice == "A":
                    print("\nSelecting all countries:")
                    select_all_countries()
                elif choice == "B":
                    print("\nSelecting all cities:")
                    select_all_cities()
                elif choice == "C":
                    id = input("Give a city ID between 1 to 4: ")
                    year = input("Give a year between 2020 to 2022: ")
                    print(f"\nAverage annual temperature for city {id} in {year}:")
                    average_annual_temperature(conn, id, year)
                elif choice == "D":
                    id = input("Give a city ID between 1 to 4: ")
                    date = input("Give a starting date in format YYYY-MM-DD from 2020 to 2022: ")
                    print(f"\nAverage seven day precipitation for city ID {id} starting from {date}:")
                    average_seven_day_precipitation(conn, id, date)
                elif choice == "E":
                    date1 = input("Give a start date in format YYYY-MM-DD from 2020 to 2022: ")
                    date2 = input("Give a end date in format YYYY-MM-DD from 2020 to 2022: ")
                    print(f"\nAverage mean temperature by city from {date1} to {date2}")
                    average_mean_temp_by_city(conn, date1, date2)
                elif choice == "F":
                    year = input("Give a year between 2020 to 2022: ")
                    print(f"\nAverage annual precipitation by country for {year}:")
                    average_annual_precipitation_by_country(conn, year)
                else:
                    print("Invalid choice. Please enter a valid letter (A-F).")
            except Exception as ex:
                print(f"An error occurred: {ex}")
        elif initiate == "N":
            print("Exiting the program.")
            break

execute()

