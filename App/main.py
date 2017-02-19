import json
import helper
import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.listview import ListItemButton
from kivy.factory import Factory
from kivy.uix.button import Button


class WeatherApp(App):
	pass

class WeatherRoot(BoxLayout):
	current_location = ObjectProperty()
	usergender = ObjectProperty()
	userunit = ObjectProperty()
	usergender = ObjectProperty()
	
	
	weather = ObjectProperty()
	
	
	
	def set_unit(self, checkbox, unit):
		if checkbox.active:
			self.userunit = unit
			print self.userunit
	
	def set_gender(self, checkbox, gender):
		if checkbox.active:
			self.usergender = gender
			print self.usergender
			
	def set_age(self, age):
		self.userage = age	
		

	def click_to_display(self):
		self.clear_widgets()
		display = Factory.Saved_Settings_Message()
		#display.location = self.current_weather
		self.add_widget(display)
		
		
	def Display_Weather(self):
		self.clear_widgets()
		
		if self.weather is None:
			self.weather = DisplayWeather()
			
		self.weather.update_weather()
		self.add_widget(self.weather)
		
	###display.temperature.bind(text=self.temperature)

	def define_location(self, location = None):
		if location is None and self.current_location is None:
			location = ("Sydney", "AU")
		if location is not None:
			self.current_location = location
	
		print self.current_location
		
		
	def click_ok(self, age):
		self.set_age(age)
		if self.userage is None or self.current_location is None or self.userunit is None or self.usergender is None:
			print "Something is Empty!"
		
		else:
			self.save_user_settings(self.current_location, self.userage, self.usergender, self.userunit)
			
	
	def save_user_settings(self, location, age, gender, unit):
		print location
		print gender
		print unit
		print age

		userdict = {}
		userdict['City'] = location[0]
		userdict['Country'] = location[1]
		userdict['Age'] = age
		userdict['Gender'] = gender
		userdict['Unit'] = unit

		print userdict
		userarray = json.dumps(userdict)

		userfile = open("usersettingJSON.txt", "w")
		userfile.write(userarray)
		
class DisplayWeather(BoxLayout):
	location = ListProperty(['Sydney', 'AU'])
	temperature = NumericProperty()
	temp_min = NumericProperty()
	temp_max = NumericProperty()
	humidity = NumericProperty()
	rain = ObjectProperty()
	wind = NumericProperty()	
	conditions = ObjectProperty()
	outfit = ObjectProperty()
		
		
	def update_weather(self): #get search location from usersettings file and send it to the openweather API
		userfile = open("usersettingJSON.txt", "r")
		read = userfile.read()
		info = json.loads(read)
		sendcity = (info["City"])
		sendcountry = (info["Country"])
		
		weather_template = "http://api.openweathermap.org/data/2.5/weather?q={},{}&units=metric"
		weather_url = weather_template.format(sendcity, sendcountry)
		request = UrlRequest(weather_url, self.weather_retrieved)
		
		
	def weather_retrieved(self, request, data):
		self.temperature = data['main']['temp']
		self.temp_min = (data['main']['temp_min'])
		self.temp_max = (data['main']['temp_max'])
		self.humidity = (data['main']['humidity'])
		self.rain = (data['weather']['main'])
		self.wind = (data['wind']['speed'])
	
		print self.temperature
		print self.temp_min
		print self.temp_max
		print self.humidity
		print self.rain
		print self.wind
		
	def retrieve_outfit(self, agebracket, temprange, gender, precipitation):
		sqlstatement = """SELECT code_snippet FROM Polyvore 
		JOIN Demographics ON Demographics.id_demographics=Polyvore.demographics_id
		JOIN Climate ON Climate.id_climate=Polyvore.climate_id
		WHERE Polyvore.demographics_id IN 
		(SELECT id_demographics FROM Age_Bracket 
		JOIN demographics ON demographics.age_bracket_id = Age_Bracket.id_age_bracket
		WHERE Age_Bracket.age_bracketcol = {} AND demographics.gender = {})
		AND Polyvore.climate_id IN(SELECT id_climate FROM Climate JOIN Temperature_Range ON Temperature_Range.id_temperature_range=Climate temperature_range_id JOIN Precipitation ON Precipitation.id_precipitation=Climate.precipitation_id WHERE Temperature_Range.temperature_range={} AND Precipitation.precipitation={})""".format(agebracket, gender, temprange, precipitation)	
		
		conn = sqlite3.connect('WeatherApp.db')
		cursor = conn.cursor()
		cursor.execute(sqlstatement)
		polyvore = cursor.fetchone()
		
		self.outfit = polyvore
		



class FindLocation(BoxLayout):
	city_input = ObjectProperty()
	results = ObjectProperty()

	def click_search(self):
		self.search_location()

	def search_location(self):
		search_template = "http://api.openweathermap.org/data/2.5/find?q={}&type=like"
		search_url = search_template.format(self.city_input.text)
		print search_url
		request = UrlRequest(search_url, self.found_location)
	

	def found_location(self, request, data):
		cities = [(d['name'],d['sys']['country'])for d in data['list']]  #stores as a list of tuples
		self.results.item_strings = cities
		del self.results.adapter.data[:]
		self.results.adapter.data.extend(cities)
		self.results._trigger_reset_populate()


	def args_converter(self, index, data_item): #takes item from list as an input and returns a dictionary
		city, country = data_item
		return {'location':(city, country)}


class LocationButton(ListItemButton):
	location = ListProperty()
	
		

		
#class DisplayWeather(BoxLayout):
	#location = ListProperty(['Sydney', 'AU'])
	#conditions = StringProperty()
	#current_weather = ObjectProperty()
	#temp = NumericProperty()
	#temp_min = NumericProperty()
	#temp_max = NumericProperty()

	#if location is not None:
		#self.current_weather = DisplayWeather(location=location)

	#def update_weather(self):
		#weather_template = "http://api.openweathermap.org.data/2.5/weather?q={},{}&units=metric"
		#weather_url = weather_template.format(*self.location)
		#request = UrlRequest(weather_url, self.weather_retrieved)

	#def weather_retrieved(self, request, data):
		#data = json.loads(data.decode())
		#self.conditions = data['main']['temp']
		#self.temp = data['main']['temp']
		#self.temp_min = data['main']['temp_min']
		#self.temp_max = data['main']['temp_max']

	#def show_current_weather(self, location=None):
		#self.clear_widgets()

		#if self.current_weather is None:
			#self.current_weather = CurrentWeather()
		#if location is not None:
			#self.current_weather.location = location

		#self.current_weather.update_weather
		#self.add_widget(self.current_weather)


	    


if __name__ == '__main__': 
	WeatherApp().run()