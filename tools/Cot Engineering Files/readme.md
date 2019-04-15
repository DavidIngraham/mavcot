From PS:
I have attached a utility script, gtp, and some associated files we use when debugging and testing CoT problems on our system. We run these on our linux development stations. The script gtp copies cot_pos_base.xml to cot_node_pos.xml. It then edits fields in file cot_node_pos.xml and sends it to the radio.

The very last line in the gtp script, ./send_cot_packets.pl 172.26.1.1 9190 ./cot_node_pos.xml, sends the CoT message to our system. I believe this information will help our customer get up and running quickly.

Our code only parses the following fields: uid, type, time, start, stale, point, lat, lon, hae,
if detail is present then we check for track. If track is present, we look for speed, and course are parsed.

One of our developers is looking at why the message the customer sent is crashing the visualization process. This should not happen. We opened an internal ticket and will fix that problem.
Please thank the customer for reporting this problem.

A CoT status screen is accessible in the web management interface under Node Status--> CoT Status. You can see the received messages here and it provides some useful information about how the message was processed.


