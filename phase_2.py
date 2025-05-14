import matplotlib.pyplot as plt 
import sqlite3
path = "C:/Users/user/OneDrive - Teesside University/Desktop/Software for Digital Innovation/ICA/CIS4044-N-ICA/CIS4044-N-ICA/db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db"
with sqlite3.connect(path) as conn:
     conn.row_factory = sqlite3.Row

 #Bar chart to show the 7-day precipitation for a specific town/city    
def bar_chart(conn, cityID, start_date):
     cursor = conn.cursor()
     query = '''SELECT dw.date, dw.precipitation,c.name
                FROM daily_weather_entries dw
                INNER JOIN [cities] c ON dw.city_id = c.id 
                WHERE dw.city_id = ? 
                AND dw.date BETWEEN ? AND DATE(?, '+7 days')'''
     cursor.execute(query,(cityID,start_date, start_date))
     result = cursor.fetchall()

     dates = [row[0] for row in result]
     precipitation = [row[1] for row in result]
     city_name = result[0]['name']

     plt.bar(dates, precipitation, color='blue')
     plt.xlabel('Date')
     plt.ylabel('Precipitation (mm)')
     plt.title(f'7-day Precipitation for City {city_name} ID {cityID} from {start_date}')
     plt.xticks(rotation=45)
     plt.tight_layout()
     plt.show()
#bar_chart(conn,1,'2022-01-01')

#Bar Chart for a Specified Period for a Specified Set of Towns/Cities
def barchart_period_time(conn, date_from, date_to):

     cursor = conn.cursor()
     query = '''SELECT c.name,ROUND(AVG(dw.precipitation),2)
                FROM daily_weather_entries dw
                INNER JOIN [cities] c ON dw.city_id = c.id
                WHERE dw.date BETWEEN ? AND ?
                GROUP BY c.name'''
     cursor.execute (query,(date_from,date_to))
     result = cursor.fetchall()

     cities = [row[0]for row in result]
     avg_precipitation = [row[1] for row in result]

     plt.bar(cities, avg_precipitation, color='blue')
     plt.xlabel('Date')
     plt.ylabel('Precipitation (mm)')
     plt.title(f'Precipitation for City from {date_from} to {date_to}')
     plt.xticks(rotation=45)
     plt.tight_layout()
     plt.show()

#barchart_period_time(conn,'2020-01-01', '2020-10-10')

# Bar Chart Showing the Average Yearly Precipitation by Country
def barchart_avg_yearly(conn, year):
     cursor = conn.cursor()
     query = '''SELECT c.name,ROUND(AVG(dw.precipitation),2)
                FROM daily_weather_entries dw
                INNER JOIN [cities] ci ON ci.id = dw.city_id
                INNER JOIN [countries] c ON ci.country_id = c.id
                WHERE dw.date LIKE ?
                GROUP BY c.name'''
     cursor.execute (query,(f'{year}%',))
     result = cursor.fetchall()

     countries = [row[0] for row in result]
     precipitation = [row[1] for row in result]
     
    
     bars = plt.bar(countries, precipitation, color='red')
     plt.bar_label(bars, labels=precipitation, fontsize=10, color='black')
     plt.xlabel('Country')
     plt.ylabel('Average Precipitation (mm)')
     plt.title(f'Average Yearly Precipitation per Country for {year}')
     plt.xticks(rotation=45)
     plt.tight_layout()
     plt.show()

#barchart_avg_yearly(conn,2020)

#Grouped bar charts for displaying the min/max/mean temperature and precipitation 
# values for selected cities or countries

def min_max_avg(conn,data_base):
     try:
          cursor = conn.cursor()
          if data_base == "cities":
               query = '''SELECT ci.name, 
                         MIN(dw.mean_temp), MAX(dw.mean_temp), ROUND(AVG(dw.mean_temp),2),
                         MIN(dw.precipitation),MAX(dw.precipitation),ROUND(AVG(dw.precipitation),2)
                         FROM daily_weather_entries dw
                         INNER JOIN [cities] ci ON ci.id = dw.city_id
                         INNER JOIN [countries] c ON ci.country_id = c.id
                         GROUP BY ci.name'''
          elif data_base == "countries":
               query = '''SELECT c.name, 
                         MIN(dw.mean_temp), MAX(dw.mean_temp), ROUND(AVG(dw.mean_temp),2),
                         MIN(dw.precipitation),MAX(dw.precipitation),ROUND(AVG(dw.precipitation),2)
                         FROM daily_weather_entries dw
                         INNER JOIN [cities] ci ON ci.id = dw.city_id
                         INNER JOIN [countries] c ON ci.country_id = c.id
                         GROUP BY ci.name'''
          else:
               print(f"Invalid Data Base")
               return

          cursor.execute (query)
          result = cursor.fetchall()

          name = [row['name'] for row in result]
          min_temp = [row[1] for row in result]
          max_temp = [row[2] for row in result]
          avg_temp = [row[3] for row in result]
          min_precipitation = [row[4] for row in result]
          max_precipitation = [row[5] for row in result]
          avg_precipitation = [row[6] for row in result]

          plt.style.use("ggplot")
          fig, [[ax1, ax2, ax3],[ax4,ax5,ax6]] = plt.subplots(nrows = 2, ncols = 3, sharey = True, figsize = [14, 8])
          
          ax1.set_xlabel("Min Temperature")
          ax1.set_ylabel("Ubication")
          ax1.barh(name, min_temp, label = "Min Temperature")
          ax1.legend(loc = 0)

          ax2.set_xlabel("Max Temperature")
          ax2.set_ylabel("Ubication")
          ax2.barh(name, max_temp, label = "Max Temperature")
          ax2.legend(loc = 0)

          ax3.set_xlabel("Avg. Temperature")
          ax3.set_ylabel("Ubication")
          ax3.barh(name, avg_temp, label = "Avg. Temperature")
          ax3.legend(loc = 0)

          ax4.set_xlabel("Min Precipitation")
          ax4.set_ylabel("Ubication")
          ax4.barh(name, min_precipitation, label = "Min Precipitation")
          ax4.legend(loc = 0)

          ax5.set_xlabel("Max Precipitation")
          ax5.set_ylabel("Ubication")
          ax5.barh(name, max_precipitation, label = "Max Precipitation")
          ax5.legend(loc = 0)

          ax6.set_xlabel("Avg. Precipitation")
          ax6.set_ylabel("Ubication")
          ax6.barh(name, avg_precipitation, label = "Avg Precipitation")
          ax6.legend(loc = 0)

          fig.tight_layout()

          plt.show()
     except Exception as ex:
          print(f"An error occurred: {ex}")

