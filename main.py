
# Import Modules
from machine import Pin, I2C, UART
import time
from picozero import DistanceSensor
from ssd1306 import SSD1306_I2C
import framebuf


# RGB led Pins
green = Pin(13, Pin.OUT)
red = Pin(12, Pin.OUT)
blue = Pin(11, Pin.OUT)



# Buzzer Pin
buzz = Pin(19, Pin.OUT)



# Flame sensor Pin
flame = Pin(15, Pin.IN)



# MQ5 sensor Pin
gass = Pin(14, Pin.IN)


# Ultrasonic sensor Pin
ds = DistanceSensor(echo=5, trigger=4)


# Push button Pin
button = Pin(20, Pin.IN, Pin.PULL_UP)


# HC-05 sensor Pins
uart1 = UART(1,baudrate=9600,tx=Pin(8),rx=Pin(9))


# OLED Pin
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
oled = SSD1306_I2C(128, 64, i2c)


# System Flag
flag = True


# RGB LED 
def rgb(r, g, b):
    red.value(r)
    green.value(g)
    blue.value(b)


# OLED helper functions
def oled_write(text, x, y):
    oled.text(text, x, y)
    oled.show()


def oled_clear():
    oled.fill(0)
    oled.show()



# RTC function    
def get_rtc_time():
    dt = time.localtime()  
    return f"{dt[0]}/{dt[1]}/{dt[2]}-{dt[4]}:{dt[5]}:{dt[6]}"


# fire animation
def show_flame(duration=4):
    end_time = time.time() + duration
    blink_interval = 1  

    while time.time() < end_time:
        oled.fill(0)
        oled.text("FLAME", 20, 10)
        oled.text("FLAME!!! HELPPP!!!", 0, 50)  
        oled.text(get_rtc_time(), 0, 40)
        oled.show()
        time.sleep(blink_interval)

        oled.fill(0)
        oled.text("FLAME!!! HELPPP!!!", 0, 50)  
        oled.text(get_rtc_time(), 0, 40)
        oled.show()



# gas animation

def show_gass(duration=4):
    end_time = time.time() + duration
    blink_interval = 1  

    while time.time() < end_time:
        oled.fill(0)
        oled.text("GASS", 20, 10)
        oled.text("GASS DETECTION!!!", 0, 50)
        oled.text(get_rtc_time(), 0, 40)
        oled.show()
        time.sleep(blink_interval)

        oled.fill(0)
        oled.text("GASS DETECTION!!!", 0, 50)
        oled.text(get_rtc_time(), 0, 40)
        oled.show()
     

 
#Move detect oled
def movement_oled():
    oled_clear()
    oled_write("Somebody is",5,30)
    oled_write("too close!!!!",5,40)


# Motion detector
def motion_detector(ds):
    dist = ds.distance
    if dist is None:
        print("No reading from ultrasonic sensor")
        return

    if dist <= 0.2:  
        buzz.value(1)
        rgb(1, 0, 0)
        movement_oled()
        time.sleep(0.5)
        buzz.value(0)
        return True
    else:
        buzz.value(0)
        oled_clear()
        time.sleep(0.1)
        return False


# Flame detector
def flame_detector():
    if flame.value() != 0:
        rgb(1, 0, 0)
        buzz.value(1)
        show_flame()
        buzz.value(0)
        return True
    else:
        oled_clear()
        return False

# Smoke detector
def smoke_detector():
    if gass.value() == 0:
        rgb(1, 0, 0)
        buzz.value(1)
        show_gass()
        buzz.value(0)
        return True
    else:
        oled_clear()
        return False

# Manager function        
def detectors(ds):
    x1 = smoke_detector()
    x2 = flame_detector()
    x3 = motion_detector(ds)
    if x1 == False and x2 == False and x3 == False:
        rgb(0,1,0)


# HC-05 module function    
def uart_control(last_flag, uart1):
    if uart1.any():
        message = uart1.read()
        if message:
            message = message.decode().strip().lower()
            if message == 'on':
                return True
            elif message == 'off':
                oled_clear()
                return False
    return last_flag

# Determine the flag's status
def flag_state(button, uart1, last_flag):
    flag = uart_control(last_flag, uart1)

    if button.value() == 0:  
        time.sleep(0.2)  
        flag = not flag

    return flag


# Main loop
while True:
    flag = flag_state(button,uart1,flag)
    if flag == True:
        detectors(ds)
    else:
        rgb(1,1,1)
