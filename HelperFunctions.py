import time
import json

def current_time_in_millis():
    return round(time.time() * 1000)

class TruckDetails:
  def __init__(self, truckNumber, latitude, longitude, route, speed):
    self.truckNumber = truckNumber
    self.latitude = latitude
    self.longitude = longitude
    self.route = route
    self.speed = speed

  def __str__(self):
    return f"{self.truckNumber}, {self.latitude}, {self.longitude}, {self.route}, {self.speed} "

# Class to specify the message to exchange
class Message:
   def __init__(self, timestamp, truckNumber, latitude, longitude, route, speed):
      
      self.timestamp =  timestamp
      self.truckNumber =  truckNumber
      self.latitude =  latitude
      self.longitude =  longitude
      self.route =  route
      self.speed =  speed


   def toJSON(self):
      return json.dumps(
         self,
         default=lambda o: o.__dict__, 
         sort_keys=False)
   
   def __str__(self):
    return f"{self.timestamp}, {self.truckNumber}, {round(self.latitude,3)}, {round(self.longitude,3)}, {self.route}, {self.speed}"