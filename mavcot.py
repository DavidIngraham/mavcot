from pymavlink import mavutil
from mavcot import helpers
import pycot, os, time, datetime, socket


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

point = pycot.Point()
point.ce = 1.0
point.le = 1.0
event = pycot.Event()
event.version='2.0'
event.event_type = 'a-f-A-M-F-Q'

event.uid = "Cobalt008" 
event.how="m-g"

last_sent_time = time.time()

while True:
	msg = mav.recv_match(type='GLOBAL_POSITION_INT')
	if msg is not None and ((time.time() - last_sent_time) > 1):
		#print(msg)
		point.lat = msg.lat / 10000000.0
		point.lon = msg.lon / 10000000.0
		alt_msl = msg.alt / 1000.0 
		point.hae = alt_msl + helpers.get_geoid_height(point.lat,point.lon)
		event.point = point
		event.time = datetime.datetime.fromtimestamp(time.time())
		event_xml = event.render(standalone=True)
		print(event_xml)
		try:
			s.sendto(event_xml, address)
			last_sent_time = time.time()
		except Exception as e:
			print('COT Socket Error:', e)
			time.sleep(1) # Never run faster than 1 Hz when the TCP connection is closed
