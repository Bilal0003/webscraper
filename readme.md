# Database App with Docker and PostgreSQL

This project sets up a PostgreSQL database using Docker and populates it with the contents of `AppleWatchSE2.json`.

## Prerequisites

- Docker
- Docker Compose

## Setup

### Step 1: Create a Dockerfile

Create a `Dockerfile` to set up a Python environment where we can run a script to feed the database.

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the script to feed the database
CMD ["python", "feed_database.py"]
```
### Step 2: Create a Docker Compose file
Create a docker-compose.yml file to set up the database and the app.

version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydatabase
    ports:
      - "5432:5432"

  app:
    build: .
    depends_on:
      - db
    environment:
      DATABASE_URL: postgres://user:password@db:5432/mydatabase

### Step 3: Write a script to feed the database
Create a feed_database.py script to read the JSON file and insert its contents into the database.

### Step 4: Create a requirements file
Create a requirements.txt file to specify the Python dependencies.

psycopg2-binary

### Step 5: Build and run the Docker containers
Run the following commands in your terminal:

docker-compose build
docker-compose up

This will set up the PostgreSQL database, build the Python app, and run the script to feed the database with the contents of AppleWatchSE2.json.

## Verification
To verify if the database has been successfully populated, follow these steps:

### Step 1: Connect to the PostgreSQL Database
First, find the container ID of the PostgreSQL container:

docker ps

Look for the container running the postgres image and note its container ID.

Then, connect to the PostgreSQL database using the psql tool:

docker exec -it <container_id> psql -U user -d mydatabase

Replace <container_id> with the actual container ID.

### Step 2: Query the Table
Once you are connected to the database, you can run SQL queries to check the contents of the table. For example:

```SQL
SELECT * FROM apple_watch;
```

This will display all the rows in the apple_watch table.

### Step 3: Exit the Database
To exit the psql tool, simply type:
\q


