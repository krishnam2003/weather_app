# You have to run these given dependencies on your folder terminal before running this code otherwise your code will not be executed.
# pip install requests
# pip install geocoder
# pip install pillow
# pip install ttkbootstrap
# python -m tkinter

# tkinter : This is an interface to the tk GUI toolkit that ships with Python.



# API_KEY = "d32068adcaa147741e4e8845d8e11840"


import tkinter as tk
from tkinter import messagebox,Toplevel
from tkinter import ttk  # Import ttk for styling
import requests
from PIL import Image, ImageTk
import geocoder  # For getting current location
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import threading

# Replace with your OpenWeatherMap API key
API_KEY = "d32068adcaa147741e4e8845d8e11840"


# Mapping of weather conditions to background colors
WEATHER_BACKGROUND_MAP = {
    "clear": "#87CEEB",  # Light blue for clear sky
    "clouds": "#B0C4DE",  # Light gray for cloudy sky
    "rain": "#778899",  # Gray for rainy weather
    "thunderstorm": "#2F4F4F",  # Dark gray for thunderstorms
    "snow": "#FFFFFF",  # White for snowy weather
    "mist": "#F5F5F5",  # Light gray for mist
    "haze": "#E0D7C6",  # Beige for haze
    "fog": "#C0C0C0",  # Light gray for fog
}

def update_background(description):
    """Update the background color based on weather description."""
    for key, color in WEATHER_BACKGROUND_MAP.items():
        if key in description.lower():
            root.config(bg=color)  # Update the main window's background
            return
    # Default background if no match is found
    root.config(bg="#ADD8E6")  # Default light blue

# Update the main get_weather function to include air quality
def get_weather(city_name):
    if city_name == "":
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    # URL for current weather API endpoint
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"

    # Make a GET request to the API
    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()

        # Extract weather information
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']

        city = data['name']
        temperature = main['temp']
        humidity = main['humidity']
        description = weather['description']
        wind_speed = wind['speed']
        wind_speed1 = wind_speed * 3.6
        icon_code = weather['icon']  # Weather icon code

        # Update the labels with weather information
        temperature_label.config(text=f"Temperature: {temperature}°C")
        humidity_label.config(text=f"Humidity: {humidity}%")
        description_label.config(text=f"Weather: {description.capitalize()}")
        wind_speed_label.config(text=f"Wind Speed: {wind_speed1:.1f} km/h")
        
        
        # Update the background based on weather description
        update_background(description)

        # Display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
        icon_response = requests.get(icon_url, stream=True)
        if icon_response.status_code == 200:
            img = Image.open(icon_response.raw)
            img = img.resize((100, 80))  # Resize the icon
            icon_photo = ImageTk.PhotoImage(img)
            icon_label.config(image=icon_photo)
            icon_label.image = icon_photo

        # Call the function to get air quality
        get_air_quality(city)

        # Call the function to get the forecast
        get_forecast(city)
    else:
        messagebox.showerror("Error", "City not found or invalid API key!")


# Function to get 5-day weather forecast
def get_forecast(city_name):
    # 5-day forecast endpoint
    base_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric"

    response = requests.get(base_url)

    if response.status_code == 200:
        data = response.json()

        forecast_output.delete(1.0, tk.END)  # Clear the previous forecast
        forecast_output.insert(tk.END, f"Weather forecast for {city_name}:\n\n")

        # Loop through the 5-day forecast
        for item in data['list']:
            time = item['dt_txt']
            temp = item['main']['temp']
            description = item['weather'][0]['description']
            icon_code = item['weather'][0]['icon']  # Icon for each forecast

            # Display each forecast item
            forecast_output.insert(tk.END, f"{time}: {temp}°C, {description.capitalize()}\n")
            # Fetch and display the forecast icon
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
            icon_response = requests.get(icon_url, stream=True)
            if icon_response.status_code == 200:
                img = Image.open(icon_response.raw)
                img = img.resize((30, 30))  # Resize the icon for forecast
                icon_photo = ImageTk.PhotoImage(img)
                forecast_output.image_create(tk.END, image=icon_photo)
                forecast_output.insert(tk.END, "  ")  # Add some space after the icon

    else:
        forecast_output.insert(tk.END, "Error: City not found or invalid API key!\n")

