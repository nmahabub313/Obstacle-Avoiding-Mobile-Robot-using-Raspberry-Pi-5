
# Obstacle Avoiding Robot with Raspberry Pi

This project is a simple obstacle-avoiding robot built using a Raspberry Pi, ultrasonic sensor, servo motor, and a motor driver. The robot detects obstacles in its path, scans for free space using a servo-mounted ultrasonic sensor, and turns in the direction with more distance to avoid collisions.

## Features

- Real-time obstacle detection using an ultrasonic sensor
- Automatic turning using servo-based directional scanning
- Smooth forward, backward, and turning motor controls
- PWM-based speed control for both motors
- Safe GPIO handling with cleanup on exit

## Components Required

- Raspberry Pi (any model with GPIO support)
- L298N Motor Driver Module
- 2x DC Motors
- Ultrasonic Distance Sensor (HC-SR04)
- Servo Motor (SG90 or similar)
- Power source (battery or power bank)
- Jumper wires, wheels, and robot chassis

## Wiring and GPIO Pinout

| Component         | Function       | GPIO Pin | Physical Pin |
|------------------|----------------|----------|--------------|
| Motor A Forward   | IN1            | GPIO 15  | Pin 10       |
| Motor A Backward  | IN2            | GPIO 18  | Pin 12       |
| Motor B Forward   | IN3            | GPIO 27  | Pin 13       |
| Motor B Backward  | IN4            | GPIO 17  | Pin 11       |
| Motor A Enable    | ENA (PWM)      | GPIO 22  | Pin 15       |
| Motor B Enable    | ENB (PWM)      | GPIO 23  | Pin 16       |
| Ultrasonic Trigger| TRIG           | GPIO 2   | Pin 3        |
| Ultrasonic Echo   | ECHO           | GPIO 3   | Pin 5        |
| Servo Signal      | PWM Signal     | GPIO 14  | Pin 8        |

## Software Requirements

- Python 3
- RPi.GPIO library

### Install Dependencies

```bash
sudo apt-get update
sudo apt-get install python3-rpi.gpio
```

## How It Works

1. The robot moves forward by default.
2. When an obstacle is detected within 25 cm, it stops and reverses slightly.
3. The servo motor rotates the ultrasonic sensor left and right to scan distances.
4. The robot compares the left and right distances and turns toward the direction with more space.
5. The cycle repeats as it continues moving forward.

## Running the Code

1. Connect the components as shown above.
2. Clone this repository or copy the script onto your Raspberry Pi.
3. Run the script:

```bash
python3 robot.py
```

Press `Ctrl + C` to stop the robot and clean up GPIOs safely.

## Safety Tips

- Ensure your motor power supply is separate from the Pi’s power to prevent brownouts.
- Double-check all connections before powering the robot.
- Test in a safe and open space to avoid damage.

## License

This project is licensed under the MIT License. Feel free to use and modify it for your own robotic creations.
