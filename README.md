# Open Meteo 2024 ICA

This project is developed with three different Python files that allow users to explore a historical meteorology database, generate graphs using the data from the selected database, and create a new database with data pulled from an external API at [Open Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api).

## General Description

### Phase 1 and Phase 2

#### Requirements to Execute the Program:

- Install SQLite3: 
  ```bash
  pip install sqlite3
  ```

#### Description

1. **Data Retrieval from Database**:  
   This program executes different functions to pull data from a specified database. If the database needs to be changed, the `path` variable should be updated with the new path where the database is located on your device.

2. **User Prompt**:  
   Upon execution, the program will display the prompt:
   ```
   Do you want to start the program? (Y/N):
   ```
   This ensures the user intends to execute the program. The prompt will appear every time the user finishes any consultation option, until "N" is entered. Any other input will result in a loop until "Y" or "N" is entered.

3. **Consultation Menu**:  
   When the user enters "Y", a menu with different types of queries will appear as shown below. To proceed, the user must enter a letter corresponding to the desired function.
   ```
   A - Select all countries
   B - Select all cities
   C - Average annual temperature for desired city ID in desired year
   D - Average seven-day precipitation for desired city ID starting from desired date
   E - Average mean temperature by city between desired dates
   F - Average annual precipitation by country for desired year
   Enter the letter corresponding to the function you want to execute:
   ```

4. **Phase 1 and Phase 2 Input Management**:  
   Options A and B will be displayed automatically. However, other options will prompt the user for specific details to provide the requested data. The values the user will be prompted to enter are as follows:
   - **City ID**: Values from 1 to 4 are accepted.
   - **Year**: Values from 2020 to 2022 are accepted.
   - **Dates**: The accepted date format is `YYYY-MM-DD`.

---

### Phase 3

#### Requirements to Execute the Program:

- Install SQLite3:
  ```bash
  pip install sqlite3
  ```

- Install requests:
  ```bash
  pip install requests
  ```

- Install geocoder:
  ```bash
  pip install geocoder
  ```

#### Description

1. **Data Retrieval from External APIs**:  
   This program executes a function that requests data from two external APIs and stores or replaces the data in a new dataset saved at the given path. If the user wants to change the location of the created database, the `path` variable must be updated with the desired location.

2. **API Key**:  
   The program includes a predefined API key for the Google Maps API. If the key needs to be changed, the `api_key` variable must be updated with the new key.

3. **User Input**:  
   When executed, the program will prompt:
   ```
   Insert Location: (mighr be unavailable due api key expired)
   ```
   The user must input the desired location (e.g., "London"). After this input, the latitude and longitude for the location will be displayed. Then, the prompt for the start date will appear in the format `YYYY-MM-DD`, followed by the end date. After entering the dates, a list of timezones will be displayed, as shown below. The user must select one option from the list.
   
   ```
   America/Anchorage
   America/Los_Angeles
   America/Denver
   America/Chicago
   America/New_York
   America/Sao_Paulo
   GMT+0
   Europe/London
   Europe/Berlin
   Europe/Moscow
   Africa/Cairo
   Asia/Bangkok
   Asia/Singapore
   Asia/Tokyo
   Australia/Sydney
   Pacific/Auckland
   ```

4. **Phase 3 Input Management**:
   - **Location**: Any address can be added.
   - **Start and End Date**: Dates must be entered in the format `YYYY-MM-DD`.
   - **Time Zone**: The user must select a time zone from the list.

5. **Data Storage Success**:  
   After the program completes, if everything goes as expected, the message `"Data successfully stored"` will appear. If there is an error, the message `"There was an error"` will be displayed.
