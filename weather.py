from flask import Flask, render_template, request

import os

# import json to load JSON data to a python dictionary
import json

# urllib.request to make a request to api
import urllib.request

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def weather():
    if request.method == 'POST':
        city = request.form['city']
    else:
        city = 'san francisco'

    city = city.replace(" ", "+")
    api = os.getenv('WEATHER_API_KEY')

    #source contains json data from api
    try:
        source = urllib.request.urlopen(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}')
        source = source.read().decode('utf-8')
    except:
         return render_template('index.html', data = {"city": city})   
    else:
        #converting JSON data to a dictionary
        list_of_data = json.loads(source)

        #convert temperature from Kelvin to Farenheit
        tmp = float(list_of_data['main']['temp'])
        temp =  (tmp - 273.15) * 9 / 5 + 32 
        fm_temp = '{:6.2f}'.format(temp)

        data = { "country_code": str(list_of_data['sys']['country']), 
            "city_code": str(list_of_data['name']),
            "coordinate": str(list_of_data['coord']['lon']) + ' ' 
                        + str(list_of_data['coord']['lat']), 
            "temp": str(fm_temp) + 'F', 
            "pressure": str(list_of_data['main']['pressure']), 
            "humidity": str(list_of_data['main']['humidity']), 
        } 
        return render_template('index.html', data = data)

if __name__ == '__main__':
    app.run(debug = True)    