#min_max_avg(conn,'countries')

# Multi-line chart to show the daily minimum and maximum temperature for a given month for a 
# specific city.
def multi_line(conn, cityID, month):
     cursor = conn.cursor()
     query = '''SELECT strftime('%d', dw.date), MIN(dw.min_temp), MAX(dw.max_temp), ci.name, strftime('%m', dw.date)
                FROM daily_weather_entries dw
                INNER JOIN [cities] ci ON ci.id = dw.city_id
                WHERE dw.city_id = ? 
                AND strftime('%m', dw.date) = ?
                GROUP BY strftime('%d', dw.date)''' 
     
     cursor.execute(query,(cityID,f'{month:02d}'))
     result = cursor.fetchall()

     dates = [row[0] for row in result]
     min_temp = [row[1] for row in result]
     max_temp = [row[2] for row in result]
     city = result[0]['name']
     month = result[0][4]
     
     fig, ax = plt.subplots(figsize=(12, 6))
     ax.plot(dates, max_temp, label='Avg Max Temperature', color='orange')
     ax.plot(dates, min_temp, label='Avg Min Temperature', color='blue')

     ax.tick_params(axis='x', labelrotation=90, labelsize=8)
     ax.grid(True)
     ax.set_xlabel('Days')
     ax.set_ylabel('Temperature (°C)')
     ax.set_title(f'Average Daily Min/Max Temperature for City {city} in month {month}')
     ax.legend()

     fig.tight_layout()
     plt.show()
#multi_line(conn, 1, 10)

#Scatter plot chart for average temperature against average rainfall
#  for town/city/country/all countries etc.

def scatter_plot_avg_temp_vs_rainfall(conn,cityID):
    cursor = conn.cursor()
    # Query to get the average temperature and average precipitation for the specified city
    query = '''SELECT dw.mean_temp, dw.precipitation, ci.name
               FROM daily_weather_entries dw
               INNER JOIN [cities] ci ON ci.id = dw.city_id
               INNER JOIN [countries] c ON ci.country_id = c.id
               WHERE dw.city_id = ? 
               '''
    
    cursor.execute(query,(cityID,))
    result = cursor.fetchall()
    mean_temp = [row[0] for row in result]
    precipitation = [row[1] for row in result]
    city = result[3]['name']

    
    print(city)
    plt.scatter(mean_temp,precipitation,c="#f5b342",alpha=0.5)
    
    plt.title(f"Mean Temperature against Rainfall in{city}")

    plt.xlabel("Avg. Temperature")

    plt.ylabel("Precipitation")

    plt.show()
#scatter_plot_avg_temp_vs_rainfall(conn,1)

def execute():
     while True:
          initiate= input("Do you want to start the program? (Y/N): ").upper()
          if initiate == "Y":
               print("A - Bar chart to show the 7-day precipitation for a specific town/city")
               print("B - Bar Chart for a Specified Period for a Specified Set of Towns/Cities")
               print("C - Bar Chart Showing the Average Yearly Precipitation by Country")
               print("D - Grouped bar charts for displaying the min/max/mean temperature and precipitation")
               print("E - Multi-line chart to show the daily minimum and maximum temperature for a given month for a specific city.")
               print("F - Scatter plot chart for average temperature against average rainfall for town/city/country/all countries")
               choice = input("Enter the letter corresponding to the function you want to execute: ").upper()
               try:
                    if choice == "A":
                         city_id = input("Give a city ID between 1 to 4: ")
                         start_date = input("Give a starting date in format YYYY-MM-DD from 2020 to 2022: ")
                         
                         bar_chart(conn, city_id, start_date)
                    elif choice == "B":
                         date_from = input("Give a start date in format YYYY-MM-DD from 2020 to 2022: ")
                         date_to = input("Give an end date in format YYYY-MM-DD from 2020 to 2022: ")
                         
                         barchart_period_time(conn, date_from, date_to)
                    elif choice == "C":
                         year = input("Give a year between 2020 to 2022: ")
                         
                         barchart_avg_yearly(conn, year)
                    elif choice == "D":
                         data_base = input("Enter 'cities' or 'countries' to display the grouped bar chart: ").lower()
                         
                         min_max_avg(conn, data_base)
                    elif choice == "E":
                         city_id = input("Give a city ID: ")
                         month = int(input("Give a month as number (1-12): "))
                         
                         multi_line(conn, city_id, month)
                    elif choice == "F":
                         city_id = input("Give a city ID: ")
                         
                         scatter_plot_avg_temp_vs_rainfall(conn, city_id)
                    else:
                         print("Invalid choice. Please enter a valid letter (A-F).")
               except Exception as ex:
                    print(f"An error occurred: {ex}")
          elif initiate == 'N':
            print("Exiting the program.")
            break
execute()         