import psycopg2
import config
from fastapi import FastAPI
import os

app = FastAPI()

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

@app.get("/latest-forecast")
def latest_forecast():
    conn = psycopg2.connect(database=os.getenv('POSTGRES_DATABASE'), user=os.getenv('POSTGRES_USERNAME'), password=os.getenv('POSTGRES_PASSWORD'), host=os.getenv('POSTGRES_HOST'), port= os.getenv('POSTGRES_PORT'))
    conn.autocommit = True
    cur = conn.cursor()

    with open("queries/distinct_cities.sql", "r") as sql_file:
        sql_query = sql_file.read()
    cur.execute(sql_query)
    rows = cur.fetchall()
    # Convert the list of tuples into a list of lists
    result_list = [str(value) for row in rows for value in row]

    dictionary = {}
    for name in result_list:
        # Read the SQL file
        with open("queries/latest_forecast.sql", "r") as sql_file:
            sql_query_template = sql_file.read()

        # Replace :parameter_name with the actual parameter value
        sql_query = sql_query_template.replace(":name", name)

        parameters_str = ', '.join(config.parameter_list)
        sql_query = sql_query.replace(":parameter", parameters_str)

        # Execute the modified SQL query
        cur.execute(sql_query)
        columns = [column.name for column in cur.description]
        rows = cur.fetchall()
        # Convert each row to a dictionary with column names as keys
        result_dicts = [dict(zip(columns, row)) for row in rows]

        dictionary[name] = result_dicts

    cur.close()
    conn.close()
    return dictionary

@app.get("/average-3-forecasts")
def average_3_forecasts():
    conn = psycopg2.connect(database=os.getenv('POSTGRES_DATABASE'), user=os.getenv('POSTGRES_USERNAME'), password=os.getenv('POSTGRES_PASSWORD'), host=os.getenv('POSTGRES_HOST'), port= os.getenv('POSTGRES_PORT'))
    conn.autocommit = True
    cur = conn.cursor()

    with open("queries/distinct_cities.sql", "r") as sql_file:
        sql_query = sql_file.read()
    cur.execute(sql_query)
    rows = cur.fetchall()
    # Convert the list of tuples into a list of lists
    result_list = [str(row[0]) for row in rows]

    dictionary = {}
    for name in result_list:
        # Read the SQL file
        with open("queries/average_3_forecasts.sql", "r") as sql_file:
            sql_query_template = sql_file.read()

        # Replace :parameter_name with the actual parameter value
        sql_query = sql_query_template.replace(":name", name)
        parameters_str = ', '.join(config.parameter_list)

        cast_avg_parameters_str = ', '.join([f'CAST(avg({par}) AS decimal(10,1)) as {par}' for par in config.parameter_list])


        sql_query = sql_query.replace(":avg_parameter", cast_avg_parameters_str)
        sql_query = sql_query.replace(":parameter", parameters_str)
        # Execute the modified SQL query
        cur.execute(sql_query)
        columns = [column.name for column in cur.description]
        rows = cur.fetchall()
        # Convert each row to a dictionary with column names as keys
        result_dicts = [dict(zip(columns, row)) for row in rows]

        dictionary[name] = result_dicts

    cur.close()
    conn.close()
    return dictionary


@app.get("/top-n")
def top_n(n):
    conn = psycopg2.connect(database=os.getenv('POSTGRES_DATABASE'), user=os.getenv('POSTGRES_USERNAME'), password=os.getenv('POSTGRES_PASSWORD'), host=os.getenv('POSTGRES_HOST'), port= os.getenv('POSTGRES_PORT'))
    conn.autocommit = True
    cur = conn.cursor()

    dictionary = {}
    for parameter in config.parameter_list:
        # Read the SQL file
        with open("queries/top_n.sql", "r") as sql_file:
            sql_query_template = sql_file.read()

        # Replace :n with the actual n value
        sql_query = sql_query_template.replace(":n", n)

        # Replace :parameter with the actual parameter value
        sql_query = sql_query.replace(":parameter", parameter)

        # Execute the modified SQL query
        cur.execute(sql_query)
        columns = [column.name for column in cur.description]
        rows = cur.fetchall()
        # Convert each row to a dictionary with column names as keys
        result_dicts = [dict(zip(columns, row)) for row in rows]

        dictionary[parameter] = result_dicts

    cur.close()
    conn.close()
    return dictionary


@app.get("/hourly-min-max-avg")
def hourly_min_max_avg():
    conn = psycopg2.connect(database=os.getenv('POSTGRES_DATABASE'), user=os.getenv('POSTGRES_USERNAME'), password=os.getenv('POSTGRES_PASSWORD'), host=os.getenv('POSTGRES_HOST'), port= os.getenv('POSTGRES_PORT'))
    conn.autocommit = True
    cur = conn.cursor()

    with open("queries/distinct_cities.sql", "r") as sql_file:
        sql_query = sql_file.read()
    cur.execute(sql_query)
    rows = cur.fetchall()
    # Convert the list of tuples into a list of lists
    result_list = [str(row[0]) for row in rows]

    dictionary = {}
    for name in result_list:
        # Read the SQL file
        with open("queries/hourly_min_max_avg.sql", "r") as sql_file:
            sql_query_template = sql_file.read()

        # Replace :parameter_name with the actual parameter value
        sql_query = sql_query_template.replace(":name", name)

        min_max_avg_str = ', '.join([f'MIN({par}) AS min_{par}, MAX({par}) AS max_{par}, CAST(AVG({par}) AS DECIMAL(10,1)) AS avg_{par}' for par in config.parameter_list])


        sql_query = sql_query.replace(":min_max_avg_parameter", min_max_avg_str)
        # Execute the modified SQL query
        cur.execute(sql_query)
        columns = [column.name for column in cur.description]
        rows = cur.fetchall()
        # Convert each row to a dictionary with column names as keys
        result_dicts = [dict(zip(columns, row)) for row in rows]

        dictionary[name] = result_dicts

    cur.close()
    conn.close()
    return dictionary


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


