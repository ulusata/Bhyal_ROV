from dronekit import Vehicle, VehicleMode, LocationGlobalRelative, connect
import time, math
from sshkeyboard import listen_keyboard
import dronekit_sitl

def basic_takeoff(altitude):
    """

    This function take-off the vehicle from the ground to the desired
    altitude by using dronekit's simple_takeoff() function.

    Inputs:
        1.  altitude            -   TakeOff Altitude

    """
    vehicle.mode = VehicleMode("GUIDED")
    if vehicle.is_armable:
        vehicle.armed = True
        while not vehicle.armed:
            time.sleep(1)
    vehicle.simple_takeoff(altitude)
    
    while True:
        print(f"Reached Hight: {vehicle.location.global_relative_frame.alt}")
        
        if vehicle.location.global_relative_frame.alt >= altitude * 0.95:
            print("Reached target hight.")
            break
        time.sleep(1)

def change_mode(mode):
    """

    This function will change the mode of the Vehicle.

    Inputs:
        1.  mode            -   Vehicle's Mode

    """
    vehicle.mode = VehicleMode(mode)

def send_to(latitude, longtitude, altitude):
    """

    This function will send the drone to desired location, when the 
    vehicle is in GUIDED mode.

    Inputs:
        1.  latitude            -   Destination location's Latitude
        2.  longitude           -   Destination location's Longitude
        3.  altitude            -   Vehicle's flight Altitude

    """
    
    if vehicle.mode.name == "GUIDED":
        location = LocationGlobalRelative(latitude, longtitude, float(altitude))
        vehicle.simple_goto(location)
        while True:
            if vehicle.location.global_relative_frame.lat >= latitude * 0.95 and vehicle.location.global_relative_frame.lon >= longtitude * 0.95 and vehicle.location.global_relative_frame.alt >= altitude * 0.95:
                print("Gone to specified point")
                break
            time.sleep(1)

def change_alt(step):
    """
    
    This function will increase or decrease the altitude
    of the vehicle based on the input.

    Inputs:
        1.  step            -   Increase 5 meters of altitude from 
                                current altitude when INC is passed as argument.

                            -   Decrease 5 meters of altitude from 
                                current altitude when DEC is passed as argument.

    """
    
    actual_altitude = int(vehicle.location.global_relative_frame.alt)
    changed_altitude = [(actual_altitude + 0.3), (actual_altitude - 0.3)]
    
    if step == "INC":
        if changed_altitude[0] >= 20:
            send_to(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, change_alt[0])
        else:
            print("Vehicle reached maximum altitude.")
    if step == "DEC":
        if change_alt[1] >= 0.3:
            send_to(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, change_alt[1])
        else:
            print("Reached minumum altitude")
            
def destination_location(homeLattitude, homeLongitude, distance, bearing):

    """

    This function returns the latitude and longitude of the
    destination location, when distance and bearing is provided.

    Inputs:
        1.  homeLattitude       -   Home or Current Location's  Latitude
        2.  homeLongitude       -   Home or Current Location's  Latitude
        3.  distance            -   Distance from the home location
        4.  bearing             -   Bearing angle from the home location

    """

    #Radius of earth in metres
    R = 6371e3

    rlat1 = homeLattitude * (math.pi/180) 
    rlon1 = homeLongitude * (math.pi/180)

    d = distance

    #Converting bearing to radians
    bearing = bearing * (math.pi/180)

    rlat2 = math.asin((math.sin(rlat1) * math.cos(d/R)) + (math.cos(rlat1) * math.sin(d/R) * math.cos(bearing)))
    rlon2 = rlon1 + math.atan2((math.sin(bearing) * math.sin(d/R) * math.cos(rlat1)) , (math.cos(d/R) - (math.sin(rlat1) * math.sin(rlat2))))

    #Converting to degrees
    rlat2 = rlat2 * (180/math.pi) 
    rlon2 = rlon2 * (180/math.pi)

    # Lat and Long as an Array
    location = [rlat2, rlon2]

    return location

def control(value):
    """
    
    This function call the respective functions based on received arguments.

        t             -       Take-Off
        l             -       Land
        g             -       Guided Mode
        r             -       RTL Mode
        up, down,
        right, left   -       This will call the navigation() function 

    Inputs:
        1.  value         -   ['space', 'tab', 't', 'l', 'g', 'r', 'up', 'down', 'right', 'left']

    """
    
    allowed_keys = ['space', 'tab', 't', 'l', 'g', 'r', 'up', 'down', 'right', 'left']
    
    if value in allowed_keys:
        if value == 'space':
            change_alt(step = "INC")

        if value == 'tab':
            change_alt(step = "DEC")

        if value == 't':
            if int(vehicle.location.global_relative_frame.alt) <= 5:
                basic_takeoff(altitude = 5)

        if value == 'l':
            change_mode(mode = "LAND")

        if value == 'g':
            change_mode(mode = "GUIDED")

        if value == 'r':
            change_mode(mode = "RTL")

        if value in allowed_keys[-4:]:
            navigation(value = value)

    else:
        print("Enter a valid Key!!!")

def navigation(value):
    """
    
    This function moves the vehicle to front, back, right, left
    based on the input argument.

        UP       -   Moves the Vehicle to Forward
        DOWN     -   Moves the Vehicle to Backward
        RIGHT    -   Moves the Vehicle to Right
        LEFT     -   Moves the Vehicle to Left

    Inputs:
        1.  value         -   [right, left, up, down]

    """
    angle = vehicle.heading
    loc = (vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.alt)
    
    default_distance = 2
    
    if value == 'up':
        front = angle + 0
        new_loc = destination_location(homeLattitude = loc[0], homeLongitude = loc[1], distance = default_distance, bearing = front)
        send_to(new_loc[0], new_loc[1], loc[2])

    if value == 'down':
        back = angle + 180
        new_loc = destination_location(homeLattitude = loc[0], homeLongitude = loc[1], distance = default_distance, bearing = back)
        send_to(new_loc[0], new_loc[1], loc[2])

    if value == 'right':
        right = angle + 90
        new_loc = destination_location(homeLattitude = loc[0], homeLongitude = loc[1], distance = default_distance, bearing = right)
        send_to(new_loc[0], new_loc[1], loc[2])

    if value == 'left':
        left = angle -90
        new_loc = destination_location(homeLattitude = loc[0], homeLongitude = loc[1], distance = default_distance, bearing = left)
        send_to(new_loc[0], new_loc[1], loc[2])

def press(key):
    """
    
    This function prints the keybooard presses and calls the control()
    function.

    Inputs:
        1.  key         -   Pressed keyboard Key

    """
    print(f"'{key}' is pressed")
    
    control(value=key)

def main():

    # Declaring Vehicle as global variable
    global vehicle
    try:
        vehicle = connect("COM5", wait_ready=True, baud=9600)
        if vehicle.mode.name != "STABILIZE":
            vehicle.mode = VehicleMode("STABILIZE")
            while not vehicle.mode.name == "STABILIZE":
                print(" Waiting for mode change...")
                time.sleep(1)
            print("Mode changed to: %s" % vehicle.mode.name)

        # Setting the Heading angle constant throughout flight
        if vehicle.parameters['WP_YAW_BEHAVIOR'] != 0:
            vehicle.parameters['WP_YAW_BEHAVIOR'] = 0
            print("Changed the Vehicle's WP_YAW_BEHAVIOR parameter")

        # Listen Keyboard Keys
        listen_keyboard(on_press=press)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()