import csv
from fast_flights import FlightData, Passengers, Result, get_flights


FILE_PATH = 'data/city_airport_codes.csv'

def get_airport_code(city_name, file_path=FILE_PATH):
    """
    Extracts the airport code for a given city name from a CSV file.

    Args:
        city_name (str): The name of the city to search for.
        file_path (str): The path to the CSV file.

    Returns:
        str: The airport code if found, or a message indicating it was not found.
    """
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if city_name.lower() in row['City Name'].lower():
                return row['Airport Code']
    return f"Airport code for '{city_name}' not found."

# def search_flights(flight_date:str, from_city:str, to_city:str, adults:int=1, children:int=0, infants_in_seat:int=0, infants_on_lap:int=0, trip:str="round-trip", seat:str="economy")->dict:
def search_flights(flight_date:str, from_city:str, to_city:str, adults_count:int, children_count:int, infants_in_seat:int, infants_on_lap:int, trip_detail:str, seat_class:str)->dict:
    """
    Searches for flights.

    Args:
        flight_date (str): The date of the flight in YYYY-MM-DD format, must be a future date.
        from_city (str): Flight origin city.
        to_city (str): Flight destination city.
        trip (str): Type of trip - "one-way" or "round-trip" or "multi-city".
        seat (str): Seat class - "economy" or "premium-economy" or "business" or "first".
        adults (int): Number of adult passengers.
        children (int): Number of child passengers.
        infants_in_seat (int): Number of infants requiring a seat.
        infants_on_lap (int): Number of infants sitting on laps.

    Returns:
        dict: The result object containing flight details or an error message.
    """
    try:
        from_airport = get_airport_code(city_name=from_city)
        to_airport = get_airport_code(city_name=to_city)
        
        
        print(f"Search Flights function called Date:{flight_date}, from_city:{from_city}, to_city:{to_city}, adults:{adults_count}, children:{children_count}, infants_in_seat:{infants_in_seat}, infants_on_lap:{infants_on_lap}, trip:{trip_detail}, seat:{seat_class}, from_airport:{from_airport}, to_airport:{to_airport} ")
        
        # Perform the flight search
        results :Result = get_flights(flight_data = [FlightData(date=flight_date, from_airport=from_airport, to_airport=to_airport)],
                                      passengers=Passengers(adults=adults_count,children=children_count, infants_in_seat=infants_in_seat, infants_on_lap=infants_on_lap),
                                      trip=trip_detail,
                                      seat=seat_class,
                                      fetch_mode='fallback')

        # Return the search results
        return {"status":"success", "flight_info":results.flights}
    except Exception as e:
        print(f"--ERROR DETAILS --\n{e}\n")
        # Handle any errors during the search
        return {"status":"error", "message": str(e)}
    
    

# Example usage
if __name__ == "__main__":
    result = search_flights(
        flight_date="2025-05-30",
        from_city="Minneapolis",
        to_city="Calgary",
        trip="one-way",
        seat="economy",
        adults=1,
        children=0,
        infants_in_seat=0,
        infants_on_lap=0
    )
    # print(result)
    # print(f"We found {len(result)} flights.\n")
    # print(result)
    for flight in result['flight_info']:
        print(f"Flight:{flight.name}, Duration:{flight.duration}, Stops:{flight.stops} Departure:{flight.departure}, Arrival:{flight.arrival}, Price:{flight.price} \n")
