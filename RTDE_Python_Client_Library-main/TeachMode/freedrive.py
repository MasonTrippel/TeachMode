import socket
import time

ROBOT_IP = "192.168.137.149"

def send_urscript(ip, port, script):
    """Send a URScript command to the robot."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(script.encode('utf-8'))
#Set any of the inputs x,y,z,rx,ry,rz to 1 to make the robot complient in those axes 
def setFD(x=0,y=0,z=0,rx=0,ry=0,rz=0):
    
    script_commands = "def Program():\n  popup(\"Press STOP PROGRAM to end Freedrive mode\",\"End Program\",blocking=False)\n  while True:\n"
    script_commands += f"    freedrive_mode([{x},{y},{z},{rx},{ry},{rz}])\n"
    script_commands += "  end\nend\nProgram()"
    send_urscript(ROBOT_IP, 30002, script_commands)

                
    

if __name__ == "__main__":
    setFD(x=1)
