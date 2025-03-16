import streamlit as st
import requests
from PIL import Image
import io

# Function to get weather forecast data
def get_weather_forecast(city_name, API_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_key}&units=metric"
    
    try:
        # Send a GET request to OpenWeatherMap API
        response = requests.get(url)
        
        # If the request was successful (HTTP status code 200)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            # If the status code is not 200, raise an exception
            st.error(f"Error: Unable to fetch weather forecast for {city_name}. Please check the city name or try again later.")
            return None
    except requests.exceptions.RequestException as e:
        # If an exception occurs during the request, display an error message
        st.error(f"Error: Could not retrieve data. {e}")
        return None

# Streamlit UI setup
st.set_page_config(
    page_title="Weather Forecast Information", 
    page_icon="⛅", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Custom CSS styling for the background, text colors, and spinner
st.markdown("""
    <style>
        body {
            background-color: #f0f8ff;  # Light sky blue for readability
            color: #ffffff;  # White text color (permanent)
        }
        .stButton>button {
            background-color: #4CAF50;  # Green color for the button
            color: white;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #45a049;  # Darker green on hover
        }
        .stTextInput>div>div>input {
            border-radius: 10px;  # Rounded input field
            padding: 12px;
            font-size: 18px;
            width: 100%;
        }
        .stTextInput>div>div>input:focus {
            border: 2px solid #4CAF50;  # Green border on focus
        }
        .stTitle {
            font-size: 36px;
            color: #ffffff;
            text-align: center;
        }
        .stSubheader {
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
        }
        .stApp {
            background-image: url("https://static.vecteezy.com/system/resources/thumbnails/023/133/298/small/dark-blue-texture-with-cloudy-sky-vector.jpg");  /* Lighter sky image */
            background-size: cover;
            background-position: center;
            background-attachment: fixed; /* Make the background image permanent */
        }
    </style>
""", unsafe_allow_html=True)

# Title for the app
st.title("Weather Forecast App ⛅")

# Subtitle for instructions
st.subheader("Enter the name of the city to get the 5-day weather forecast:")

# User input for city name
city_name = st.text_input("City Name")

# Your OpenWeatherMap API key
API_key = "d2b518e1b88f8c8a30469bee4caacbe7"

# Check if user has entered a city
if city_name:
    with st.spinner('Fetching weather forecast data...'):
        # Get the weather forecast data
        weather_data = get_weather_forecast(city_name, API_key)
    
        # If weather data is successfully fetched, display the forecast
        if weather_data:
            # Weather details
            st.markdown(f"### Weather Forecast for **{city_name}**:")
            for entry in weather_data['list']:
                dt_txt = entry['dt_txt']
                temp = entry['main']['temp']
                feels_like = entry['main']['feels_like']
                weather_description = entry['weather'][0]['description']
                wind_speed = entry['wind']['speed']
                wind_deg = entry['wind']['deg']
                humidity = entry['main']['humidity']
                
                # Display forecast information for each entry (every 3 hours)
                st.write(f"**Date/Time:** {dt_txt}")
                st.write(f"**Temperature:** {temp}°C (Feels like: {feels_like}°C)")
                st.write(f"**Weather:** {weather_description.capitalize()}")
                st.write(f"**Wind Speed:** {wind_speed} m/s (Direction: {wind_deg}°)")
                st.write(f"**Humidity:** {humidity}%")
                st.markdown("---")
            
# Error handling for empty input (if the user doesn't enter a city)
else:
    st.warning("Please enter a city name to get the weather forecast.")
