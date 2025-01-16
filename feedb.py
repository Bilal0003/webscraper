import json
import psycopg2
import os
from dotenv import load_dotenv

# Load the JSON data
with open("AppleWatchSE2.json") as f:
    data = json.load(f)


load_dotenv()
# Connect to the database
try:
    conn = psycopg2.connect(
        database="applewatch",
        host="localhost",
        user="user",
        password="password",
        port="5432",
    )
    print("Connection established to PostgreSQL db.")

except Exception as e:
    print(f"Exception occured trying to connect to local postgreSQL server : {str(e)}")


with conn.cursor() as cur:
    try:
        # Create a table (adjust the schema as needed)
        cur.execute(
            """CREATE TABLE apple_watch (
            id SERIAL PRIMARY KEY,
            title VARCHAR(1000),
            imgSrc VARCHAR(1000),
            rating float,
            price float);"""
        )

        # Insert the JSON data into the table
        for i, product in enumerate(data):
            # check if current dict not empy

            if not product == False:
                query = f"""INSERT INTO apple_watch (title, imgSrc, rating, price) VALUES (
                '{product['title']}', 
                '{product['imgSrc'].strip()}', 
                '{float(product['rating'].strip().replace("," , "."))}', 
                '{float(product['price'].strip().replace("," , "."))}');"""

                cur.execute(query)

        # Commit the transaction
        conn.commit()

        # Close the connection
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Exception occured within cursor: {str(e)}")
