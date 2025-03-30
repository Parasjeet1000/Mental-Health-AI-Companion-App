
import socket
import json
import time

def send_udp(ip, msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(msg).encode(), (ip, 4003))

def breathing_loop(ip, cycles=3):
    print("🧘‍♂️ Starting breathing animation...")
    for _ in range(cycles):
        # Breathe in (brighten)
        for brightness in range(10, 101, 10):
            msg = {
                "msg": {
                    "cmd": "brightness",
                    "data": {"value": brightness}
                }
            }
            send_udp(ip, msg)
            time.sleep(0.2)

        # Breathe out (dim)
        for brightness in range(100, 9, -10):
            msg = {
                "msg": {
                    "cmd": "brightness",
                    "data": {"value": brightness}
                }
            }
            send_udp(ip, msg)
            time.sleep(0.2)


            send_udp(ip, {
                "msg": {
                    "cmd": "brightness",
                    "data": {"value": 50}
                }
            })

    print("✅ Finished breathing sequence.")
