import socket
from pynput import keyboard
from Data import ControlData




def on_press(key):
    print(f'Key {key} pressed')



    
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def on_release(key):
    print(f'Key {key} released')


HOST = '192.168.68.128'  #Raspberry Pi’s IP address
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    control_data = ControlData()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Collect events until released


