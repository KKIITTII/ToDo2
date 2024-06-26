from django.shortcuts import render, redirect
import requests
from .models import City
from .form import CityForm
from django.views.decorators.csrf import csrf_protect
# Create your views here.

def index(request):
    
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID=ece2459e2a1e7517b7abcc691fb1311e" 
    message = None
    err_msg = None
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            number_of_city = City.objects.filter(name=new_city).count()
            if number_of_city == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = "City does not exist in the world!"
            else:
                err_msg = "City already exits in the database!"
                                      
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully'
            message_class = 'is-success'      

    form = CityForm()
    cities = City.objects.all()
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        weather_data.append(city_weather)
        
    if message:
        context = {"weather_data": weather_data, 
               'form': form, 
               'message': message, 
               'message_class': message_class}
    else:
        context = {"weather_data": weather_data, 
               'form': form}
        
    return render(request, 'weather/index.html',  context)


def delete_city(request, city_name):
    
    City.objects.filter(name=city_name).delete()
    return redirect('index_weather')
    