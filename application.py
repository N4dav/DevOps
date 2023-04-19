from flask import Flask, render_template, request, redirect, send_file
import requests
import os
from botocore.config import Config
import datetime
import json
import logging
import boto3
from prometheus_flask_exporter import PrometheusMetrics



logging.basicConfig(level=logging.DEBUG)
application = Flask(__name__)
metrics = PrometheusMetrics(application)


my_city=''
an_json={}
bg_color = os.environ.get('BG_COLOR', 'silver')
aws_region = Config(
    region_name = 'eu-central-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)
@application.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        try:
            global my_city
            my_city = userInput()
            #print("City inputted")
            city_details = cityGeo(my_city)
            #print("City translated to geo loc")
            geo_loc = city_details[0]
            my_country = city_details[1]
            geo_api = geoApi((geo_loc),my_city)
            #print("Weather gathered for loc")
            global an_json
            an_json = analyzeJson(geo_api)
            #print("Data analyzed succesfully")
            application.logger.info("Info logs")
            return render_template("index.html", an_json= an_json, city=my_city, country=my_country, bg_color=bg_color)
        except(Exception):
            application.logger.error("Error logs")
            print(f"Request Error! Try Again {Exception}")
            return redirect("/")
    return render_template("index.html", bg_color=bg_color)

def userInput():
    ''' Get User input from the form in the field "city" '''
    if request.method == 'POST':
        city_input = request.form["City"]
        return city_input

def cityGeo(city):
    ''' Get from JSON raw data the country and the Geo location '''
    app_id= '93c8227801e25c807c9e5c3e839b0273'
    raw = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city},&appid={app_id}')
    raw2 = raw.json()
    raw3 = raw2[0]
    lat = raw3.get('lat')
    lon = raw3.get('lon')
    country = raw3.get('country')
    geo_list = [lat, lon]
    return [geo_list, country]

def geoApi(geo_list, city):
    ''' Send Geo Location to the API for 7 days forecast '''
    app_id = '8afde337'
    app_key = '54cfb1cc2d416faa9ba79e54a60818e4'
    lat = geo_list[0]
    lon = geo_list[1]
    weather_data = requests.get(f'http://api.weatherunlocked.com/api/forecast/{lat},{lon}?app_id={app_id}&app_key={app_key}')
    weather = weather_data.json()
    today = datetime.date.today()
    # Create the directory for history of queries if it doesn't exist
    # with open(f'forecasts_history/{city}_{today}', "w") as f:
    #     json.dump(weather, f)
    return weather


def analyzeJson(weather):
    ''' Analyze JSON and get only dates, max_temp and min_temp '''
    data = weather['Days']

    max_list = []  # Will contain 7 elements of max tempr for each day
    min_list = []  # Will contain 7 elements of min tempr for each day
    date_list = [] # Will contain 7 elements of the date of each day

    for h in range(0,7):
        temp = data[h].get('temp_max_c')
        max_list.append(temp)

    for l in range(0,7):
        temp = data[l].get('temp_min_c')
        min_list.append(temp)

    for d in range(0,7):
        temp = data[d].get('date')
        date_list.append(temp)

    end_tmpr = []   # each element will contain both min and max tempr
    for mx in max_list:
        for mn in min_list:
            end_tmpr.append(f"{mn}~{mx}")

    tmpr_dict = dict(zip(date_list,end_tmpr))    # Keys are the dates, Values are the min-max tempr

    return tmpr_dict

'''
Adding button to download img
from aws S3 bucket
'''
@application.route('/s3', methods=["GET"])
def imgDown():
    client = boto3.client(('s3'))
    bucket = 'nadav.ops'
    current_path = os.getcwd()
    file = 'Sky_img'
    filename = os.path.join(current_path, 'downloads', file)
    client.download_file(
        Bucket=bucket,
        Key=file,
        Filename=filename
    )

'''
Added button to save viewed data
in AWS DynamoDB table
'''
@application.route('/db', methods=["GET"])
def weatherView():
    db_client = boto3.resource('dynamodb')
    table = db_client.Table('weather_view')
    for date in an_json.keys():
        table.put_item(
            Item={
                'City': my_city,
                'Date': date,
                'Min~Max Temp.': an_json[date]
            }
        )
    return redirect("/")

@application.route('/history', methods=["GET"])
def list_files():
  # Get the list of files in the directory
  directory = './forecasts_history'
  files = os.listdir(directory)
  # Render the template and pass the list of files as a variable
  return render_template('history.html', files=files)

@application.route('/download/<file>')
def download_file(file):
    return send_file(f'forecasts_history/{file}', as_attachment=True)


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=9090, debug=True)



