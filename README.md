# API Data Processing Project

This project fetches data from an API, processes it, and saves the processed data into a CSV file. The project is built using Python, Flask for the API, and pandas for data processing. The goal of this project is to showcase the ability to work with APIs, handle and preprocess data, and deploy a Flask app.

## Project Overview

- **API Fetching:** Data is fetched from an external API using the `requests` library.
- **Data Preprocessing:** The raw data is cleaned and processed using `pandas` (missing columns are handled, and required transformations are done).
- **API Deployment:** The project includes a Flask app to serve the data and expose relevant endpoints.

## Features

- Fetches data from an API
- Preprocesses data (handles missing fields, checks column consistency)
- Serves data using a Flask API
- Saves processed data to a CSV file
- Allows interaction through API endpoints for data retrieval
