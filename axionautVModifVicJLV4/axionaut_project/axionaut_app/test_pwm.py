import Adafruit_PCA9685
import time

servo = Adafruit_PCA9685.PCA9685()
servo.set_pwm_freq(60)

while True: 
    print("True")
    servo.set_pwm(1,0,423)
    time.sleep(1)
    servo.set_pwm(1,0,386)
    time.sleep(1)
    servo.set_pwm(1,0,350)
    time.sleep(1)
    servo.set_pwm(1,0,313)
    time.sleep(1)
    servo.set_pwm(1,0,276)
    time.sleep(1)
