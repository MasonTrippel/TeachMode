import sys
import os
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
import socket
import time
import freedrive


# Configuration
ROBOT_IP = "192.168.137.149"

RECIPE = 'state'
#Set postition and config file paths
current_directory = os.path.dirname(os.path.abspath(__file__))
postition_file_path = os.path.join(current_directory, "robot_positions.txt")
configuration_file_path = os.path.join(current_directory, "control_loop_configuration.xml")
CONFIG_FILENAME = configuration_file_path
stopCollection = False

def send_script_command(ip, port, command):
    """ Send a script command directly to the UR robot. """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall((command).encode('utf8'))
    except socket.error as e:
        print(f"Socket error: {e}")

def send_popup(ip, port, message, title="Position Adjustment", blocking=True):
    """ Send a popup message to the UR robot's teach pendant. """
    blocking_str = 'True' if blocking else 'False'
    command = f'popup("{message}", title="{title}", blocking={blocking_str})'
    send_script_command(ip, port, command)
def stop():
    global stopCollection 
    stopCollection = True

def save_positions(newFilename):
    with open(newFilename, 'w') as file:
        with(open(postition_file_path, 'r')) as currentPositions:
            positionsFile = currentPositions.read()
            file.write(positionsFile)
            file.close()
    
def begin(x, y, z, rx, ry, rz):
    # Load RTDE configuration and connect
    conf = rtde_config.ConfigFile(CONFIG_FILENAME)
    output_names, output_types = conf.get_recipe(RECIPE)
    rtde_io = rtde.RTDE(ROBOT_IP, 30004)
    rtde_io.connect()
    rtde_io.send_output_setup(output_names, output_types)
    rtde_io.send_start()
    # Data collection with popup, looping indefinitely
    with open(postition_file_path, 'w') as file:
        
        print("Collecting data starting in 10 seconds. Press Ctrl+C to stop.")
        try:                       
            #Enable freedrive Mode
            freedrive.setFD(x,y,z,rx,ry,rz)
            time.sleep(10)
            global stopCollection
            stopCollection = False
            while not stopCollection: 
                time.sleep(0.25)  
                state = rtde_io.receive()
                if state:
                    position_str = ','.join(map(str, state.actual_q))
                    file.write(f"[{position_str}], \n")
                    print(position_str + '\n')
            file.close()    
                 # Delay before the next cycle begins
        except KeyboardInterrupt:
            print("Stopping data collection.")
        finally:
            # Cleanup
            send_script_command(ROBOT_IP, 30002, 'end_freedrive_mode()')
            rtde_io.disconnect()
            file.close()

if __name__ == '__main__':
    begin(1,1,1,1,0,1)
