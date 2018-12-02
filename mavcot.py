from pymavlink import mavutil
import pycot, os, datetime

#Assert Mavlink 2
os.environ['mavlink20'] = "1"

mav = mavutil.mavlink_connection("udp:127.0.0.1:14550", retries=20)

print("Connecting, waiting for heartbeat")
mav.wait_heartbeat()
print("Connected, Waiting for fix")
mav.wait_gps_fix()
print("Fix acquired, running")

point = pycot.Point()
point.ce = 0.1
point.le = 0.1
event = pycot.Event()
event.version='0.1'
event.event_type = 'a-h-G-p-i'
event.uid = uuid.uuid4()
event.how="h-e"

while True:
	msg = mav.recv_match(type='GPS_RAW_INT')
	point.lat = msg.lat / 10000.0
	point.lon = msg.lon / 10000.0
	point.hae = msg.alt / 1000.0 - 8 
	event.point = point
	event.time = datetime.datetime.fromtimestamp(msg.time_usec / 1000.0)
	print(event.render(standalone=True, pretty=True))
