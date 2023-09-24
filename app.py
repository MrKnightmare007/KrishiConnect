import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template
import os
import joblib
import requests
from datetime import datetime,timedelta

def get_future_dates(start_date, num_days):
    dates = []
    for day in range(num_days):
        date = start_date + timedelta(days=day)
        dates.append(date.strftime("%Y-%m-%d"))
    return dates

url = "https://api.tomorrow.io/v4/weather/forecast?location=kolkata&timesteps=daily&apikey=NWbU1ceSDImxoVp6CmKLzUrXScmgL1c2"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)
data = response.json()  # Parse the JSON response

# Extract the daily forecast data for 5 days
daily_forecast = data['timelines']['daily'][:5]

# Initialize lists to store extracted data
temperature_data = []
humidity_data = []
pressure_data = []
windspeed_data = []
rain_data = []

# Extract data for each day
for day_data in daily_forecast:
    temperature = day_data['values']['temperatureAvg']
    humidity = day_data['values']['humidityAvg']
    pressure = day_data['values']['pressureSurfaceLevelAvg']
    windspeed = day_data['values']['windSpeedAvg']
    rain = day_data['values']['rainAccumulationAvg']
    
    temperature_data.append(temperature)
    humidity_data.append(humidity)
    pressure_data.append(pressure)
    windspeed_data.append(windspeed)
    rain_data.append(rain)

# Load the soil moisture prediction model
model = joblib.load('soil_moisture_model.pkl')

# Create a list of input values and reshape it to match the model's input format
input_data = []
for day in range(5):
    input_data.append([temperature_data[day], humidity_data[day], pressure_data[day]/10, windspeed_data[day], rain_data[day]])

# Make predictions for the next 5 days
soil_moisture_predictions = model.predict(input_data)

# Synthetic data for the previous 5 days (you can replace this with actual data)
synthetic_data = [0.60, 0.50, 0.55, 0.69, 0.75]

# Combine the previous and next 5 days of soil moisture data
soil_moisture_data = synthetic_data + list(soil_moisture_predictions)

# Get future dates
current_date = datetime.now()
future_dates = get_future_dates(current_date, 5)
past_dates = get_future_dates(current_date - timedelta(days=5), 5)

# Plot soil moisture data with different colors and labels
plt.plot(past_dates, synthetic_data, label='Previous 5 Days', color='blue', marker='o')
plt.plot(future_dates, soil_moisture_predictions, label='Next 5 Days', color='green', marker='o')

# Rotate x-axis labels for better visibility
plt.xticks(rotation=45)

# Add labels and legend
plt.xlabel('Date')
plt.ylabel('Soil Moisture Prediction')
plt.legend()
plt.title('Predicted Soil Moisture Data')
plt.grid(True)

# Show the plot
plt.tight_layout()
# plt.show()
plt.savefig(os.path.join('static', 'images', 'plot.png'))
plt.close('all')

x1 = np.array([0, 1, 2, 3, 4])  # Use day indices as x-axis values
y1 = np.array(rain_data)

# Set tick labels for the x-axis
x_labels = [day_data['time'][:10] for day_data in daily_forecast]
plt.xticks(x1, x_labels, rotation=45)

subArray = [rain_data[0], rain_data[4]]
ids1 = np.nonzero(np.in1d(y1, subArray))[0]

plt.plot(x1, y1)
plt.plot(x1[ids1], y1[ids1], 'bo')

plt.xlabel('Date')
plt.ylabel('Rain Accumulation (Avg)')
plt.title('Predicted Rain Data')
plt.grid(True)

# Adjust the margins to ensure the entire plot is visible
plt.subplots_adjust(bottom=0.2)
# Save the figure in the static directory
plt.savefig(os.path.join('static', 'images', 'plot2.png'))
print("plot generated!")

app = Flask(__name__)
esp_url = "http://192.168.234.93"
# Function to fetch temperature data
def fetch_temperature():
    try:
        response = requests.get(f'{esp_url}/temperature')
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Error fetching temperature data: {e}")
    return "N/A"  # Return a default value if data cannot be fetched

def fetch_humidity():
    try:
        response = requests.get(f'{esp_url}/humidity')
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Error fetching temperature data: {e}")
    return "N/A"  # Return a default value if data cannot be fetched

def fetch_ldr():
    try:
        response = requests.get(f'{esp_url}/ldr')
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Error fetching temperature data: {e}")
    return "N/A"  # Return a default value if data cannot be fetched

def fetch_soil():
    try:
        response = requests.get(f'{esp_url}/soil-mois')
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Error fetching temperature data: {e}")
    return "N/A"  # Return a default value if data cannot be fetched

def fetch_rain():
    try:
        response = requests.get(f'{esp_url}/rain')
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Error fetching temperature data: {e}")
    return "N/A"  # Return a default value if data cannot be fetched

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ldr')
def ldr():
    ldr= fetch_ldr()
    return ldr

@app.route('/temp')
def temp():
    temp = fetch_temperature()
    return temp

@app.route('/humidity')
def hum():
    hum = fetch_humidity()
    return hum

@app.route('/soil')
def soil():
    soil = fetch_soil()
    return soil

@app.route('/rain')
def rain():
    rain = fetch_rain()
    return rain

@app.route('/index1')
def index1():
    return render_template('index1.html')

@app.route('/index4')
def index4():
    return render_template('index4.html')

@app.route('/chart_soilms')
def single_converter():
    soilms_data = [round(i, 3) for i in soil_moisture_predictions]
    return render_template('chart.html', no=future_dates)


if __name__ == '__main__':
    app.run(debug=True)