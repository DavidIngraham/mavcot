import geoid

geoid_height_table = geoid.GeoidHeight()

def get_geoid_height(lat, lon):
	geoid_height = 0
	try:
		geoid_height = geoid_height_table.get(lat, lon)
	except Exception as e:
		print(e)
	return geoid_height