from flet import *
import requests
import math
import folium
# INSTALL FOLIUM WITH PIP


def main(page:Page):
	page.scroll = "auto"

	you_now_location = TextField(label="Location now")
	cordinate_start = TextField(label="You lat and lot now")

	# DESTINATION CORDINATE LAT AND LONG
	destination_con = TextField(label="YOU ADDRESS DESTINATION")
	cordinate_con = TextField(label="insert cordinate destination")
	you_list_destination = []

	result_trip = Column()
	list_widget_destination = Column()

	# I CREATE CONTAINER FOR DESTINATION INPUT
	# LIKE ADDRESS DESTINATION AND LATITUDE AND LONGITUDE
	all_destination = Container(
		bgcolor="blue200",
		padding=10,
		content=Column([
			Text("insert destination ",weight="bold"),
			Column([
				destination_con,
				cordinate_con

				])

			])

		)

	def addyoudestination(e):
		cordinate_str = cordinate_con.value
		# CONVERT STRING TO FLOAT
		# FOR GET LATITUDE AND LONGITUDE
		lat_str,long_str = cordinate_str.split(",")
		lat = float(lat_str)
		long = float(long_str)
		cordinate = (lat,long)

		data = {
			"name":destination_con.value,
			"kordinat":cordinate

		}
		print(data)
		# PUSH TO you_list_destination
		you_list_destination.append(data)
		list_widget_destination.controls.append(
			ListTile(
				title=Text(destination_con.value),
				subtitle=Text(cordinate)

				)

			)
		# CLEAR INPUT
		destination_con.value = ""
		cordinate_con.value = ""
		page.update()

	def calculate_distance(lat1,lon1,lat2,lon2):
		# 6731 is RADIUS EARTH IN KM
		R = 6371
		dlat = math.radians(lat2 - lat1)
		dlon = math.radians(lon2 - lon1)
		a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
			* math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
		c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))	
		d = R * c
		return d	





	def processnow(e):
		for location in you_list_destination:
			# AND REQUEST TO API
			api_url = f"https://nominatim.openstreetmap.org/search?q={location['name']}&format=json"
			response = requests.get(api_url).json()
			if response:
				lat = float(response[0]['lat'])
				lon = float(response[0]['lon'])
				location['kordinat'] = (lat,lon)
				location['address'] = response[0]['display_name']
			else:
				location['address'] = location['name']

		# NOW CONVERT FROM STRING TO FLOAT
		mylat_start,mylong_start = map(float,cordinate_start.value.split(","))

		# AND NOW SORT TO NEAR YOU LOCATION
		you_list_destination.sort(key=lambda x:calculate_distance(mylat_start,mylong_start,x['kordinat'][0],x['kordinat'][1]))

		myloc = tuple(map(float,cordinate_start.value.split(", ")))

		you_map = folium.Map(location=myloc,zoom_start=12)

		# NOW CREATE MARKER
		# FROM YOU LOCATION NOW 
		folium.Marker(location=myloc,popup="YOu Here",icon=folium.Icon(color="blue")).add_to(you_map)

		# AND NOW SHOW THE RESULT TO WIDGET 
		for i,lokasi in enumerate(you_list_destination):
			result_trip.controls.append(
				Container(
					bgcolor="yellow200",
					padding=10,
					content=Column([
					Text(f"{i+1}. {lokasi['address']}"),
				Text(f"latitude : {lokasi['kordinat'][0]} , Longitude : {lokasi['kordinat'][1]}"),
				Text(f"distance from start : {calculate_distance(mylat_start,mylong_start,lokasi['kordinat'][0],lokasi['kordinat'][1])} ")




						])
					)
				)
			try:
				cordinate_value = tuple(map(float,lokasi['kordinat']))
			except ValueError:
				# SET TO 0
				cordinate_value = (0,0)

			# AND NOW CREATE LINE BETWEEN LOCATION
			# AND CREATE MARKER DESTINATION YOU
			folium.PolyLine(locations=[(mylat_start,mylong_start),lokasi['kordinat']],color="blue",weight=2.5,opacity=0.7).add_to(you_map)
	
			# AND CREATE MARKER
			folium.Marker(location=lokasi['kordinat'],tooltip=lokasi['address'],icon=folium.Icon(color="red")).add_to(you_map)


		# AND SAVE YOU MAPS TO HTML FILE
		you_map.save("You maps.html")
		page.update()		



	page.add(
	AppBar(
	title=Text("Flet sorting locations",

		color="white",weight="bold"
		),
	bgcolor="blue"
	),
	Column([
		you_now_location,
		cordinate_start,
		all_destination,
	ElevatedButton("add destination",
		bgcolor="blue",color="white",
		on_click=addyoudestination
		),
	list_widget_destination,
	ElevatedButton("Process now",
		bgcolor="green",color="white",
		on_click=processnow
		),
	Text("result after locations sorted bt proximity",
		weight="bold"
		),
	result_trip

		])

	)

flet.app(target=main)
