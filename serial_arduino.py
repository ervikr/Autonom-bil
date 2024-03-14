import serial
import time

def send_data(data: str, port:str = "/dev/ttyACM0", baud:int = 9600):
    data = data + "\n"
    with serial.Serial(port, baud) as ser:
        ser.write(data.encode())
    
    
if __name__ == '__main__':
    send_data("1000")