import gps
import requests

class GPS:
    def __init__(self, *args, **kwargs):
        self.enabled = False
        self.session = None
        self.stop_gps_thread = False
        self.currentLocation = { "alt": None, "climb": None, "lat": None, "lng": None, "speed": None }

    def is_enabled(self):
        return self.enabled

    def enable_gps(self):
        # start the session here
        self.session = gps.gps("localhost", "2947")
        self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
        self.enabled = True
    
    def get_current_location(self):
        return self.currentLocation

    def read_location_from_sensor(self):
        while True:
            if self.stop_gps_thread:
                #print("stopping current val = ", self.stop_gps_thread)
                break
            gps_response = self.session.next()
            try:
                if (gps_response["class"] == "TPV"):
                    # set the current location here
                    # print(str(gps_response.lat) + "," + str(gps_response.lon))
                    self.currentLocation = {
                        "alt": gps_response.alt if gps_response.alt else -1,
                        "climb": gps_response.climb if gps_response.climb else -1,
                        "lat": gps_response.lat,
                        "lng": gps_response.lon,
                        "speed": gps_response.speed if gps_response.speed else -1
                    }
            except Exception as e:
                print("Got exception " + str(e))

    def stop_gps(self):
        # print("Stopping gps now")
        self.stop_gps_thread = True

    def start_gps(self):
        self.stop_gps_thread = False