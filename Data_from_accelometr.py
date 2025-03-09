import serial

# Configure the serial port
port = 'COM10'  # Replace with your port (e.g., '/dev/ttyUSB0' on Linux/macOS)
baud_rate = 115200

# Open the serial connection
ser = serial.Serial(port, baud_rate, timeout=1)

try:
    while True:
        if ser.in_waiting > 0:
            # Read a line of data
            line = ser.readline().decode('utf-8').strip()
            if line:
                # Split the CSV data
                sensor_value, temperature = map(float, line.split(','))
                print(f"Sensor Value: {sensor_value}, Temperature: {temperature}")
except KeyboardInterrupt:
    print("Exiting program.")
finally:
    ser.close()  # Close the serial connection