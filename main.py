Creating a complete smart route planner involves integrating various components such as a traffic data API, machine learning for optimization, and a routing algorithm. Below is a simplified version of such a Python program, highlighting how one might build the essential components. Since a fully operational solution would require extensive code and integration with real-world services (e.g., Google Maps API for traffic data), I'll demonstrate the general structure and core elements.

Please note, for a complete and operational system, you will need to handle API keys, real-time data, a proper machine learning model trained on historical data, and potentially more sophisticated error handling and logistics considerations.

```python
import requests
import json
import numpy as np
from sklearn.linear_model import LinearRegression

# Mock data for demonstration
# You would typically train your model with historical traffic data and travel times.
historical_data = {
    'distance': [5, 10, 15, 20],  # in kilometers
    'traffic_delay': [5, 10, 20, 25]  # in minutes
}

# Train a simple linear regression model
X = np.array(historical_data['distance']).reshape(-1, 1)
y = np.array(historical_data['traffic_delay'])

model = LinearRegression()
model.fit(X, y)

def get_real_time_traffic_data(api_key, start, end):
    """
    Fetch real-time traffic data from an external API.
    
    :param api_key: Your API key for the traffic data service
    :param start: Starting location coordinates (latitude, longitude)
    :param end: Ending location coordinates (latitude, longitude)
    :return: Traffic data (JSON response)
    """
    try:
        # Sample API request - change URL to match the real traffic data service you are using.
        url = f"https://api.traffic-service.com/data?api_key={api_key}&start={start}&end={end}"
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the response was an unsuccessful status
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error fetching real-time traffic data:", e)
        return None

def estimate_travel_time(distance, real_traffic_data):
    """
    Estimate travel time based on distance and real-time traffic data.
    
    :param distance: Distance between start and end points
    :param real_traffic_data: Traffic data obtained from API
    :return: Estimated travel time in minutes
    """
    # Error handling for data integrity
    if real_traffic_data is None:
        return "Unable to estimate time due to lack of traffic data."
    
    # Use mock prediction from model
    traffic_delay = model.predict(np.array([[distance]]))[0]
    
    # Adjust estimation with real-time traffic info (simplified example)
    real_time_factor = 1  # In a real-world scenario, this would be derived from real_traffic_data
    estimated_time = (distance / 50) * 60 + traffic_delay * real_time_factor  # Assuming avg speed 50km/h

    return estimated_time

def optimize_route(locations, api_key):
    """
    Optimize the route based on current traffic conditions.
    
    :param locations: List of tuples representing coordinates of stops [(lat1, lon1), (lat2, lon2), ...]
    :param api_key: Your API key for real-time traffic data
    :return: Optimized route with estimated travel times
    """
    optimized_route = []
    for i in range(len(locations) - 1):
        start = locations[i]
        end = locations[i + 1]
        
        distance = 10  # Placeholder for a calculated distance
        # Fetch real-time traffic data
        traffic_data = get_real_time_traffic_data(api_key, start, end)
        
        estimated_time = estimate_travel_time(distance, traffic_data)
        
        optimized_route.append({
            'from': start,
            'to': end,
            'estimated_time': estimated_time
            # You might include more details here such as distance, directions, etc.
        })
    
    return optimized_route

def main():
    api_key = 'YOUR_API_KEY'  # Replace with your actual API key
    locations = [(37.7749, -122.4194), (34.0522, -118.2437), (36.1699, -115.1398)]  # Example lat/lon pairs
    
    try:
        route = optimize_route(locations, api_key)
        print(json.dumps(route, indent=2))
    except Exception as e:
        print("An error occurred during route optimization:", e)

if __name__ == "__main__":
    main()
```

### Important Notes:
- **API Integration:** This example assumes access to an external traffic data service. You need to subscribe to a traffic data provider like Google Maps, HERE, TomTom, etc., and replace the placeholder API URLs and handling with actual endpoints.

- **Model Training:** The mock model here uses a simple linear regression trained on fictional data. In practice, you would train your model using comprehensive historical traffic data, including time of day, day of the week, etc.

- **Error Handling:** Error handling is basic in this example. In production, you'd want to log errors and handle different HTTP status codes appropriately.

- **Route Optimization:** The route optimization logic is highly simplified. Implementing actual routing and optimization (e.g., Travelling Salesman Problem solutions) requires more sophisticated algorithms and potentially additional libraries, such as `scipy` or `Google OR-Tools`.