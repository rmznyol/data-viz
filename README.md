# Interactive U.S. Weather Description
The Erdos Institute Spring 2023 Project

## Description

### This is a dashboard which displays information about weather in cities across the continental US. 

The weather data is displayed graphically as follows. Each city has an arrow emanating from it. The direction of the arrow on the map corresponds to the wind direction, and its size represents the wind speed. The color of the arrow corresponds to the temperature, according to the colorbar on the right.

### There are five levels of interface:
#### 1. The calendar tool
The user selects the date to focus on, using a calendar tool. The allowed dates are between 11/01/2012 and 10/31/2017.
#### 2. Radio items to select timeframe
The options allow the user to view weather data for each hour of the day or daily averages over a span of 31 days.
#### 3. Slider to select what to view
If the timeframe is "per hour," the user can select which hour of the day to view. All hours are in Eastern time. If the timeframe is "daily average," the user can select the day up to 15 days before or 15 days after.
### 4. Graph interaction
The user can pan or zoom to better see the graphical information. While it is possible to pan away from the continental US, there is no weather information elsewhere.
### 5. Hover for detailed information
The user can hover over a city and view its name and the exact temperature, weather description, and wind speed. It also displays an image corresponding to the weather description.

## Dashboard URL
https://weather-description.onrender.com

## Running on local server

- Clone the repository and run !pip install -r requirements.txt
- Open data_viz_dashboard.ipynb and run
- View in a local server

## Contributors

- Christian Cofoid
- Daniel Freese
- Ramazan Yol