# Function to get weather for current location
def get_location_weather():
    g = geocoder.ip('me')  # Get the current location (IP based)
    latitude = g.latlng[0]
    longitude = g.latlng[1]

    # Use latitude and longitude for the weather request
    base_url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric"
    
    response = requests.get(base_url)
    
    if response.status_code == 200:
        data = response.json()

        # Extract weather information
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']

        city = data['name']
        temperature = main['temp']
        humidity = main['humidity']
        description = weather['description']
        wind_speed = wind['speed']
        wind_speed1 = wind_speed * 3.6
        icon_code = weather['icon']  # Weather icon code

        # Update the labels with weather information
        temperature_label.config(text=f"Temperature: {temperature}°C")
        humidity_label.config(text=f"Humidity: {humidity}%")
        description_label.config(text=f"Weather: {description.capitalize()}")
        wind_speed_label.config(text=f"Wind Speed: {wind_speed1} m/s")

        # Display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
        icon_response = requests.get(icon_url, stream=True)
        if icon_response.status_code == 200:
            img = Image.open(icon_response.raw)
            img = img.resize((50, 50))  # Resize the icon
            icon_photo = ImageTk.PhotoImage(img)
            icon_label.config(image=icon_photo)
            icon_label.image = icon_photo
            
        # Update the background based on weather description
        update_background(description)
            
        # # Call the function to get air quality
        # get_air_quality(city)

        # # Call the function to get the forecast
        # get_forecast(city)
        
        # Call the function to get air quality and forecast in a separate thread
        threading.Thread(target=get_air_quality, args=(city,)).start()
        threading.Thread(target=get_forecast, args=(city,)).start()
        
    else:
        messagebox.showerror("Error", "Unable to fetch weather for your location!")
        
        # Function to get air quality based on city
def get_air_quality(city_name):
    # Get coordinates (latitude and longitude) for the city using the OpenWeatherMap Weather API
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
    weather_response = requests.get(weather_url)

    if weather_response.status_code == 200:
        data = weather_response.json()
        latitude = data['coord']['lat']
        longitude = data['coord']['lon']

        # URL for air quality API endpoint using coordinates
        air_quality_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={API_KEY}"
        air_quality_response = requests.get(air_quality_url)

        if air_quality_response.status_code == 200:
            air_data = air_quality_response.json()

            # Extract air quality data
            air_quality = air_data['list'][0]['main']['aqi']  # Air quality index (AQI)

            # Map AQI values to categories and colors
            air_quality_mapping = {
                # 1: ("Good", "#4CAF50", "good.png"),
                # 2: ("Fair", "#FFC107", "fair.png"),
                # 3: ("Moderate", "#FF9800", "moderate.png"),
                # 4: ("Poor", "#F44336", "poor.png"),
                # 5: ("Very Poor", "#9C27B0", "very_poor.png"),
                1: ("Good", "#4CAF50","good.png"),
                2: ("Moderate", "#FFEB3B","moderate.png"),
                3: ("Unhealthy for Sensitive Groups", "#FF9800","Unhealthy_for_Sensitive_Groups.png"),
                4: ("Unhealthy", "#F44336","Unhealthy.png"),
                5: ("Very Unhealthy", "#9C27B0","Very_Unhealthy.png"),
                6: ("Hazardous", "#7E0023","Hazardous.png"),
            }
            category, color, icon_file = air_quality_mapping.get(air_quality, ("Unknown", "#9E9E9E", None))

            # Display the air quality information
            air_quality_label.config(text=f"Air Quality: {category}", bg=color)

            # Display air quality icon if available
            if icon_file:
                try:
                    icon = Image.open(icon_file)
                    icon = icon.resize((100, 100))  # Resize the icon
                    icon_photo = ImageTk.PhotoImage(icon)
                    air_quality_icon_label.config(image=icon_photo)
                    air_quality_icon_label.image = icon_photo  # Keep a reference to avoid garbage collection
                except FileNotFoundError:
                    air_quality_icon_label.config(image='', text="Icon Missing", bg=color)
        else:
            air_quality_label.config(text="Error fetching air quality data.", bg="#F44336")
    else:
        air_quality_label.config(text="Error: City not found or invalid API key!", bg="#F44336")

        
