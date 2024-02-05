# Instructions

Create a .env file to store the sensitive information that will be used for the Meteomatics Weather API authentication and for the Dtabase Managment System connection.

METEO_USERNAME=none_kostopoulos_marios  
METEO_PASSWORD=fbst68LQ4R  
POSTGRES_DRIVER=postgresql+psycopg2  
POSTGRES_DATABASE=postgres  
POSTGRES_HOST=localhost  
POSTGRES_PORT=5432  
POSTGRES_USERNAME=postgres  
POSTGRES_PASSWORD=123

### API Endpoints

##### 1)List the latest (last hour) forecast for each location for every day  
##### 2)List the average of the last 3 forecasts for each location for every day 
##### 3)Get the top n locations based on each available metric
##### 4)List the min, max and avergae forecast values for each hour of the day

You will find the API endpoints in the api.py file.

### Process of the overall project  

#####   Get the forecasts for any 3 locations in the period of 7 days
1) Find the API call from meteomatics weather API that returns hourly weekly forecasts for a location(latitude, longitude)  
2) Use geopy library to extract latitude and longitude from a city name 
3) Create .env file to store sensitive information  
4) Decide the format that will recieve the forecasts (JSON)  
5) Depend on the status handle it's response  

##### Store the data in a relational database  
1) Define a function that takes as an argument the forecasts retrieved in the previous step
2) Create an engine that connects with the Database Management System (PostgreSQL) and takes the sensitive connection information from the .env file
3) Decide the appropriate schema
4) Create a Pandas Dataframe which will have the necessary columns

##### Create an API that uses the database data  
1) Decided to work with FastAPI
2) Configure FastAPI with Postgres using .env file to retrieve sensitive information
3) Create SQL queries for the API endpoints

You will find the SQL queries in the 'queries' file.

### Tools  
1) meteomatics Weather API
2) SQL
3) Python
4) FastAPI
5) PostgreSQL
6) psycopg2
7) Pandas
8) geopy.geocoders.Nominatim
9) JSON



