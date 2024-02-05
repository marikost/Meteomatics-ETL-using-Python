import pandas as pd
from sqlalchemy import create_engine
import os
import config


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

# Create a connection to the PostgreSQL database
engine = create_engine(F"{os.getenv('POSTGRES_DRIVER')}://{os.getenv('POSTGRES_USERNAME')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DATABASE')}")

# Query the table and load it into a Pandas DataFrame
query = f'SELECT * FROM {config.table_name};'
df = pd.read_sql_query(query, engine)

# Export the DataFrame to a CSV file
df.to_csv(config.csv_file_path, index=False)

print(f'Table "{config.table_name}" exported to {config.csv_file_path}')
