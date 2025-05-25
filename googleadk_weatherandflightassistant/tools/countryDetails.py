import requests

def get_country_details(country_name:str)->dict:
    """
    Fetches details about a country using the REST Countries API.

    Args:
        country_name (str): The name of the country to fetch details for.

    Returns:
        dict: A dictionary containing the following keys:
            - 'currency': The currency used in the country (e.g., 'Indian Rupee').
            - 'language': The primary language spoken in the country (e.g., 'Hindi').
            - 'capital_city': The capital city of the country (e.g., 'New Delhi').
            - 'calling_code': The international calling code of the country (e.g., '+91').
            - 'region': The region where the country is located (e.g., 'Asia').

    Raises:
        ValueError: If the API response does not contain the expected data.
        requests.exceptions.RequestException: If there is an issue with the API request.
    """
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    try:
        response = requests.get(url)
        # response.raise_for_status()
        data = response.json()

        if not data or not isinstance(data, list):
            raise ValueError("Invalid response from API")

        country_data = data[0]

        # Extracting required details
        currency = list(country_data['currencies'].values())[0]['name'] if 'currencies' in country_data else None
        language = list(country_data['languages'].values())[0] if 'languages' in country_data else None
        capital_city = country_data['capital'][0] if 'capital' in country_data else None
        calling_code = f"+{country_data['idd']['root']}{country_data['idd']['suffixes'][0]}" if 'idd' in country_data else None
        region = country_data['region'] if 'region' in country_data else None

        return {
            'currency': currency,
            'language': language,
            'capital_city': capital_city,
            'calling_code': calling_code,
            'region': region
        }

    except requests.exceptions.RequestException as e:
        print(f"Error Details: {e}")
        # raise requests.exceptions.RequestException(f"API request failed: {e}")
    except (KeyError, IndexError, ValueError) as e:
        raise ValueError(f"Error processing API response: {e}")
    
if __name__=="__main__":
    country_info = get_country_details("Poland")
    print(country_info)