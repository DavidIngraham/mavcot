# MAVCOT
Publishes Cursor on Target events from a MAVLINK feed via UDP

Install:
```
git clone https://github.com/DavidIngraham/mavcot.git
cd mavcot
pip install .
```

Usage (with optional path to config file):
```
mavcot_proxy.py /path/to/mavcot.conf
```

Configuration Example:
```
# mavcot_cobalt.conf
[mavlink]
address: 127.0.0.1
port: 14550

[cot]
address: 10.0.64.10
port: 9190
output_rate_hz: 1
uid: UAV_005
type: a-f-A-M-F-Q
```
