import serial

PORT = "COM7"       # Change if needed
BAUD = 115200

ser = serial.Serial(PORT, BAUD)

print("Connected!")
on = True
while on:

    line = ser.readline().decode("utf-8").strip()
    adc, sensor_ph, sensor_moisture = line.split(",")
    print(f"ADC: {adc}, pH: {sensor_ph}, Moisture: {sensor_moisture}")