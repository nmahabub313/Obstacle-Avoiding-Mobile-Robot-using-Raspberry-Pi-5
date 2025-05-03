import RPi.GPIO as GPIO
import time

# === Motor Control Pins ===
IN1 = 15  # Motor A forward
IN2 = 18  # Motor A backward
IN3 = 27  # Motor B forward
IN4 = 17  # Motor B backward
ENA = 22  # Motor A enable (PWM)
ENB = 23  # Motor B enable (PWM)

# === Ultrasonic Sensor Pins ===
TRIG = 2
ECHO = 3

# === Servo Pin ===
SERVO = 14

# === Constants ===
CENTER_ANGLE = 70
TURN_ANGLE = 60
SPEED = 75  # 0 to 100 (%)

# === Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup motor pins
motor_pins = [IN1, IN2, IN3, IN4, ENA, ENB]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# Setup PWM for motor speed control
pwm_A = GPIO.PWM(ENA, 1000)  # 1kHz
pwm_B = GPIO.PWM(ENB, 1000)
pwm_A.start(0)
pwm_B.start(0)

# Setup ultrasonic sensor pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Setup servo motor
GPIO.setup(SERVO, GPIO.OUT)
servo = GPIO.PWM(SERVO, 50)  # 50Hz
servo.start(7.5)  # Center position

# === Functions ===

def set_servo_angle(angle):
    duty = 2.5 + (angle / 18)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.4)

def distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    dist = pulse_duration * 17150
    return round(dist, 2)

def forward(speed=SPEED):
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
    pwm_A.ChangeDutyCycle(speed)
    pwm_B.ChangeDutyCycle(speed)

def backward(speed=SPEED):
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
    pwm_A.ChangeDutyCycle(speed)
    pwm_B.ChangeDutyCycle(speed)

def stop():
    pwm_A.ChangeDutyCycle(0)
    pwm_B.ChangeDutyCycle(0)
    for pin in [IN1, IN2, IN3, IN4]:
        GPIO.output(pin, False)

def turn_right(speed=SPEED):
    GPIO.output(IN1, True)
    GPIO.output(IN2, False)
    GPIO.output(IN3, False)
    GPIO.output(IN4, True)
    pwm_A.ChangeDutyCycle(speed)
    pwm_B.ChangeDutyCycle(speed)

def turn_left(speed=SPEED):
    GPIO.output(IN1, False)
    GPIO.output(IN2, True)
    GPIO.output(IN3, True)
    GPIO.output(IN4, False)
    pwm_A.ChangeDutyCycle(speed)
    pwm_B.ChangeDutyCycle(speed)

# === Main Loop ===
try:
    while True:
        set_servo_angle(CENTER_ANGLE)
        dist = distance()
        print("Front Distance:", dist)

        if dist < 25:
            stop()
            time.sleep(0.5)
            backward()
            time.sleep(0.6)
            stop()

            # Look Left
            set_servo_angle(CENTER_ANGLE + TURN_ANGLE)
            left = distance()
            print("Left Distance:", left)

            # Look Right
            set_servo_angle(CENTER_ANGLE - TURN_ANGLE)
            time.sleep(0.5)
            right = distance()
            print("Right Distance:", right)

            # Return to center
            set_servo_angle(CENTER_ANGLE)

            if left > right:
                turn_left()
            else:
                turn_right()
            time.sleep(0.7)
            stop()
        else:
            forward()

except KeyboardInterrupt:
    stop()
    pwm_A.stop()
    pwm_B.stop()
    servo.stop()
    GPIO.cleanup()
