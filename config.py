# variable to store the url
base = "https://api.meteomatics.com"

# describes the time interval (seven-days)
time_period = 'todayT00:00:00ZPT167H'
# describes the time step (1-hour)
frequency = 'PT1H'
temperature = 't_2m:C'
# describes the absolute humidity 2 meters above ground (gm3)
humidity = 'absolute_humidity_2m:gm3'
# describes the Instantaneous wind speed at 10m above ground
wind_speed = 'wind_speed_10m:ms'
# describes the mean sea level pressure in hectopascal (hPa) or pascal (Pa)
msl_pressure = 'msl_pressure:hPa'

# Useful format of the parameters
parameter_list = [temperature.split(":")[0], humidity.split(":")[0], wind_speed.split(":")[0],msl_pressure.split(":")[0]]
parameters = f'{temperature},{humidity},{wind_speed},{msl_pressure}'

# api output
output_format = 'json'

# Cities input of the user
cities = ["rome", "paris", "london"]

#  Name of the table in the Postgres database
table_name = 'forecasts'

# Set create = 1 if you want to create a new table and create = 0 if you want to append to the previous table
create = 1

# Sensitive information file
env_file_path = '.env'

# Specify the path where you want to save the CSV file
csv_file_path = 'exports/forecast.csv'
