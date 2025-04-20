import socket
from pynput import keyboard
from Data import ControlData
import pickle

control_data = ControlData()
Stop_Program = False
Connected = False


def on_press(key):
    global Stop_Program
    print(key)

    #quit press esc
    if key == keyboard.Key.esc:
        Stop_Program = True
        # Stop listener
        return False

    try:
        if key.char.lower() == 'w':
            control_data.forward = True
        if key.char.lower() == 'a':
            control_data.left = True
        if key.char.lower() == 's':
            control_data.backward = True
        if key.char.lower() == 'd':
            control_data.right = True
    except:
        if key == keyboard.Key.shift:
            control_data.shift = True


    print(control_data)
    

    

def on_release(key):
    print(key)
    try:
        if key.char.lower() == 'w':
            control_data.forward = False
        if key.char.lower() == 'a':
            control_data.left = False
        if key.char.lower() == 's':
            control_data.backward = False
        if key.char.lower() == 'd':
            control_data.right = False
    except:
        if key == keyboard.Key.shift:
            control_data.shift = False

    print(control_data)

"""with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()"""

listener = keyboard.Listener(
    on_press=on_press, 
    on_release=on_release,
    daemon=True
)


HOST = '192.168.68.128'  #Raspberry Pi’s IP address
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    try:
        print("Trying to connect...")
        s.connect((HOST, PORT))
        print("Connected successfully!")
        listener.start()
        Connected = True
    except Exception as e:
        print(f"Connection failed: {e}")


    while (not Stop_Program and Connected):
        s.sendall(f"{control_data.to_string()}".encode())
        data = s.recv(1024)



listener.stop()
        

