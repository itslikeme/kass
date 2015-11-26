#coding: UTF-8

import pyowm
API_KEY = '88bef2e2314e0affe5c32f6caf8a3a4d'
owm = pyowm.OWM(API_KEY)

observation = owm.weather_at_place('ASSIS,BR')
w = observation.get_weather()
l = observation.get_location()

class Forecast():
	def __init__(self, city_name, city_temp, city_status,city_pressure, city_sunrise,city_humidity,city_wind,city_time,city_lon,city_lat,city_ID,city_rain,city_sunset):
		self.name = city_name
		self.status = city_status
		self.pressure = city_pressure
		self.sunrise = city_sunrise
		self.humidity = city_humidity
		self.wind = city_wind
		self.time = city_time
		self.lon = city_lon
		self.lat = city_lat
		self.ID = city_ID
		self.rain = city_rain
		self.sunset = city_sunset

		def convertTemp(city_temp):
			for i in city_temp:
				if(i == 'temp'):
					self.temp = city_temp[i]
		convertTemp(city_temp)

		def display_info():
			print '\n____________________________________________\n'
			print 'Hora da consulta:  ' + str(self.time) + '\n'
			print 'Informacao metereologica da cidade "' + str(self.name) + '" :\n'
			print 'Nome: ' + str(self.name) + ' - ID: ' + str(self.ID)
			print 'Geolocation: Lat(' + str(self.lat) + ') Lon(' + str(self.lon) + ')' 
			print 'Temperatura: ' + str(self.temp) + ' Celsius'
			print 'Estado atual: ' + str(self.status)
			print 'Chuva: ' + str(self.rain)
			print 'Pressao Atmosferica: ' + str(self.pressure)
			print 'Humidade relativa do ar: ' + str(self.humidity)
			print 'Nascer do Sol: ' + str(self.sunrise)
			print 'Por do Sol: ' + str(self.sunset)
			print '\n____________________________________________\n'
		display_info()
		

weatherForecast = Forecast(l.get_name(),w.get_temperature(unit='celsius'),w.get_detailed_status(),w.get_pressure(),w.get_sunrise_time('iso'),w.get_humidity(), w.get_wind(),w.get_reference_time(timeformat='iso'),l.get_lon(),l.get_lat(),l.get_ID(),w.get_rain(),w.get_sunset_time('iso'))
