from pymavlink import mavutil
from mavcot import helpers
import xml.etree.ElementTree as ET
import os, time, datetime, socket


# Configure Socket Connection
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
address = ('10.0.64.10', 9190)

# Assert Mavlink 2
os.environ['mavlink20'] = "1"


print("Waiting for MAVLink Socket")
mav = mavutil.mavlink_connection("udp:127.0.0.1:14550", retries=20)

print("UDP Listening, waiting for heartbeat")
mav.wait_heartbeat()
print("Connected, Waiting for fix")
mav.wait_gps_fix()
print("Fix acquired, running")

last_sent_time = time.time()

while True:
	msg = mav.recv_match(type='GLOBAL_POSITION_INT')
	if msg is not None and ((time.time() - last_sent_time) > 1):
		lat = msg.lat / 10000000.0
		lon = msg.lon / 10000000.0
		alt_msl = msg.alt / 1000.0 
		hae = alt_msl + helpers.get_geoid_height(lat,lon)
		timestamp = datetime.datetime.fromtimestamp(time.time())
		timestamp_string = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%FZ')

		cot_event_element = ET.Element('event')
		cot_event_element.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
		cot_event_element.set('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
		cot_event_element.set('uid', 'COBALT_UAV')
		cot_event_element.set('type', 'a-f-A-M-F-Q')
		cot_event_element.set('time', timestamp_string)
		cot_event_element.set('start', timestamp_string)
		cot_event_element.set('stale', timestamp_string)

		cot_point_element = ET.SubElement(cot_event_element, 'point')
		cot_point_element.set('lat', str(lat))
		cot_point_element.set('lon', str(lon))
		cot_point_element.set('hae', str(hae))

		event_xml_string = ET.tostring(cot_event_element)
		header_string = '<?xml version="1.0" standalone="yes"?>'
		out_cot_xml = header_string + event_xml_string
		print(out_cot_xml)
		try:
			s.sendto(out_cot_xml, address)
			last_sent_time = time.time()
		except Exception as e:
			print('COT Socket Error:', e)
			time.sleep(1) # Never run faster than 1 Hz when the TCP connection is closed
