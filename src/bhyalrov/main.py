from threading import Thread
from server import start_server
from vehicleMovement import start_vehicle

def main():
    server_thread  = Thread(target=start_server)
    vehicle_thread = Thread(target=start_vehicle)

if __name__ == "__main__":
    main()