# Create the main window
root = tk.Tk()
root.title("Weather App")

# Set the window size and make it responsive
root.geometry("600x550")
root.resizable(True, True)

# Apply ttkbootstrap theme
style = Style(theme="litera")  # Choose a theme: litera, darkly, etc.

# Set background color
root.config(bg="#90EE90")



# Add labels and input fields with styling
city_label = tk.Label(root, text="Enter city name:", font=("Helvetica", 14), bg="#e0f7fa")
city_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

city_entry = tk.Entry(root, font=("Helvetica", 14), width=30)
city_entry.grid(row=0, column=3, padx=10, pady=10)

# Search button with color change on hover
def on_enter(e):
    search_button.config(bg="#4CAF50")
   

def on_leave(e):
    search_button.config(bg="#3e8e41")
      
   
# refresh button with color change on hover 
def on_ente(e):
    refresh_button.config(bg="#673AB7")

def on_leav(e):
    refresh_button.config(bg="#607D8B")
    
   
# location button with color change on hover 
def on_enter1(e):
    location_button.config(bg="#F44336")  
def on_leave1(e):
    location_button.config(bg="#8E24AA")   

search_button = ttk.Button(root, text="Get Weather",style="success.TButton",  command=lambda: get_weather(city_entry.get()))
search_button.grid(row=1, column=2, columnspan=2, pady=10)
# search_button.bind("<Enter>", on_enter)
# search_button.bind("<Leave>", on_leave)

style.configure(
    "success.TButton", 
    font=("Helvetica", 14), 
    borderwidth=2
)
style.map(
    "success.TButton", 
    focuscolor=[("active", "#4CAF50")], 
    bordercolor=[("active", "#4CAF50")]
)


# Add refresh button
refresh_button = ttk.Button(root, text="Refresh Weather", command=lambda: get_weather(city_entry.get()))
refresh_button.grid(row=2, column=2, columnspan=2, pady=10)
# refresh_button.bind("<Enter>", on_ente)
# refresh_button.bind("<Leave>", on_leav)

# Add button to get weather for current location
location_button = ttk.Button(root, text="Use My Location",style="info.TButton",  command=get_location_weather)
location_button.grid(row=3, column=2, columnspan=2, pady=10)
# location_button.bind("<Enter>", on_enter1)
# location_button.bind("<Enter>", on_leave1)

# Labels to display the weather data
temperature_label = tk.Label(root, text="Temperature: ", font=("Arial", 14), bg="#e0f7fa")
temperature_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

humidity_label = tk.Label(root, text="Humidity: ", font=("Arial", 14), bg="#e0f7fa")
humidity_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

description_label = tk.Label(root, text="Weather: ", font=("Arial", 14), bg="#e0f7fa")
description_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")

wind_speed_label = tk.Label(root, text="Wind Speed: ", font=("Arial", 14), bg="#e0f7fa")
wind_speed_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")

# Air quality info
air_quality_label = tk.Label(root, text="Air Quality: --", font=("Arial", 14), bg="#e0f7fa")
air_quality_label.grid(row=8, column=0,columnspan=2,  padx=10, pady=5, sticky="w")

# Air quality icon label
air_quality_icon_label = tk.Label(root, bg="#e0f7fa")
air_quality_icon_label.grid(row=8, column=2, padx=10, pady=5)



# Add the weather icon label
icon_label = tk.Label(root, bg="#e0f7fa")
icon_label.grid(row=4, column=2, padx=10, pady=10)

# Text widget to display the forecast data
forecast_label = tk.Label(root, text="5-Day Forecast:", font=("Helvetica", 14), bg="#e0f7fa")
forecast_label.grid(row=9, column=0, columnspan=2, pady=10)

forecast_output = tk.Text(root, height=10, width=60, font=("Helvetica", 12))
forecast_output.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

# Run the Tkinter event loop
root.mainloop()

