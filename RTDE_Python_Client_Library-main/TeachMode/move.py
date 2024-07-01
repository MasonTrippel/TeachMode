import socket
import ast
import os
def load_data(filename):
    arrays = []
    with open(filename, "r") as file:
        for line in file:
            # Remove whitespace and trailing commas
            line = line.strip().strip(',')
            if line:
                # Convert string representation of list to actual list
                try:
                    array = ast.literal_eval(line)
                    arrays.append(array)
                except ValueError as e:
                    print(f"Error parsing line: {line}. Error: {e}")
    return arrays

def send_urscript(ip, port, script):
    """Send a URScript command to the robot."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(script.encode('utf-8'))

def move(loop_count=1, filepath="robot_positions.txt", speed=0.05):
    robot_ip = "192.168.137.149"  # Change to your robot's IP address
    port = 30002  # Port for sending URScript commands

    
    # List of positions (each position is a list of joint angles)
    if filepath == "robot_positions.txt":
        positions = load_data(os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath))
    else:
        positions = load_data(filepath)
    # Build the URScript command with all positions in a loop
    script_commands = "def Program():\n"
    script_commands+= "  number = 0\n"
    script_commands+= f"  while number<{loop_count}:\n "
    for pos in positions:
        script_commands += f"    movej({pos}, a=0.2, v={speed}, r=0.005)\n"
    script_commands += "    number = number+1\n  end\nend\nProgram()"
    send_urscript(robot_ip, port, script_commands)
    
    file = open("urscript.txt", "w")
    file.write(script_commands)
    

if __name__ == "__main__":
    move()
