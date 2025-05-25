# README.md

## Project Overview
This project, `googleadk_weatherandflightassistant`, is designed to provide tools and utilities for handling flight-related data, including airport codes, flight details, weather information, and validation of flight requests.

## Project Structure
- `__init__.py`: Marks the directory as a Python package.
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `agent.py`: Contains the main logic for the agent functionality.
- `main.py`: Entry point for the application.
- `requirement.txt`: Lists the Python dependencies required for the project.

### Subdirectories
- `data/`: Contains data files used by the project.
  - `city_airport_codes.csv`: A CSV file containing city and airport codes.

- `tools/`: Contains utility scripts for various functionalities.
  - `countryDetails.py`: Handles country-related details.
  - `flightDetails.py`: Manages flight-related information.
  - `validateFlightRequest.py`: Validates flight request data.
  - `weatherDetails.py`: Fetches and processes weather-related information.

## Environment Variables
The project requires the following environment variables to be set in a `.env` file located in the root of the workspace:

### Required Variables
**`The Required Variables can be chosen based on the LLM you use, not all are required`**
- **`AZURE_API_KEY`**: The API key for accessing Azure services.
- **`AZURE_API_BASE`**: The base URL for Azure API endpoints.
- **`AZURE_API_VERSION`**: The version of the Azure API to use.
- **`GOOGLE_WEATHER_API_KEY`**: The API key for accessing Google Weather services.
- **`OPENAI_API_KEY`**: The API key for accessing OpenAI services.
- **`GOOGLE_API_KEY`**: The API key for accessing Google services.

### Example `.env` File
Create a `.env` file in the root of your project and include the following:
