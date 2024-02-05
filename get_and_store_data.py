import requests
from requests.auth import HTTPBasicAuth
from sqlalchemy import create_engine
from geopy.geocoders import Nominatim
import config
import pandas as pd
from datetime import datetime
import os



def get_api_data(latitude, longitude):
    # The complete url address
    full_url_address = f'{config.base}/{config.time_period}:{config.frequency}/{config.parameters}/{latitude},{longitude}/{config.output_format}'
    # Parse the response content as json
    try:
        # Making an HTTP GET request with basic authentication.
        response = requests.get(full_url_address, auth=HTTPBasicAuth(username, password))
        x = response.json()
        if x['status'] == 'OK':
            return x['data']
        else:
            print(" No city with that name ")
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


if __name__ == '__main__':
    # Load environment variables from .env file
    with open(config.env_file_path, 'r') as file:
        for line in file:
            # Skip lines that are comments or empty
            if line.startswith('#') or not line.strip():
                continue

            # Split the line into key and value
            key, value = line.strip().split('=', 1)

            # Set the environment variable
            os.environ[key] = value

    # Access the loaded environment variables
    username = os.getenv('METEO_USERNAME')
    password = os.getenv('METEO_PASSWORD')
    engine = create_engine(F"{os.getenv('POSTGRES_DRIVER')}://{os.getenv('POSTGRES_USERNAME')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DATABASE')}")
    df = pd.DataFrame()
    cr = config.create

    for city_name in config.cities:

        # find the latitude and longitude of the cities
        geolocator = Nominatim(user_agent="user_agent")

        # try valid city name
        try:
            location = geolocator.geocode(city_name)
            latitude = str(location.latitude)
            longitude = str(location.longitude)
        except AttributeError as e:
            print('There is no city')

        api_data = get_api_data(latitude, longitude)

        df = pd.DataFrame()
        # Convert into correct datetime format
        df['forecast_date'] = [datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%SZ') for x in api_data[0]['coordinates'][0]['dates']]
        for par in api_data:
            df[par['parameter'].split(':')[0]] = [p['value'] for p in par['coordinates'][0]['dates']]
        df['city'] = city_name

        # Append data after the first iteration
        if cr == 1:
            # If the table already exists in the database
            df.to_sql(config.table_name, engine, if_exists='replace', index=False)
            cr = 0
        else:
            df.to_sql(config.table_name, engine, if_exists='append', index=False)

        print(f'stored forecasts for {city_name}')