import time
import socket
import threading
import serial

# Set the IP address and port
HOST = '127.0.0.1'  # Localhost (change if Gpredict is running elsewhere)
PORT = 4533         # Default port used by Hamlib rotctld

#generate timestamp
timestr = time.strftime("%Y%m%d-%H%M%S")

#connect to tailgater
dish = serial.Serial(
	port='/dev/ttyACM0',
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1)

# Global variables to store the current azimuth and elevation
current_azimuth = 0
current_elevation = 8
tailgater_setaz = None
tailgater_setel = None
add180 = 180


def parse_command(command):
    """Parse the azimuth and elevation from the Gpredict command."""
    try:
        # Commands are expected to be like "P AZ EL", e.g., "P 180.0 45.0"
        if command.startswith("P"):
            _, az, el = command.split()
            return float(az), float(el)
    except ValueError:
        print("Invalid command format.")
    return None, None

def handle_client_connection(client_socket):
    """Handle the incoming commands from Gpredict."""
    global current_azimuth, current_elevation  # Access the global variables

    while True:
        data = client_socket.recv(1024).decode('utf-8').strip()
        if not data:
            break  # Connection closed
        print(f"Received command: {data}")
        
        # Parse azimuth and elevation
        az, el = parse_command(data)
        if az is not None and el is not None:
            # Store the azimuth and elevation in the global variables
            current_azimuth = az
            current_elevation = el
            print(f"Updated Azimuth: {current_azimuth}, Elevation: {current_elevation}")

        # Send acknowledgment or response if needed
        command2 = "set_pos {current_azimuth:.2f} {current_elevation.2f}\n"
        client_socket.sendall(command2.encode('utf-8')) # Send OK response (Hamlib standard)

def start_server():
    """Start a server to receive az/el commands."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"Listening on {HOST}:{PORT}...")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        # Handle the client connection in a new thread
        client_handler = threading.Thread(target=handle_client_connection, args=(client_socket,))
        client_handler.start()

def monitor_az_el():
    """Continuously monitor and print the azimuth and elevation values."""
    global current_azimuth, current_elevation, tailgater_setaz, tailgater_setel  # Access the global variables
    while True:
        if current_azimuth is not None and current_elevation is not None:
            print(f"Current Azimuth: {current_azimuth}, Current Elevation: {current_elevation}")
        else:
            print("Waiting for azimuth and elevation data...")
        # Sleep for a bit before checking again (to avoid spamming the output)
        tailgater_setaz = 360 - current_azimuth
        tailgater_setel = current_elevation
        print(f"tailgater set to AZ: {tailgater_setaz} EL: {tailgater_setel}")
        numberaz = round(tailgater_setaz)

        # Split the number into hundreds, tens, and ones
        a3 = numberaz // 100         # Get the hundreds digit
        a2 = (numberaz % 100) // 10      # Get the tens digit
        a1 = numberaz % 10               # Get the ones digit
        print(f"hundreds AZ {a3}")
        print(f"tens AZ {a2}")
        print(f"ones AZ {a1}")

        # Output the result
        numberel = round(tailgater_setel)

        # Split the number into hundreds, tens, and ones
                
        e2 = (numberel % 100) // 10      # Get the tens digit
        e1 = numberel % 10               # Get the ones digit
        print(f"tens EL {e2}")
        print(f"ones EL {e1}")
        #encode bytes
        ae3 = (str(a3)).encode()
        ae2 = (str(a2)).encode()
        ae1 = (str(a1)).encode()
        ee2 = (str(e2)).encode()
        ee1 = (str(e1)).encode()

        # Output the result
        dish.write(b'a')
        dish.write(b'z')
        dish.write(b'a')
        dish.write(b'n')
        dish.write(b'g')
        dish.write(b'l')
        dish.write(b'e')
        dish.write(b' ')
        if a3 and a2 == 0:
            dish.write(ae1)
            dish.write(b'\r')
        elif a3 == 0:
            dish.write(ae2)
            dish.write(ae1)
            dish.write(b'\r')
        else:
            dish.write(ae3)
            dish.write(ae2)
            dish.write(ae1)
            dish.write(b'\r')
            time.sleep(1)
        dish.write(b'e')
        dish.write(b'l')
        dish.write(b'a')
        dish.write(b'n')
        dish.write(b'g')
        dish.write(b'l')
        dish.write(b'e')
        dish.write(b' ')
        if e2 == 0:
            dish.write(ee1)
            dish.write(b'\r')
        else:
            dish.write(ee2)
            dish.write(ee1)
            dish.write(b'\r')
            
            
            
            
       
        
        time.sleep(1)

if __name__ == "__main__":
    # Start the server in a separate thread to handle Gpredict connections
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Monitor the azimuth and elevation in the main thread
    monitor_az_el()
