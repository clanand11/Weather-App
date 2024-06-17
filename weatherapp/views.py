from django.shortcuts import render
from django.http import HttpResponse
import requests
import datetime

def main(request):
    api='77228131ef7cfd13d5ff11f98069a5ba'
    curr_URL='https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    for_URL='https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'
    if request.method=="POST" :
        city=request.POST['city']
        city=city.lstrip()
        response=requests.get(curr_URL.format(city,api)).json()
        lat,lon=response['coord']['lat'],response['coord']['lon']
        forecast_response=requests.get(for_URL.format(lat,lon,api)).json()
        weatherData={
            'city':city.capitalize(),
            'temp':round(response['main']['temp'] - 273.15),
            'description':response['weather'][0]['description'].capitalize(),
            'icon':response['weather'][0]['icon'],
            'day':datetime.datetime.fromtimestamp(response['dt']),
        }

        future_forecast=[]
        day=datetime.datetime.fromtimestamp(forecast_response["list"][0]['dt']).strftime("%A")
        counter=0
        for data in forecast_response["list"]: 
            if day == datetime.datetime.fromtimestamp(data['dt']).strftime("%A"):
                print('skip {}{}' .format(day,datetime.datetime.fromtimestamp(data['dt']).strftime("%I:%M")))
                counter+=1
            else: 
                if datetime.datetime.fromtimestamp(data['dt']).strftime("%I:%M %p") in ["02:30 AM","05:30 AM","08:30 AM"]:
                    continue
                else:
                    future_forecast.append({
                    'day':datetime.datetime.fromtimestamp(data['dt']).strftime("%A"),
                    'temp':round(data['main']['temp'] - 273.15, 2),
                    'time':datetime.datetime.fromtimestamp(data['dt']).strftime("%I:%M %p"),
                    'description':data['weather'][0]['description'].capitalize(),
                    'icon':data['weather'][0]['icon'],
                    })
                    print(future_forecast)
                    counter+=1
                    break

        print(future_forecast[0]['day'])            
        print(counter)
        for data in forecast_response["list"][counter:]:
            day=datetime.datetime.fromtimestamp(data['dt'])
            if future_forecast[-1]['day'] == day.strftime("%A") or day.strftime("%I:%M %p") in ["02:30 AM","05:30 AM","08:30 AM"]:
                continue
            else:    
                future_forecast.append({
                    'day':datetime.datetime.fromtimestamp(data['dt']).strftime("%A"),
                    'temp':round(data['main']['temp'] - 273.15, 2),
                    'description':data['weather'][0]['description'].capitalize(),
                    # 'time':datetime.datetime.fromtimestamp(data['dt']).strftime("%I:%M %p"),
                    'icon':data['weather'][0]['icon'],
                    })
                
                


        context={
            'weather_data': weatherData,
            'forecast_data': future_forecast,
        }
        return render(request,'weatherapp/index.html',context)
    else:
        return render(request,'weatherapp/index.html')

# Create your views here.
