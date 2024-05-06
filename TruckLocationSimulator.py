from HelperFunctions import Message, TruckDetails, current_time_in_millis 
import sys
from time import sleep

from MQTTPublisher import MQTT

CONFIG_FILE = 'simulator.conf'
INVALID_LAT_LONG_FREQ = 21 # every 21 samples generate invalid lat and long

num_of_vehicles_to_simulator = 0
speed_limit = 0
update_frequency = 5 #sec
truckDetailsList = []
ten_primes = [5,7,11,13,17,19, 23,29, 31,37]

def ReadCommandLineArgs():
    global num_of_vehicles_to_simulator, speed_limit, update_frequency
   # Verify that the command line arguments have the right details
    print("Reading command line arguments ...")
    try:
        argLen = len(sys.argv)
        if argLen < 3:
            print("Error:: Specify Correct Command Line parameters")
            print("Usage: python TruckLocationSimulator.py NumOfVehiclesToSimulate SpeedLimit UpdateSpeed(optional)")
            sys.exit(1)
        else:
            num_of_vehicles_to_simulator = int(sys.argv[1])
            # print("num_of_vehicles_to_simulator" + str(num_of_vehicles_to_simulator))
            if num_of_vehicles_to_simulator > 10 or num_of_vehicles_to_simulator < 1:
                print("Number of vehicles to simulate needs to be between 1 and 10")
                sys.exit(1)

            speed_limit = int(sys.argv[2])
            if speed_limit > 150 or speed_limit < 20:
                print("Max Speed for trucks needs to be between 20 and 150")
                sys.exit(1)

            if argLen > 3:
                update_frequency = int(sys.argv[3])
                if update_frequency > 90 or update_frequency < 1:
                    print("update frequency of truck data needs to be between 1 and 90 seconds")
                    sys.exit(1)

            #print("Read success")
    except SystemExit:
        pass
    except Exception:
        print("Error in reading command line args :: Specify Correct Command Line parameters")
        print("Usage: python TruckLocationSimulator.py NumOfVehicesToSimulate SpeedLimit UpdateSpeed(optional)")
        sys.exit(1)


def ReadConfiguration():
    print("Reading configuration ...")

    global CONFIG_FILE, truckDetailsList
    with open(CONFIG_FILE) as f:
        truck_list = []
        firstLine = True

        for line in f:
            if (firstLine == True): # Skip first line it is comment
                firstLine = False
                continue

            words = line.split()

            if (truck_list.__contains__(words[0])): #Duplicate truck numbers in the config file
                print("Error:: Verify the Config file it should not contain duplicate truck numbers")
                sys.exit(1)
            else:
                truck_list.append(words[0])
                initialTruckSpeed = speed_limit * len(truck_list)//(num_of_vehicles_to_simulator + 1)
                truckDetail =  TruckDetails(truckNumber=words[0], route=words[1], latitude=words[2], longitude=words[3], speed=initialTruckSpeed)
                truckDetailsList.append(truckDetail)
        if len(truckDetailsList) != num_of_vehicles_to_simulator:
            print("Number of trucks in configuration and command line do not match. Ensure you specify the right command line and configuration")
            sys.exit(1)

        
def StartSimulating():
    print("Starting Simulation ... \n")
    mqtt = MQTT()
    try:
        # Add a while true here
        latitude = 0.0
        longitude = 0.0 
        speed = 0
        outerIndex = 1
        while True:
            index = 0
            print("Publishing Data ... \n")
            for truckDetails in truckDetailsList:
                if (outerIndex % ten_primes[index] == 0): # generate overspeeding event
                    speed = speed_limit + ten_primes[index]
                else:
                    speed = truckDetails.speed

                if (outerIndex % INVALID_LAT_LONG_FREQ == 0): # generate invalid lat and long every INVALID_LAT_LONG_FREQ sample
                    latitude = 100
                    longitude = 200
                else:
                    latitude = truckDetails.latitude
                    longitude = truckDetails.longitude
                
                msgPayload = Message(current_time_in_millis(), truckDetails.truckNumber, latitude, longitude, truckDetails.route, speed)
                mqtt.Publish(msgPayload.toJSON())

                truckDetails.latitude = (float)(truckDetails.latitude) + 0.001
                truckDetails.longitude = (float)(truckDetails.longitude) + 0.001
                truckDetails.speed = truckDetails.speed + 5

                if (truckDetails.speed > speed_limit):
                    truckDetails.speed = speed_limit // 2
                index = index + 1
            sleep(update_frequency)
            outerIndex = outerIndex + 1
    except:
        print("Exception occured in Simulation ...")
    finally:
        mqtt.Disconnect() 

    
    
def PrintTruckDetails():
    print("The number of trucks is " + str(len(truckDetailsList)))
    for truckDetail in truckDetailsList:
        print(truckDetail)

def main():
    ReadCommandLineArgs()
    ReadConfiguration()
    StartSimulating()
    # PrintTruckDetails()

if __name__ == "__main__":
    main()